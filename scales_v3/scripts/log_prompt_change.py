#!/usr/bin/env python3
"""Log tuning changes — the research \"screw\" trail.

Every intentional change to prompts, thresholds, code, or metrics should answer:
  WHAT changed, WHY, which SCREW, tighten/loosen, and IF REVERTED what breaks.

Usage (from scales_v3/):

  # Prompt (legacy-compatible)
  python scripts/log_prompt_change.py add `
    --prompt cgr_grading.txt `
    --screw cgr.partial_over_absent `
    --direction loosen `
    --what "Prefer PARTIAL over ABSENT for on-topic paraphrase" `
    --why "Mid answers wiped to ABSENT" `
    --if-reverted "Mid band harsh ABSENT returns; Wave2/3 mid under-score" `
    --tradeoff "May award PARTIAL on thin answers; watch false ACCEPT on LOW" `
    --evidence "wave2 DEFER_DIAGNOSIS; wave3 mid students"

  # Threshold / code / metric
  python scripts/log_prompt_change.py add `
    --kind metric `
    --artifact scripts/metrics_ledger.py `
    --screw metrics.silent_zero `
    --direction measure `
    --what "Count ACCEPT+0 on HIGH-band students" `
    --why "GOOD collapsed to ABSENT then Tier-1 ACCEPT — invisible to false_accept" `
    --if-reverted "Pass bar cannot see Wave4 OS1-style silent zeros" `
    --tradeoff "Only HIGH band; mid ABSENT accepts stay normal"

  python scripts/log_prompt_change.py list -v
  python scripts/log_prompt_change.py show PC-003
  python scripts/log_prompt_change.py screws
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

PROJECT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = PROJECT / "config" / "prompts"
LEDGER = PROMPTS_DIR / "changes.jsonl"
CHANGELOG_MD = PROMPTS_DIR / "PROMPT_CHANGELOG.md"
SNAPSHOTS = PROMPTS_DIR / "snapshots"
SCREWS_MD = PROMPTS_DIR / "SCREWS.md"

KINDS = ("prompt", "settings", "code", "metric", "dataset")
DIRECTIONS = ("tighten", "loosen", "restructure", "measure")


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


def _next_id(entries: list[dict[str, Any]], prefix: str) -> str:
    max_n = 0
    for e in entries:
        eid = str(e.get("id", ""))
        if eid.startswith(f"{prefix}-"):
            try:
                max_n = max(max_n, int(eid.split("-", 1)[1]))
            except ValueError:
                continue
    return f"{prefix}-{max_n + 1:03d}"


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def _resolve_artifact(kind: str, prompt: str | None, artifact: str | None) -> Path:
    if prompt:
        name = Path(prompt).name
        path = PROMPTS_DIR / name
        if not path.exists():
            raise SystemExit(f"Prompt file not found: {path}")
        return path
    if artifact:
        path = Path(artifact)
        if not path.is_absolute():
            path = PROJECT / path
        if not path.exists():
            raise SystemExit(f"Artifact not found: {path}")
        return path
    if kind == "prompt":
        raise SystemExit("Provide --prompt for kind=prompt")
    raise SystemExit("Provide --artifact (path relative to scales_v3/) for non-prompt kinds")


def _snapshot(src: Path, entry_id: str) -> str:
    SNAPSHOTS.mkdir(parents=True, exist_ok=True)
    dest_name = f"{entry_id}_{src.name}"
    dest = SNAPSHOTS / dest_name
    shutil.copy2(src, dest)
    return f"snapshots/{dest_name}"


def _append(entry: dict[str, Any]) -> None:
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _safe_print(text: str) -> None:
    """Avoid Windows cp1252 crashes on arrows / fancy punctuation."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def cmd_add(args: argparse.Namespace) -> int:
    kind = args.kind
    if args.prompt and not args.artifact:
        kind = "prompt"

    src = _resolve_artifact(kind, args.prompt, args.artifact)
    prompt_file = (
        src.name
        if kind == "prompt" and src.parent.resolve() == PROMPTS_DIR.resolve()
        else None
    )
    artifact_rel = (
        str(src.relative_to(PROJECT)).replace("\\", "/")
        if src.is_relative_to(PROJECT)
        else str(src)
    )

    if not args.screw or not args.screw.strip():
        raise SystemExit("--screw is required (short knob name, e.g. cgr.partial_over_absent)")
    if args.direction not in DIRECTIONS:
        raise SystemExit(f"--direction must be one of {DIRECTIONS}")
    if not (args.if_reverted or "").strip():
        raise SystemExit(
            "--if-reverted is required: what happens if we undo this screw turn"
        )

    entries = _load()
    prefix = "PC" if kind == "prompt" else "TC"
    entry_id = _next_id(entries, prefix)
    snap = None if args.no_snapshot else _snapshot(src, entry_id)

    entry: dict[str, Any] = {
        "id": entry_id,
        "ts": _iso(_utc_now()),
        "kind": kind,
        "screw": args.screw.strip(),
        "direction": args.direction,
        "prompt_file": prompt_file or (Path(args.prompt).name if args.prompt else None),
        "artifact": artifact_rel,
        "what": args.what.strip(),
        "why": args.why.strip(),
        "if_reverted": args.if_reverted.strip(),
        "tradeoff": (args.tradeoff or "").strip() or None,
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
        all_entries = _load()
        _rebuild(all_entries)
        _rebuild_screws(all_entries)
    _safe_print(f"Logged {entry_id} [{kind}/{args.direction}] screw={entry['screw']}")
    _safe_print(f"  what: {entry['what']}")
    _safe_print(f"  why:  {entry['why']}")
    _safe_print(f"  if_reverted: {entry['if_reverted']}")
    if entry.get("tradeoff"):
        _safe_print(f"  tradeoff: {entry['tradeoff']}")
    if snap:
        _safe_print(f"  snapshot: {snap}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    entries = _load()
    if args.prompt:
        name = Path(args.prompt).name
        entries = [e for e in entries if e.get("prompt_file") == name]
    if args.screw:
        entries = [e for e in entries if e.get("screw") == args.screw]
    if args.kind:
        entries = [e for e in entries if e.get("kind", "prompt") == args.kind]
    for e in entries:
        day = str(e.get("ts", ""))[:10]
        direction = e.get("direction") or "?"
        screw = e.get("screw") or "(unnamed)"
        kind = e.get("kind", "prompt")
        target = e.get("prompt_file") or e.get("artifact") or "?"
        _safe_print(f"{e.get('id')}  {day}  [{kind}/{direction}]  {screw}")
        _safe_print(f"  target: {target}")
        _safe_print(f"  what: {e.get('what')}")
        _safe_print(f"  why:  {e.get('why')}")
        if args.verbose:
            if e.get("if_reverted"):
                _safe_print(f"  if_reverted: {e['if_reverted']}")
            if e.get("tradeoff"):
                _safe_print(f"  tradeoff: {e['tradeoff']}")
            if e.get("evidence"):
                _safe_print(f"  evidence: {e['evidence']}")
            if e.get("result"):
                _safe_print(f"  result: {e['result']}")
            if e.get("snapshot"):
                _safe_print(f"  snapshot: {e['snapshot']}")
        print()
    if not entries:
        print("No tuning changes logged yet.")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    entries = _load()
    match = next((e for e in entries if e.get("id") == args.id), None)
    if not match:
        raise SystemExit(f"No entry {args.id!r}")
    print(json.dumps(match, indent=2, ensure_ascii=False))
    return 0


def _latest_by_screw(entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for e in entries:
        screw = e.get("screw")
        if not screw:
            continue
        prev = latest.get(screw)
        if prev is None or str(e.get("ts", "")) >= str(prev.get("ts", "")):
            latest[screw] = e
    return latest


def _rebuild_screws(entries: list[dict[str, Any]]) -> None:
    """One-page index: named screws and the last turn on each."""
    latest = _latest_by_screw(entries)
    lines = [
        "# Screws — current knobs",
        "",
        "Named tuning knobs and their **latest** logged turn.",
        "Before you tighten/loosen again, read `if_reverted` on the latest entry.",
        "",
        "Full history: `PROMPT_CHANGELOG.md` / `changes.jsonl`.",
        "",
        "| Screw | Last id | Direction | Kind | What (latest) | If reverted |",
        "|-------|---------|-----------|------|---------------|-------------|",
    ]
    for screw in sorted(latest):
        e = latest[screw]
        what = str(e.get("what", "")).replace("|", "/")
        reverted = str(e.get("if_reverted") or "—").replace("|", "/")
        if len(what) > 60:
            what = what[:57] + "..."
        if len(reverted) > 50:
            reverted = reverted[:47] + "..."
        lines.append(
            f"| `{screw}` | {e.get('id')} | {e.get('direction', '?')} | "
            f"{e.get('kind', 'prompt')} | {what} | {reverted} |"
        )
    if not latest:
        lines.append("| _(none)_ | | | | | |")
    lines.append("")
    lines.append("## History per screw")
    lines.append("")
    by_screw: dict[str, list[dict[str, Any]]] = {}
    for e in entries:
        screw = e.get("screw") or "(unnamed — legacy)"
        by_screw.setdefault(screw, []).append(e)
    for screw in sorted(by_screw):
        lines.append(f"### `{screw}`")
        lines.append("")
        for e in sorted(by_screw[screw], key=lambda x: x.get("ts", "")):
            day = str(e.get("ts", ""))[:10]
            lines.append(
                f"- **{e.get('id')}** ({day}, {e.get('direction', '?')}): "
                f"{e.get('what')}"
            )
            if e.get("if_reverted"):
                lines.append(f"  - if reverted: {e['if_reverted']}")
        lines.append("")
    SCREWS_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _rebuild(entries: list[dict[str, Any]]) -> None:
    header = """# Tuning Changelog (prompts + screws)

Tracks **what** we changed, **why**, which **screw**, **tighten/loosen**, and
**if reverted** what happens. This is the research trail — not a general diary.

| File | Role |
|------|------|
| `PROMPT_CHANGELOG.md` | Human-readable history (this file; auto-rebuilt) |
| `SCREWS.md` | Index of named knobs + latest turn |
| `changes.jsonl` | Append-only machine ledger |
| `snapshots/` | Frozen copies after each logged change |
| `../../scripts/log_prompt_change.py` | CLI |

## How to log a change

```powershell
cd scales_v3
# Prompt
python scripts/log_prompt_change.py add `
  --prompt cgr_grading.txt `
  --screw cgr.partial_over_absent `
  --direction loosen `
  --what "..." `
  --why "..." `
  --if-reverted "..." `
  --tradeoff "..." `
  --evidence "wave / student / metric"

# Code / metric / settings
python scripts/log_prompt_change.py add `
  --kind metric `
  --artifact scripts/metrics_ledger.py `
  --screw metrics.silent_zero `
  --direction measure `
  --what "..." `
  --why "..." `
  --if-reverted "..." `
  --evidence "..."
```

## Directions

| Direction | Meaning |
|-----------|---------|
| `tighten` | Stricter (harder to get credit / more DEFER) |
| `loosen` | Softer (more PARTIAL/ACCEPT) |
| `restructure` | Behavioural redesign (not a simple dial) |
| `measure` | New metric / observability only (no grader change) |

## Rules

- Log **every** intentional prompt, threshold, code, or metric change.
- **Why** must name the failure (student id, wave, metric, failure mode).
- **if-reverted** is mandatory — so the next person knows the cost of undoing.
- Do not rewrite old entries — append a new turn on the same `--screw`.

---

## History

"""
    blocks: list[str] = [header]
    for e in sorted(entries, key=lambda x: x.get("id", ""), reverse=True):
        day = str(e.get("ts", ""))[:10]
        target = e.get("prompt_file") or e.get("artifact") or "?"
        kind = e.get("kind", "prompt")
        direction = e.get("direction") or "?"
        screw = e.get("screw")
        title = f"### {e.get('id')} — {day} — `{target}`"
        if screw:
            title += f" — `{screw}` ({direction})"
        blocks.append(title + "\n")
        blocks.append(f"**Kind:** {kind}  \n**Direction:** {direction}\n")
        if screw:
            blocks.append(f"**Screw:** `{screw}`\n")
        blocks.append(f"**What:** {e.get('what')}\n")
        blocks.append(f"**Why:** {e.get('why')}\n")
        if e.get("if_reverted"):
            blocks.append(f"**If reverted:** {e['if_reverted']}\n")
        if e.get("tradeoff"):
            blocks.append(f"**Tradeoff:** {e['tradeoff']}\n")
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
    _rebuild_screws(entries)
    print(f"Rebuilt {CHANGELOG_MD.name} + {SCREWS_MD.name} from {len(entries)} entries")
    return 0


def cmd_screws(_args: argparse.Namespace) -> int:
    entries = _load()
    latest = _latest_by_screw(entries)
    if not latest:
        legacy = [e for e in entries if not e.get("screw")]
        print(f"No named screws yet ({len(legacy)} legacy entries without --screw).")
        print("Run: python scripts/log_prompt_change.py rebuild")
        return 0
    for screw in sorted(latest):
        e = latest[screw]
        _safe_print(
            f"{screw}  last={e.get('id')}  {e.get('direction')}  {e.get('kind', 'prompt')}"
        )
        _safe_print(f"  what: {e.get('what')}")
        if e.get("if_reverted"):
            _safe_print(f"  if_reverted: {e['if_reverted']}")
        print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Log tuning changes (what / why / screw / if-reverted)",
    )
    sub = p.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Record a tuning change")
    add.add_argument(
        "--kind",
        choices=KINDS,
        default="prompt",
        help="prompt | settings | code | metric | dataset (default: prompt)",
    )
    add.add_argument(
        "--prompt",
        default=None,
        help="Prompt filename under config/prompts/ (e.g. cgr_grading.txt)",
    )
    add.add_argument(
        "--artifact",
        default=None,
        help="Path to changed file relative to scales_v3/ (for settings/code/metric)",
    )
    add.add_argument(
        "--screw",
        required=True,
        help="Short knob name, e.g. cgr.partial_over_absent or cbte.tau",
    )
    add.add_argument(
        "--direction",
        required=True,
        choices=DIRECTIONS,
        help="tighten | loosen | restructure | measure",
    )
    add.add_argument("--what", required=True, help="What changed")
    add.add_argument("--why", required=True, help="Why — failure mode that motivated it")
    add.add_argument(
        "--if-reverted",
        required=True,
        dest="if_reverted",
        help="What happens / fails if we undo this change",
    )
    add.add_argument(
        "--tradeoff",
        default=None,
        help="Cost of this change (what might get worse)",
    )
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
        help="Do not copy file into snapshots/",
    )
    add.add_argument(
        "--no-rebuild",
        action="store_true",
        help="Do not regenerate markdown files",
    )
    add.set_defaults(func=cmd_add)

    lst = sub.add_parser("list", help="List logged changes")
    lst.add_argument("--prompt", default=None, help="Filter by prompt filename")
    lst.add_argument("--screw", default=None, help="Filter by screw name")
    lst.add_argument("--kind", choices=KINDS, default=None)
    lst.add_argument("-v", "--verbose", action="store_true")
    lst.set_defaults(func=cmd_list)

    show = sub.add_parser("show", help="Show one entry as JSON")
    show.add_argument("id", help="e.g. PC-003 or TC-001")
    show.set_defaults(func=cmd_show)

    screws = sub.add_parser("screws", help="Show latest turn per named screw")
    screws.set_defaults(func=cmd_screws)

    rebuild = sub.add_parser("rebuild", help="Regenerate PROMPT_CHANGELOG.md + SCREWS.md")
    rebuild.set_defaults(func=cmd_rebuild)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
