#!/usr/bin/env python3
"""Log prompt fine-tuning changes (what changed + why).

Usage (from scales_v3/):
  python scripts/log_prompt_change.py add \\
    --prompt cgr_grading.txt \\
    --what "..." \\
    --why "..." \\
    --evidence "waveX / student ids / metric" \\
    --result "optional outcome"

  python scripts/log_prompt_change.py list
  python scripts/log_prompt_change.py show PC-003
  python scripts/log_prompt_change.py rebuild
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROMPTS_DIR = Path(__file__).resolve().parents[1] / "config" / "prompts"
LEDGER = PROMPTS_DIR / "changes.jsonl"
CHANGELOG_MD = PROMPTS_DIR / "PROMPT_CHANGELOG.md"
SNAPSHOTS = PROMPTS_DIR / "snapshots"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def _load() -> list[dict[str, Any]]:
    if not LEDGER.exists():
        return []
    entries: list[dict[str, Any]] = []
    for i, line in enumerate(LEDGER.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Corrupt changes.jsonl line {i}: {exc}") from exc
    return entries


def _next_id(entries: list[dict[str, Any]]) -> str:
    max_n = 0
    for e in entries:
        eid = str(e.get("id", ""))
        if eid.startswith("PC-"):
            try:
                max_n = max(max_n, int(eid.split("-", 1)[1]))
            except ValueError:
                continue
    return f"PC-{max_n + 1:03d}"


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def _snapshot(prompt_file: str, entry_id: str) -> str | None:
    src = PROMPTS_DIR / prompt_file
    if not src.exists():
        return None
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    dest_name = f"{entry_id}_{prompt_file}"
    dest = SNAPSHOTS / dest_name
    shutil.copy2(src, dest)
    return f"snapshots/{dest_name}"


def _append(entry: dict[str, Any]) -> None:
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def cmd_add(args: argparse.Namespace) -> int:
    prompt_file = args.prompt
    if "/" in prompt_file or "\\" in prompt_file:
        prompt_file = Path(prompt_file).name
    src = PROMPTS_DIR / prompt_file
    if not src.exists():
        raise SystemExit(f"Prompt file not found: {src}")

    entries = _load()
    entry_id = _next_id(entries)
    snap = None if args.no_snapshot else _snapshot(prompt_file, entry_id)
    entry: dict[str, Any] = {
        "id": entry_id,
        "ts": _iso(_utc_now()),
        "prompt_file": prompt_file,
        "what": args.what.strip(),
        "why": args.why.strip(),
        "evidence": (args.evidence or "").strip() or None,
        "result": (args.result or "").strip() or None,
        "related_prompts": [
            p.strip() for p in (args.related or "").split(",") if p.strip()
        ],
        "sha256_16": _file_sha(src),
        "snapshot": snap,
    }
    _append(entry)
    if not args.no_rebuild:
        _rebuild(_load())
    print(f"Logged {entry_id} for {prompt_file}")
    print(f"  what: {entry['what']}")
    print(f"  why:  {entry['why']}")
    if snap:
        print(f"  snapshot: {snap}")
    return 0


def _safe_print(text: str) -> None:
    """Avoid Windows cp1252 crashes on arrows / fancy punctuation."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def cmd_list(args: argparse.Namespace) -> int:
    entries = _load()
    if args.prompt:
        name = Path(args.prompt).name
        entries = [e for e in entries if e.get("prompt_file") == name]
    for e in entries:
        day = str(e.get("ts", ""))[:10]
        _safe_print(f"{e.get('id')}  {day}  {e.get('prompt_file')}")
        _safe_print(f"  what: {e.get('what')}")
        _safe_print(f"  why:  {e.get('why')}")
        if args.verbose:
            if e.get("evidence"):
                _safe_print(f"  evidence: {e['evidence']}")
            if e.get("result"):
                _safe_print(f"  result: {e['result']}")
            if e.get("snapshot"):
                _safe_print(f"  snapshot: {e['snapshot']}")
        print()
    if not entries:
        print("No prompt changes logged yet.")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    entries = _load()
    match = next((e for e in entries if e.get("id") == args.id), None)
    if not match:
        raise SystemExit(f"No entry {args.id!r}")
    print(json.dumps(match, indent=2, ensure_ascii=False))
    return 0


def _rebuild(entries: list[dict[str, Any]]) -> None:
    header = """# Prompt Fine-Tuning Changelog

Tracks **what we changed in grader/extractor prompts** and **why**.

This is the research trail for prompt iteration — not a general project diary.

| File | Role |
|------|------|
| `PROMPT_CHANGELOG.md` | Human-readable history (this file; auto-rebuilt from `changes.jsonl`) |
| `changes.jsonl` | Append-only machine ledger |
| `snapshots/` | Frozen copies of prompt files after each logged change |
| `../../scripts/log_prompt_change.py` | CLI to record a change |

## How to log a prompt edit

```powershell
cd scales_v3
python scripts/log_prompt_change.py add `
  --prompt cgr_grading.txt `
  --what "Describe the wording change" `
  --why "What failure / metric motivated it" `
  --evidence "wave / student ids / paths" `
  --result "What improved (optional)"
```

## Rules

- Log **every** intentional prompt edit, even small wording tweaks.
- **Why** must name the failure you saw (student id, wave, metric, or failure mode).
- Do not rewrite old entries — append a correction entry if needed.

---

## History

"""
    blocks: list[str] = [header]
    for e in sorted(entries, key=lambda x: x.get("id", ""), reverse=True):
        day = str(e.get("ts", ""))[:10]
        blocks.append(f"### {e.get('id')} — {day} — `{e.get('prompt_file')}`\n")
        blocks.append(f"**What:** {e.get('what')}\n")
        blocks.append(f"**Why:** {e.get('why')}\n")
        if e.get("evidence"):
            blocks.append(f"**Evidence:** {e['evidence']}\n")
        if e.get("result"):
            blocks.append(f"**Result:** {e['result']}\n")
        if e.get("related_prompts"):
            related = ", ".join(f"`{p}`" for p in e["related_prompts"])
            blocks.append(f"**Also touched:** {related}\n")
        if e.get("snapshot"):
            blocks.append(f"**Snapshot:** `{e['snapshot']}`\n")
        if e.get("sha256_16"):
            blocks.append(f"**File hash (16):** `{e['sha256_16']}`\n")
        blocks.append("")
    CHANGELOG_MD.write_text("\n".join(blocks).rstrip() + "\n", encoding="utf-8")


def cmd_rebuild(_args: argparse.Namespace) -> int:
    entries = _load()
    _rebuild(entries)
    print(f"Rebuilt {CHANGELOG_MD} from {len(entries)} entries")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Log prompt fine-tuning changes (what + why)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Record a prompt change")
    add.add_argument(
        "--prompt",
        required=True,
        help="Prompt filename under config/prompts/ (e.g. cgr_grading.txt)",
    )
    add.add_argument("--what", required=True, help="What wording/instruction changed")
    add.add_argument("--why", required=True, help="Why — failure mode that motivated it")
    add.add_argument("--evidence", default=None, help="Wave / student ids / doc paths")
    add.add_argument("--result", default=None, help="Observed outcome after the change")
    add.add_argument(
        "--related",
        default=None,
        help="Comma-separated other prompt files touched",
    )
    add.add_argument(
        "--no-snapshot",
        action="store_true",
        help="Do not copy prompt file into snapshots/",
    )
    add.add_argument(
        "--no-rebuild",
        action="store_true",
        help="Do not regenerate PROMPT_CHANGELOG.md",
    )
    add.set_defaults(func=cmd_add)

    lst = sub.add_parser("list", help="List logged prompt changes")
    lst.add_argument("--prompt", default=None, help="Filter by prompt filename")
    lst.add_argument("-v", "--verbose", action="store_true")
    lst.set_defaults(func=cmd_list)

    show = sub.add_parser("show", help="Show one entry as JSON")
    show.add_argument("id", help="e.g. PC-003")
    show.set_defaults(func=cmd_show)

    rebuild = sub.add_parser("rebuild", help="Regenerate PROMPT_CHANGELOG.md")
    rebuild.set_defaults(func=cmd_rebuild)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
