#!/usr/bin/env python3
"""PostToolUse hook: hold written markdown to the house writing bands.

Reads the hook payload on stdin and runs `prose_check.py` on the file that was
written. Exit 2 with the findings on stderr feeds them back to Claude, which is
the point: the correction happens in the same turn as the mistake.

Which files are ours to hold to the bands is decided by the checker, in one
place. It skips build directories, preserved evidence, anything git ignores, and
anything a project lists in `.prosecheckignore`. This script only asks whether
the payload names a markdown file that exists.

    echo '{"tool_input":{"file_path":"README.md"}}' | python3 hook.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SUFFIXES = {".md", ".markdown"}


def target(payload: dict) -> Path | None:
    response = payload.get("tool_response") or {}
    request = payload.get("tool_input") or {}
    name = response.get("filePath") or request.get("file_path") or ""
    if not name:
        return None
    path = Path(name)
    if path.suffix.lower() not in SUFFIXES or not path.is_file():
        return None
    return path


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return 0
    path = target(payload)
    if path is None:
        return 0

    checker = Path(__file__).with_name("prose_check.py")
    if not checker.is_file():
        return 0
    result = subprocess.run([sys.executable, str(checker), "--files", str(path)],
                            capture_output=True, text=True, cwd=str(path.parent),
                            check=False)
    if result.returncode == 0:
        return 0

    findings = result.stdout.strip() or result.stderr.strip()
    sys.stderr.write(
        f"Writing bands: {path.name} is outside them. Fix it in this turn.\n\n"
        f"{findings}\n\n"
        "The rules and their sources are in the writing-style skill. Run the\n"
        "checker again after fixing. If the band is wrong rather than the prose,\n"
        "say so instead of editing around it.\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
