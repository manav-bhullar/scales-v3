"""Unit tests for NLIService (mocked model)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import torch

from scales.services.nli_service import NLIPrediction, NLIService


def _build_service_with_mock():
    with patch("transformers.AutoTokenizer.from_pretrained") as tok_cls, patch(
        "transformers.AutoModelForSequenceClassification.from_pretrained"
    ) as model_cls:
        tokenizer = MagicMock()
        model = MagicMock()
        model.config.id2label = {0: "contradiction", 1: "entailment", 2: "neutral"}
        model.to.return_value = model
        model.eval.return_value = None

        def fake_tokenizer(premises, hypotheses, **kwargs):
            batch = len(premises)
            return {
                "input_ids": torch.ones(batch, 4, dtype=torch.long),
                "attention_mask": torch.ones(batch, 4, dtype=torch.long),
            }

        tokenizer.side_effect = None
        tokenizer.__call__ = MagicMock(side_effect=fake_tokenizer)
        # AutoTokenizer.from_pretrained returns tokenizer object that is callable
        tok_instance = MagicMock(side_effect=fake_tokenizer)
        tok_cls.return_value = tok_instance

        # logits favor entailment for first row
        logits = torch.tensor([[0.1, 3.0, 0.2], [3.0, 0.1, 0.2]])
        model.return_value = MagicMock(logits=logits)
        model_cls.return_value = model

        service = NLIService(model_name="mock-nli", device="cpu")
        # Replace tokenizer with callable mock
        service._tokenizer = tok_instance
        service._model = model
        service._id2label = {0: "contradiction", 1: "entailment", 2: "neutral"}
        return service, model


def test_empty_inputs_return_neutral():
    service, _ = _build_service_with_mock()
    pred = service.predict("", "hypothesis")
    assert pred.neutral == 1.0
    assert pred.entailment == 0.0


def test_predict_entailment_path():
    service, model = _build_service_with_mock()
    # Single pair → model returns first logit row (entailment high)
    model.return_value = MagicMock(logits=torch.tensor([[0.1, 3.0, 0.2]]))
    pred = service.predict("A cat is an animal", "There is an animal")
    assert isinstance(pred, NLIPrediction)
    assert pred.entailment > pred.contradiction
    assert pred.entailment_probability == pred.entailment


def test_predict_batch_length():
    service, model = _build_service_with_mock()
    model.return_value = MagicMock(
        logits=torch.tensor([[0.1, 3.0, 0.2], [3.0, 0.1, 0.2]])
    )
    preds = service.predict_batch(
        [
            ("A cat is an animal", "There is an animal"),
            ("A cat is an animal", "There is a dog"),
        ]
    )
    assert len(preds) == 2
    assert preds[0].entailment > 0.5
    assert preds[1].contradiction > 0.5


def test_is_loaded():
    service, _ = _build_service_with_mock()
    assert service.is_loaded() is True
