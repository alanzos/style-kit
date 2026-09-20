# Maintenance

This skill is a living guide. A style that is not updated when it is corrected
stops describing how anyone actually writes.

## The rule

When the author corrects phrasing, structure or voice on any draft:

1. Apply the correction where it was raised.
2. Add or tighten the rule in `SKILL.md`, or in the reference file that owns it,
   **in the same turn**. Not later.
3. Add a row to the changelog below: the date, where the correction came from,
   and what changed.
4. If the rule is mechanical, add the check to `scripts/prose_check.py` and run
   it.

Step 4 is the one that decides whether the rule survives. A rule nobody measures
decays, and the checker is the only part of this skill that cannot be forgotten
in a long conversation.

## Why the changelog is a table and not prose

Because the useful question later is "when did this become a rule, and who said
so". A dated row answers it. A paragraph does not.

## What drift looks like

Before this skill existed the same style lived in three project files and a set
of measured bands. The numeric band table survived in full in exactly one of the
four places it appeared. The later copies kept one row, the sentence cap, and
dropped the readability figures entirely.

That is the failure this skill exists to prevent, and it is the reason a project
copy is synced rather than hand-written.

## Changelog

| Date | Source | Change |
| --- | --- | --- |
| 2026-09-20 | Kit created | Initial rule set. |
