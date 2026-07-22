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

See `scales_v3/README.md` and `documentation/README.md` for details.
