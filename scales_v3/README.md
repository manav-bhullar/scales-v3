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
| **SHRR** | Human review / deferral resolution | Done (Sprint 5) |
| **Aggregator** | Discrete marks → student total | Done (Sprint 5) |
| **Pipeline** | Two-phase orchestrator + JSON persistence | Done (Sprint 5) |
| **API** | FastAPI REST (status / review / finalize) | Done (Sprint 6) |
| **Frontend** | React + Material 3 Expressive teacher UI | Done (Sprint 6) |

**Locked for this build:** JSON persistence, LiteLLM providers (Groq primary / Gemini optional), discrete marks `0 / 0.5× / 1.0×`, CBTE τ = 0.5 (manual).

**Out of scope (first build):** Tier 3 synonym stability, batch propagation, CRC, Coherence CQA, ECF, LLM response cache.

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
# Edit .env and set GROQ_API_KEY (primary) and/or GOOGLE_API_KEY (optional)

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
# Edit .env and set GROQ_API_KEY (primary) and/or GOOGLE_API_KEY (optional)
python scripts/download_models.py
python scripts/verify_setup.py
pytest tests/unit/ -v
```

## Configuration

| Setting | Location | Notes |
|---------|----------|--------|
| `OPENROUTER_API_KEY` | `.env` | Primary for Wave 3+ live grading (`open_router_api_key` also accepted) |
| `GROQ_API_KEY` | `.env` | Optional Groq fallback |
| `GOOGLE_API_KEY` | `.env` | Optional Gemini fallback |
| LLM models | `config/settings.yaml` | Default: OpenRouter Llama (`openrouter/meta-llama/llama-3.3-70b-instruct` CERA, `openrouter/meta-llama/llama-3.1-8b-instruct` CGR) |
| NLI model | `config/settings.yaml` | `cross-encoder/nli-deberta-v3-base` on `cpu` |
| Concurrency | `llm.max_concurrent_calls` | Keep at `1` on Groq free TPM limits |

## Pipeline CLI (Sprint 5)

```powershell
# Grade an exam JSON (CERA→CGR→CBTE); writes data/exams/{exam_id}/
python scripts/run_pipeline.py grade --exam-json path\to\exam.json

# Inspect deferred review queue
python scripts/run_pipeline.py status --exam-id exam_abc

# Submit one teacher correction
python scripts/run_pipeline.py review --exam-id exam_abc --student STU001 --concept Q1_C1 --verdict FULL --marks 1.0

# Aggregate finals when review is complete
python scripts/run_pipeline.py finalize --exam-id exam_abc
```

## Teacher UI + API (Sprint 6)

Review and finalize exams without loading the NLI model (review paths are lightweight).

```powershell
# Terminal 1 — API (from scales_v3/)
$env:PYTHONPATH = (Get-Location).Path
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
# open http://127.0.0.1:5173
```

Screens: exam dashboard → review queue (Agree / Correct, inline evidence highlight, Explain sheet) → results.

API surface:
- `GET /api/exams`
- `GET /api/exams/{id}/status`
- `GET /api/exams/{id}/review`
- `POST /api/exams/{id}/review`
- `POST /api/exams/{id}/finalize`
- `GET /api/exams/{id}/results`

Live grading remains on the CLI (`scripts/run_pipeline.py grade`) for v1.

## E2E eval helpers

```powershell
# Re-run CBTE only on saved CGR results (no LLM quota) — proves Signal-1 fixes
python scripts/reeval_cbte.py --exam-id e2e_wave2_tcp_handshake_groq

# Append accuracy / DEFER / false-DEFER metrics to the research ledger
python scripts/metrics_ledger.py `
  --exam-dir data/exams/e2e_wave2_tcp_handshake_groq `
  --gold data/e2e_eval/wave2/gold_labels.json `
  --run-id wave2_baseline `
  --notes "original wave2 run"
```

## Tests

```powershell
# Fast (mocked LLM/NLI) — no API cost
pytest tests/unit/ -v

# Live LLM (costs free-tier quota; currently Groq in settings.yaml)
pytest tests/integration/test_services_live.py::test_live_llm_call tests/integration/test_cera_cgr_live.py -v --run-live

# Live DeBERTa NLI (local model; no cloud API)
pytest tests/integration/test_services_live.py::test_live_nli_entailment tests/integration/test_nli_benchmark.py -v --run-live
```

## Package layout

```
scales_v3/
  scales/           # core package
    models/         # Pydantic schemas
    services/       # LLMClient, NLIService, text utils
    modules/        # CERA, CGR, CBTE, SHRR, Aggregator
    persistence.py  # per-exam JSON store
    pipeline.py     # two-phase orchestrator
  config/           # settings.yaml + prompt templates
  data/             # exams, NLI benchmark pairs, e2e_eval ledger
  scripts/          # download_models, verify_setup, run_pipeline, reeval_cbte, metrics_ledger
  tests/            # unit + integration
  api/              # FastAPI (Sprint 6)
  frontend/         # React UI (Sprint 6)
```

## Sprint status

1. Foundation (models, config, fixtures) — done  
2. Services (LLM + NLI wrappers) — done  
3. CERA + CGR — done  
4. CBTE + NLI domain benchmark — done  
5. SHRR + Aggregator + end-to-end pipeline — done  
6. API + UI (Material 3 Expressive) — done  
7. Evaluation / FYP metrics (ledger + gold growth in progress)

## Documentation

Design docs and papers live in `../documentation/` at the workspace root (not pushed to this repo).

## License

MIT (see `pyproject.toml`).
