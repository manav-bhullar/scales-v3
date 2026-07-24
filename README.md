# Text Answer Evaluation System

Final Year Project: reliable automated short answer grading (**SCALES v3.0**).

## Workspace layout

```
text ans eval system/
├── documentation/     # Research + design + engineering reviews (source of truth)
└── scales_v3/         # Implementation codebase
```

## Getting started

```bash
cd scales_v3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Set GOOGLE_API_KEY in .env

python scripts/verify_setup.py
pytest tests/unit/ -v
```

## Prompt fine-tuning log

Record each prompt edit and why (failure mode / wave / student):

```powershell
cd scales_v3
python scripts/log_prompt_change.py list
python scripts/log_prompt_change.py add `
  --prompt cgr_grading.txt `
  --what "What wording changed" `
  --why "What failure motivated it" `
  --evidence "wave / student ids"
```

See `scales_v3/config/prompts/PROMPT_CHANGELOG.md`.

See `scales_v3/README.md` and `documentation/README.md` for details.
