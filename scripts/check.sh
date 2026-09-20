#!/usr/bin/env bash
# Verify the kit end to end. Exit non-zero if any step fails.
#
# Steps, in order:
#   1. regenerate the pitch-deck INDEX.md and _full.md
#   2. regenerate every per-assistant file from rules/core.md
#   3. run the prose checker over every authored markdown file
#   4. run the leak grep over the whole kit
#
# The generators run first so the checks see fresh outputs. The leak grep reads
# its patterns from scripts/leak.local.pattern, one regular expression per line.
# That file is your private denylist, ignored by git; copy it from
# scripts/leak.pattern.example. The step is skipped when the file is absent.
#
#   bash scripts/check.sh

set -u
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$KIT" || exit 1

fail=0
log="$(mktemp)"
trap 'rm -f "$log"' EXIT

report() {
  # report <PASS|FAIL> <name>: print one line, and the log on failure.
  if [ "$1" = PASS ]; then
    echo "PASS  $2"
  else
    echo "FAIL  $2"
    sed 's/^/      /' "$log"
    fail=1
  fi
}

if python3 claude/skills/pitch-deck/scripts/build_index.py > "$log" 2>&1; then
  report PASS "build_index.py regenerates the pitch-deck index"
else
  report FAIL "build_index.py regenerates the pitch-deck index"
fi

if python3 scripts/build.py > "$log" 2>&1; then
  report PASS "build.py regenerates the per-assistant files"
else
  report FAIL "build.py regenerates the per-assistant files"
fi

# The three generated concatenations are skipped: every line in them is checked
# in its source file, and the checker's per-document inline-bold budget cannot
# hold for a dozen files glued together. The leak grep below still covers them.
if find . -name '*.md' \
    -not -path './chatgpt/writing-style.md' \
    -not -path './chatgpt/pitch-deck.md' \
    -not -path './claude/skills/pitch-deck/references/_full.md' -print0 \
    | sort -z \
    | xargs -0 python3 claude/skills/writing-style/scripts/prose_check.py --files > "$log" 2>&1; then
  report PASS "prose checker over every authored markdown file"
else
  report FAIL "prose checker over every authored markdown file"
fi

if [ -f scripts/leak.local.pattern ]; then
  grep -rniE -f scripts/leak.local.pattern . --exclude-dir=.git \
    --include='*.md' --include='*.mdc' --include='*.py' --include='*.json' \
    --include='*.txt' --include='*.sh' > "$log" 2>&1
  status=$?
  if [ "$status" -eq 1 ]; then
    report PASS "leak grep finds nothing"
  else
    report FAIL "leak grep finds nothing"
  fi
else
  echo "SKIP  leak grep: scripts/leak.local.pattern is absent (copy scripts/leak.pattern.example)"
fi

exit "$fail"
