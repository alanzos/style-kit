---
name: writing-style
description: A house writing style for any prose in any project. Use when drafting, editing or reviewing a document, README, report, memo, commit message, plan, proposal, email or set of release notes, and whenever writing is criticized for being too long, too dense, too formal, hard to read, or for sounding machine-generated. Supplies the hard formatting rules, the voice, a fixed vocabulary method, measured readability bands marked sourced or judgment, and a runnable checker that measures sentence length, paragraph and bullet density, table-cell width, banned vocabulary and readability, and exits non-zero.
---

# Writing style

Write for a peer who is smart, busy and not a specialist in the subject.
The failure this style exists to prevent is prose that is technically correct and
unreadable, and prose that reads as machine-generated.

The mechanical half is enforced by `scripts/prose_check.py`. The judgment half is
below, and it is the half that matters.

## The core, in one screen

If you read nothing else, hold these.

- **One or two ideas per sentence.** If a sentence needs a semicolon to hold
  itself together, it is two sentences. Nothing over 30 words.
- **One or two sentences per paragraph.** Prefer many short beats over a few
  heavy blocks.
- **Claim first, authority second.** "Those three profiles are out, according to the review
  policy", not "under the review policy those three profiles are out".
- **Say what something is.** Keep a negative claim only when the negative is the
  finding.
- **One name per thing.** Once named, reuse the name. Do not rotate synonyms for
  variety; a reader cannot tell a new word from a new concept.
- **Assertion headings.** The heading states the claim, not the topic. If a
  brief already named the document, that name is the title. Headings inside it
  still state claims.
- **Decisions: lay reading, then mechanism, then two alternatives.** Open with
  the sentence a busy peer can hear, then give the mechanism. Then one rejected
  alternative, and one that is still open.
- **Decisions are first person and active.** Write "I rejected X", never
  "X was rejected". When a running step does the work, that step is the
  subject.
- **Say what is not known.** "I did not test this" is stronger than silence.
- **No em dashes, no contractions, American spelling, dates as `2026-08-27`,
  metric units.** Quoted wording is left exactly as it stands.
- **Every external claim carries its source at the claim**, not only in a list at
  the end.
- **If a claim has no source, say so at the claim.**
- **Paraphrase rather than quote.** Quote only when the exact wording is the
  point, such as a contract term or an error message.
- **Never these words:** `delve`, `underscore`, `showcase`, `pivotal`,
  `comprehensive`, `crucial`, `furthermore`, `moreover`, `intricate`,
  `indispensable`, `notably`, `meticulously`, `it is worth noting`,
  `taken together` as filler. Statistical `significant` is fine.
- **No self-praise, no essay closers, no signpost glue.** Not
  `I searched systematically rather than guessing`, not `Note that` as filler,
  not `First... Second...` as scaffolding.

## The procedure

1. **Draft for the argument, not for the word count.** Get the claims down and
   in order.
2. **Read the headings alone.** They must be the argument. If they are a table
   of contents, the structure is wrong and no amount of sentence polishing fixes
   it.
3. **Fix the vocabulary before the sentences.** Name each concept once, in a
   list, and check nothing has two names. See
   `references/01-vocabulary.md`.
4. **Cut the tail.** Find the longest sentences and the widest table cells and
   fix those first. Averages are easy to pass; the tail is what a reader feels.
5. **Run the checker. Fix every finding. Re-run.**
6. **Read it out loud once.** The checker cannot hear a stranded verb or a
   sentence that lands wrong.

## The enforced layer

```bash
python3 scripts/prose_check.py
python3 scripts/prose_check.py --verbose
python3 scripts/prose_check.py --files README.md docs/plan.md
```

With no arguments it finds every markdown file the project owns. Inside a git
repository it asks git, so anything gitignored is skipped without a second list
to maintain. It exits non-zero on a gated band.

It also runs automatically. `scripts/hook.py` is wired as a `PostToolUse` hook
on Write and Edit in `~/.claude/settings.json`. Any markdown file written in any
project is checked, and the findings come straight back so the fix happens in
the same turn. Review or disable it in `/hooks`.

The bands, their values and whether each is sourced or a judgment call are in
`references/00-bands.md`. Do not present a judgment band as research.

What counts as ours to check is decided in one place, inside the checker, so the
hook and the command agree. Exempt:

- **A quotation of 20 words or more** is exempt from the sentence cap. Somebody
  else's sentence is not ours to cut.
- **Preserved material** under a directory named `discarded`, `overrides`,
  `verbatim`, `vendor`, `third_party` or `fixtures`. That text is evidence of
  what was tried or what was wrong, and editing it falsifies the record.
- **Anything git ignores**, and anything a project lists in
  `.prosecheckignore`. That file takes gitignore-style patterns, one per line,
  and exists for markdown that is an input rather than our writing: a supplied
  fixture, a vendored README, a generated report.

A banned word shown inside backticks is a citation, not a use, so a rules table
can quote what it forbids.

## What this does not govern

- **Anything on a slide.** Use the `pitch-deck` skill for slide geometry, type,
  palette and density. This skill governs the words, that one governs the
  surface, and where they overlap they agree.
- **Scoring keys, rubrics and machine-read formats.** Leave those mechanical.
- **Code comments and identifiers**, beyond the spelling and dash rules.

## Reference

`references/INDEX.md` routes to one file per task. Read the index, then the one
file you need.

## Maintenance

This skill is the source of truth, and it is meant to change. When the author
corrects phrasing, structure or voice on any draft:

1. Apply the correction where it was raised.
2. Add or tighten the rule here in the same turn, with a short example if the
   rule is easy to misread.
3. Add a row to the changelog in `references/03-maintenance.md`.
4. If the rule is mechanical, add the check to `scripts/prose_check.py` and run
   it. A rule nobody measures decays.

A project that ships its own copy of the rules or the checker syncs from here.
Three copies of this style already drifted before the skill existed: the numeric
band table survived in full in only one of the four places it appeared.
