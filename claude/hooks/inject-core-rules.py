#!/usr/bin/env python3
"""UserPromptSubmit hook: re-inject the always-on core beside every new prompt.

CLAUDE.md is read once, at session start. By the time a conversation has filled
with file contents it is the oldest thing in the window, and adherence drops.
This hook copies the core block back in next to the newest message, where it
competes on even terms with everything else that just arrived.

The core is read from `~/.claude/CLAUDE.md` between the markers, so there is one
copy of the rules and it is the one copy the hook reads. The master is rules/core.md
in the kit, and this file is regenerated from it. Anything that goes wrong here
exits 0 and stays silent: a style reminder is never worth blocking a prompt.

    echo '{"prompt":"hi"}' | python3 inject-core-rules.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

RULES = Path.home() / ".claude" / "CLAUDE.md"
START = "<!-- core:start -->"
END = "<!-- core:end -->"
PREFACE = (
    "The user's always-on rules, from CLAUDE.md, repeated next to this prompt so "
    "they do not fade as the context fills. They govern the answer you are about "
    "to write."
)
STATUS = Path.home() / ".claude" / "hooks" / "inject-core-rules.last"


def core(text: str) -> str:
    """Return the text between the markers, or an empty string if either is gone."""
    _, marker, rest = text.partition(START)
    if not marker:
        return ""
    body, marker, _ = rest.partition(END)
    if not marker:
        return ""
    return body.strip()


def note(payload: str, size: int) -> None:
    """Overwrite the one-line status file, so the hook can be shown to be running."""
    try:
        session = json.loads(payload).get("session_id", "?")
    except (json.JSONDecodeError, ValueError, AttributeError):
        session = "?"
    try:
        STATUS.write_text(f"{datetime.now().isoformat(timespec='seconds')} "
                          f"session={session} chars={size}\n", encoding="utf-8")
    except OSError:
        pass


def main() -> int:
    try:
        payload = sys.stdin.read()
    except (OSError, UnicodeDecodeError):
        payload = ""
    try:
        body = core(RULES.read_text(encoding="utf-8"))
    except OSError:
        return 0
    if not body:
        return 0
    note(payload, len(body))
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": f"{PREFACE}\n\n{body}",
        }
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
