#!/usr/bin/env python3
"""Merge claude/settings.hooks.json into a Claude Code settings file.

Adds each hook entry under its event, skips entries already present, and leaves
every other key in the settings file alone. The default target is
~/.claude/settings.json; pass another path as the only argument.

    python3 scripts/merge_hooks.py
    python3 scripts/merge_hooks.py path/to/settings.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
SOURCE = KIT / "claude" / "settings.hooks.json"


def main() -> int:
    ap = argparse.ArgumentParser(description="Merge the kit's hook entries into a Claude Code settings file.")
    ap.add_argument("target", nargs="?", default=str(Path.home() / ".claude" / "settings.json"),
                    help="settings file to update (default: ~/.claude/settings.json)")
    target = Path(ap.parse_args().target).expanduser()
    new_hooks = json.loads(SOURCE.read_text(encoding="utf-8"))["hooks"]
    current = json.loads(target.read_text(encoding="utf-8")) if target.is_file() else {}
    hooks = current.setdefault("hooks", {})
    added = 0
    for event, entries in new_hooks.items():
        existing = hooks.setdefault(event, [])
        for entry in entries:
            if entry not in existing:
                existing.append(entry)
                added += 1
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    print(f"{target}: {added} hook entries added")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
