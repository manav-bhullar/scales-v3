# SCALES v3.0

Structured Concept-Anchored LLM Evaluation System — FYP research prototype for reliable automated short answer grading.

## Scope (locked)

- Skeleton: CERA → CGR → CBTE (Tier 1 + Tier 2) → SHRR → Aggregator
- Persistence: JSON files
- LLM provider: Gemini (via LiteLLM)
- Out of scope for first build: Tier 3 synonym stability, batch propagation, CRC, Coherence CQA, ECF

## Quick start

```bash
cd scales_v3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY

python scripts/download_models.py   # DeBERTa-NLI (~1.7 GB)
python scripts/verify_setup.py
pytest tests/unit/ -v
```

## Documentation

Project design docs and papers live in `../documentation/` at the workspace root.

## Package layout

- `scales/` — core research package (models, modules, services, pipeline)
- `api/` — FastAPI layer (Sprint 6)
- `frontend/` — React UI (Sprint 6)
- `config/` — settings + prompt templates
- `scripts/` — setup and CLI utilities
- `tests/` — unit + integration tests
