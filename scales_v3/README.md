# SCALES v3.0

Structured Concept-Anchored LLM Evaluation System — FYP research prototype for reliable automated short-answer grading.

## Pipeline

```
CERA → CGR → CBTE (Tier 1 + Tier 2) → SHRR → Aggregator
```

| Module | Role | Status |
|--------|------|--------|
| **CERA** | Concept extraction from question + rubric | Done (Sprint 3) |
| **CGR** | Per-concept grading (FULL / PARTIAL / INCORRECT / ABSENT) | Done (Sprint 3) |
| **CBTE** | Trust estimation (evidence + keywords → DeBERTa NLI) | Done (Sprint 4) |
| **SHRR** | Human review / deferral resolution | Next (Sprint 5) |
| **Aggregator** | Discrete marks → student total | Next (Sprint 5) |

**Locked for this build:** JSON persistence, Gemini via LiteLLM, discrete marks `0 / 0.5× / 1.0×`, CBTE τ = 0.5 (manual).

**Out of scope (first build):** Tier 3 synonym stability, batch propagation, CRC, Coherence CQA, ECF.

## Quick start

### Windows (PowerShell)

```powershell
cd scales_v3
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# CPU PyTorch (recommended for this prototype)
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

Copy-Item .env.example .env
# Edit .env and set GOOGLE_API_KEY

python scripts/download_models.py   # DeBERTa-NLI ~1.7 GB (first run)
python scripts/verify_setup.py
pytest tests/unit/ -v
```

### macOS / Linux

```bash
cd scales_v3
python3 -m venv .venv
source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY
python scripts/download_models.py
python scripts/verify_setup.py
pytest tests/unit/ -v
```

## Configuration

| Setting | Location | Notes |
|---------|----------|--------|
| `GOOGLE_API_KEY` | `.env` | Required for live Gemini calls |
| LLM models | `config/settings.yaml` | Default: `gemini/gemini-flash-latest` |
| NLI model | `config/settings.yaml` | `cross-encoder/nli-deberta-v3-base` on `cpu` |
| Concurrency | `llm.max_concurrent_calls` | Lower to `2–4` on Gemini free tier |

## Tests

```powershell
# Fast (mocked LLM/NLI) — no API cost
pytest tests/unit/ -v

# Live Gemini (costs quota)
pytest tests/integration/test_services_live.py::test_live_llm_call tests/integration/test_cera_cgr_live.py -v --run-live

# Live DeBERTa NLI (local model; no Gemini)
pytest tests/integration/test_services_live.py::test_live_nli_entailment tests/integration/test_nli_benchmark.py -v --run-live
```

## Package layout

```
scales_v3/
  scales/           # core package
    models/         # Pydantic schemas
    services/       # LLMClient, NLIService, text utils
    modules/        # CERA, CGR, CBTE (+ SHRR/Aggregator later)
  config/           # settings.yaml + prompt templates
  data/             # exams, NLI benchmark pairs
  scripts/          # download_models.py, verify_setup.py
  tests/            # unit + integration
  api/              # FastAPI (Sprint 6)
  frontend/         # React UI (Sprint 6)
```

## Sprint status

1. Foundation (models, config, fixtures) — done  
2. Services (LLM + NLI wrappers) — done  
3. CERA + CGR — done  
4. CBTE + NLI domain benchmark — done  
5. SHRR + Aggregator + end-to-end pipeline — **next**  
6. API + UI  
7. Evaluation / FYP metrics  

## Documentation

Design docs and papers live in `../documentation/` at the workspace root (not pushed to this repo).

## License

MIT (see `pyproject.toml`).
