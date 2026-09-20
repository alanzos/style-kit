# Scope, and conflicts with other guides

## Where this applies

Any prose the author writes, or an agent writes for them. Documents, READMEs,
reports, memos, plans and proposals. Commit messages and release notes. Emails,
and answers in conversation.

The always-on core lives in `~/.claude/CLAUDE.md`. It therefore applies to every
session in every project, without this skill being loaded. This skill holds the
full rule set, the provenance and the checker. The two must not disagree, so if
the core is edited, edit here too.

## Where it does not apply

| Not governed | Whose rules win |
| --- | --- |
| Anything on a slide: type, grid, palette, object count, density | The `pitch-deck` skill |
| Scoring keys, rubrics, machine-read formats | Leave them mechanical. Humanizing a scoring key breaks the tooling that reads it |
| Code identifiers and comments | The project's code style, beyond spelling and the dash rule |
| Quoted material | The person who wrote it. Never edit a quotation to fit these rules |
| Preserved evidence: discards, overridden agent output, vendored text | Nobody. It is kept verbatim, and editing it falsifies the record |
| Markdown a project lists in `.prosecheckignore` | Whoever supplied it. Use this for an input: a fixture, a vendored README, a generated report |
| Generated blocks between markers | The generator. Fix the generator or its input, not the output |

## Where this skill and `pitch-deck` overlap

They agree, and each owns one half.

- **The words on a slide** follow this skill: the headline states the claim, one
  message, no machine-generated vocabulary.
- **The surface** follows `pitch-deck`: 16:9, the type scale, the six-object
  budget, the hue-family cap, the words-per-slide cap.

A slide headline is the clearest case of an assertion heading, which is why both
guides state that rule.

## A rule from the parent guide that did not cross

The guide this style descends from forbids filenames in prose: say "the member
list", never `members.csv`.

That rule governs memos written for a reader with no repository. It does not
cross to a code repository. There, `scripts/prose_check.py` is a reference the
reader can open, and hiding it behind a description makes the document worse.

Recorded here so nobody imports it later by mistake. Three other rules from that
guide are project-specific and stay behind:

- Opaque labels in place of real names.
- Its domain vocabulary rules.
- Its fixed currency format.

The currency principle does cross: do not invent precision.

## When a project needs its own copy

A project ships its own style file when that file is itself a deliverable. One
case: a repository a client or an employer will read as evidence of rigor.

In that case the project file is synced from this skill, not written fresh, and
the skill stays the source of truth. Otherwise the project points here and keeps
nothing local.
