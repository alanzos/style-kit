# Style kit

Released under CC0 1.0 Universal, see `LICENSE`. Anyone may use, change and share it for any purpose, with no conditions and no attribution.

One master rule file, two skills, and a generator that writes the same rules in the shape each assistant reads: Claude Code, Cursor, ChatGPT and Codex. Edit the master once, run the check script, and every output is regenerated and verified.

## One master, generated copies everywhere else

| Path | What it holds |
| --- | --- |
| `rules/core.md` | The master rule file, with `{{ASSISTANT}}` and `{{USER}}` placeholders. Edit this one. |
| `scripts/build.py` | Reads the master and writes every generated file below. |
| `scripts/check.sh` | Regenerates everything, then runs the prose checker and the leak grep. |
| `scripts/merge_hooks.py` | Adds the two hook entries to a Claude Code settings file. |
| `claude/CLAUDE.md` | Generated. The always-on file for Claude Code, with the markers its hook reads. |
| `claude/hooks/inject-core-rules.py` | Re-injects the Core block next to every prompt. |
| `claude/settings.hooks.json` | The two hook entries, ready to merge into `~/.claude/settings.json`. |
| `claude/skills/writing-style/` | The prose rules, their references, and the checker `scripts/prose_check.py`. |
| `claude/skills/pitch-deck/` | The deck rules, their references, and the audit `scripts/audit_deck.py`. |
| `cursor/rules/*.mdc` | Two always-on Cursor rules: consistent terms and affirmative prose. |
| `cursor/user-rules.md` | Generated. Paste it into Cursor's User Rules box. |
| `chatgpt/AGENTS.md` | Generated. Copy it to `~/.codex/AGENTS.md` and paste it into a ChatGPT Project's instructions box. |
| `chatgpt/custom-instructions.txt` | Generated. The Core as plain text for the custom-instructions box, split into two parts only if it outgrows 1500 characters. |
| `chatgpt/writing-style.md`, `chatgpt/pitch-deck.md` | Generated. Each skill as one file for a ChatGPT Project upload. |
| `scripts/leak.pattern.example` | Template for `scripts/leak.local.pattern`, your private denylist for the leak grep. Git ignores the local file. |

## Claude Code takes the master, the skills and two hooks

1. Save the label you want in the next-step line, then build the outputs. The label file is ignored by git, and both `build.py` and `check.sh` read it.

   ```bash
   echo "Me" > scripts/user.local && python3 scripts/build.py
   ```

2. Copy the always-on file.

   ```bash
   mkdir -p ~/.claude && cp claude/CLAUDE.md ~/.claude/CLAUDE.md
   ```

3. Copy the skills.

   ```bash
   mkdir -p ~/.claude/skills && cp -R claude/skills/* ~/.claude/skills/
   ```

4. Copy the hook.

   ```bash
   mkdir -p ~/.claude/hooks && cp claude/hooks/inject-core-rules.py ~/.claude/hooks/
   ```

5. Merge the hook entries into your settings. The helper adds the two entries and leaves every other key alone.

   ```bash
   python3 scripts/merge_hooks.py
   ```

## Cursor reuses the skills and adds two rules

Do the Claude Code section first: the symlinks below point at the skills it installs.

1. Symlink the skills.

   ```bash
   mkdir -p ~/.cursor/skills && ln -sfn ~/.claude/skills/writing-style ~/.cursor/skills/writing-style && ln -sfn ~/.claude/skills/pitch-deck ~/.cursor/skills/pitch-deck
   ```

2. Copy the rules.

   ```bash
   mkdir -p ~/.cursor/rules && cp cursor/rules/*.mdc ~/.cursor/rules/
   ```

3. Paste `cursor/user-rules.md` into Cursor under Settings, Rules, User Rules. On macOS this command puts the file on the clipboard.

   ```bash
   pbcopy < cursor/user-rules.md
   ```

## ChatGPT and Codex take one file and four uploads

1. Copy the agents file for Codex.

   ```bash
   mkdir -p ~/.codex && cp chatgpt/AGENTS.md ~/.codex/AGENTS.md
   ```

2. In ChatGPT, create a Project and paste `chatgpt/AGENTS.md` into its instructions box.

3. Upload `chatgpt/writing-style.md`, `chatgpt/pitch-deck.md`, `claude/skills/writing-style/scripts/prose_check.py` and `claude/skills/pitch-deck/scripts/audit_deck.py` as project files.

4. Paste `chatgpt/custom-instructions.txt` into the box under Settings, Personalization, Custom instructions. A box accepts 1500 characters, so the file holds the Core alone, and the generator splits it into two labeled parts, one per box, only when the Core outgrows one box.

## Requirements stop at python3 and one optional package

python3 runs everything in the kit. The deck audit also needs python-pptx, installed in a virtual environment so the system python stays untouched.

```bash
python3 -m venv ~/.venv-pptx && ~/.venv-pptx/bin/pip install python-pptx
```

Run the audit with that environment's python.

```bash
~/.venv-pptx/bin/python claude/skills/pitch-deck/scripts/audit_deck.py deck.pptx
```

## Maintenance means editing the source and regenerating

Edit `rules/core.md` or the skills, then run the check script. It regenerates every output, checks the prose, and greps for leaks. Then repeat the copy steps in the three sections above, so the installed copies match.

```bash
bash scripts/check.sh
```

Never edit a generated file: `claude/CLAUDE.md`, `chatgpt/*.md`, `chatgpt/*.txt`, `cursor/user-rules.md`, and the pitch-deck `references/INDEX.md` and `references/_full.md`. The generators overwrite them on the next run.

The prose checker skips the three files that glue a whole skill together: `chatgpt/writing-style.md`, `chatgpt/pitch-deck.md` and the pitch-deck `_full.md`. Every line in them is checked in its source file, and the leak grep still covers them.

The leak grep reads `scripts/leak.local.pattern`, your private list of names that must not appear in the kit. Copy `scripts/leak.pattern.example` to that name and fill it in. Git ignores the local file, and the check script skips the step when it is absent.

## Optional lines cover two personal preferences

- Working on main. If you want it, add this line under Working habits in `rules/core.md`: "Work on main. No branches or worktrees unless asked."
- The Claims discipline section at the end of `rules/core.md` suits founders and anyone who writes about evidence. Delete it if that is not you.
