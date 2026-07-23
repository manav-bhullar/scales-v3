"""DeBERTa-NLI service for CBTE Tier 2 entailment checks."""

from __future__ import annotations

from dataclasses import dataclass

from loguru import logger


@dataclass
class NLIPrediction:
    entailment: float
    contradiction: float
    neutral: float

    @property
    def entailment_probability(self) -> float:
        """Alias used by CBTE pipeline docs."""
        return self.entailment


class NLIService:
    """Load-once DeBERTa NLI wrapper."""

    def __init__(self, model_name: str, device: str = "cpu") -> None:
        self.model_name = model_name
        self.device = device
        self._tokenizer = None
        self._model = None
        self._id2label: dict[int, str] = {}
        self._load()

    def _load(self) -> None:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        try:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self._model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            requested = self.device
            if requested.startswith("cuda") and not torch.cuda.is_available():
                logger.warning("CUDA requested but unavailable; falling back to CPU")
                requested = "cpu"
            self.device = requested
            self._model.to(self.device)
            self._model.eval()
            self._id2label = {int(k): v.lower() for k, v in self._model.config.id2label.items()}
            logger.bind(module="nli").info(
                "Loaded NLI model {} on {}", self.model_name, self.device
            )
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"Failed to load NLI model '{self.model_name}'. "
                "Run scripts/download_models.py or check network/HuggingFace access. "
                f"Underlying error: {exc}"
            ) from exc

    def is_loaded(self) -> bool:
        return self._model is not None and self._tokenizer is not None

    def predict(self, premise: str, hypothesis: str) -> NLIPrediction:
        if not premise.strip() or not hypothesis.strip():
            return NLIPrediction(entailment=0.0, contradiction=0.0, neutral=1.0)
        return self.predict_batch([(premise, hypothesis)])[0]

    def predict_batch(self, pairs: list[tuple[str, str]]) -> list[NLIPrediction]:
        if not pairs:
            return []
        if not self.is_loaded():
            raise RuntimeError("NLI model is not loaded")

        import torch
        import torch.nn.functional as F

        # Empty pairs → neutral
        results: list[NLIPrediction | None] = [None] * len(pairs)
        valid_indices: list[int] = []
        valid_premises: list[str] = []
        valid_hypotheses: list[str] = []

        for idx, (premise, hypothesis) in enumerate(pairs):
            if not premise.strip() or not hypothesis.strip():
                results[idx] = NLIPrediction(entailment=0.0, contradiction=0.0, neutral=1.0)
            else:
                valid_indices.append(idx)
                valid_premises.append(premise)
                valid_hypotheses.append(hypothesis)

        if not valid_indices:
            return [r for r in results if r is not None]  # type: ignore[misc]

        encoded = self._tokenizer(
            valid_premises,
            valid_hypotheses,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True,
        )
        # Warn if truncation likely occurred for very long inputs
        for premise, hypothesis in zip(valid_premises, valid_hypotheses):
            if len(premise) + len(hypothesis) > 2000:
                logger.warning("NLI input may be truncated to 512 tokens")

        encoded = {k: v.to(self.device) for k, v in encoded.items()}
        with torch.no_grad():
            logits = self._model(**encoded).logits
            probs = F.softmax(logits, dim=-1).cpu()

        for batch_i, result_i in enumerate(valid_indices):
            row = probs[batch_i]
            mapped = {"entailment": 0.0, "contradiction": 0.0, "neutral": 0.0}
            for label_id, label_name in self._id2label.items():
                value = float(row[label_id].item())
                if "entail" in label_name:
                    mapped["entailment"] = value
                elif "contradict" in label_name:
                    mapped["contradiction"] = value
                else:
                    mapped["neutral"] = value
            results[result_i] = NLIPrediction(**mapped)

        return [r if r is not None else NLIPrediction(0.0, 0.0, 1.0) for r in results]
