---
name: pitch-deck
description: Build, fix or review an investor pitch deck or any presentation delivered to an audience. Use whenever a .pptx, .potx, .key or slide deck is produced, edited or reviewed, and whenever a deck is criticized for having too much text, poor alignment, weak hierarchy or too many colors. Supplies a source-backed rule set, a house style, and a runnable audit that measures text density, object count, type hierarchy, palette, alignment, overlap and assertion headlines.
---

# Pitch decks

A deck is **spoken by a person and read by an audience at the same time**, which
is the whole problem: the two channels compete. Almost every bad deck is the
speaker's script pasted onto the slides.

This file is everything you need to build one. The `references/` folder holds the
reasoning and the citations, one file per task; read `references/INDEX.md` to
find the right one instead of loading them all.

## First, decide which artifact

A projected deck and an emailed deck are different products. Building one deck
for both jobs is the most common structural mistake, and the audit's thresholds
differ by `--mode` for exactly this reason.

| | Live, projected | Read-alone, emailed |
|---|---|---|
| Slides | about 10 | about 19 to 20 pages |
| Headline | 36 to 54 pt, default 42 | 30 to 44 pt, default 36 |
| Body | 24 to 30 pt, default 24 | 20 to 26 pt, default 22 |
| Labels and chart labels | 18 to 24 pt, default 20 | 16 to 20 pt, default 18 |
| Explanation | speaker notes | one short sentence on the slide |
| Appendix | handed over on request | attached behind the ask |

## The procedure

1. **Write the spine before opening any tool.** One line per slide, the claim
   the slide makes; if a line contains an "and", it is two slides. Read the
   spine back on its own: it must be the argument, not a table of contents,
   because layout cannot rescue a spine that argues nothing.
2. **Check the investor network's own rules first** and let them override
   everything here: required topics, slide cap, time limit, and what may not
   appear on a slide. Valuation is commonly forbidden.
3. **Give each slide one message and one hero object.** The hero is the largest
   thing on the slide. Everything else recedes.
4. **Move every sentence of explanation off the slide.** On a live deck it goes
   into the speaker notes, which are what you say anyway; on a read-alone deck
   there is no speaker, so it goes into the appendix. An emailed PDF carries no
   narration, notes nobody opens are the same as deleting the argument, and
   proof goes to the appendix in both cases.
5. **Emit the numbers from the source of truth into a data file** the build
   script reads. Never retype a figure onto a slide.
6. **Declare the grid and the palette once, as constants.** Every x and every
   width comes from the grid, never a typed offset.
7. **Build.** For `.pptx` write a build script on `python-pptx`, or use a pptx
   skill if one is installed. Hand-rolled geometry is where
   alignment drift and 48-object slides come from, because nothing checks the
   arithmetic.
8. **Charts native rather than drawn**, one axis, direct labels, the deck's own
   palette checked for contrast against **both** the light and the dark surface,
   with a `dataviz` skill's validator if one is installed or a WCAG contrast
   checker otherwise.
9. **Run the audit. Fix every finding. Re-run.**
10. **Render and look at it.** Convert to PDF, then to PNG, and view every page.
    The audit checks geometry, not whether the slide reads well.

## The enforced layer

```bash
python3 scripts/audit_deck.py deck.pptx                     # live deck
python3 scripts/audit_deck.py deck.pptx --mode read         # emailed deck
python3 scripts/audit_deck.py deck.pptx --minutes 5 --skip 11,12
```

It measures words per slide, objects per slide, smallest and largest type, size
contrast, hue families and tints, and near-miss edge alignment. It also flags
off-slide shapes, table columns wider than the slide, text-on-text overlap,
topic-label headlines, duplicate slide titles, centered body text and aspect
ratio. It checks whether the speaker notes can be said inside the time limit,
and it exits non-zero on any failure. `--skip` marks pages that are not projected slides, such as an
appendix: exempt from the projection limits and from the clock.

### Numeric thresholds

Each row is either sourced or marked JUDGMENT. A JUDGMENT row is a call made for
this skill: defensible, but do not present it to anyone as research.

| Check | Live | Read-alone | Source |
|---|---|---|---|
| Words of on-slide text | 40 | 55 | JUDGMENT |
| Visible objects per slide | 6 | 6 | Phillips, below. His only. |
| Type floor | 18 pt | 14 pt | 18 pt: Harvard accessibility. 14 pt: JUDGMENT, **not** Harvard. |
| Largest type on a slide | 36 pt | 30 pt | the bottom of the sourced type scales, `references/04-type-and-layout.md` |
| Size contrast, largest over smallest | 1.8x | 1.8x | JUDGMENT |
| Hue families in the deck | 3 | 3 | JUDGMENT, from Tableau's "accent for emphasis, neutral elsewhere" |
| Tints inside one hue family | 3 | 3 | JUDGMENT |
| Near-miss edge alignment | 0.05 in | 0.05 in | JUDGMENT |
| Speaker notes | fit the clock at 110 wpm | not applicable | JUDGMENT, from the 8 to 12 minute guidance |

The 18 pt floor is the one row with real institutional weight behind it. The 14 pt
read-alone floor is a judgment: Harvard's figure is about type read across a
room, and a read-alone deck is read at desk distance.

### Non-numeric checks

The audit also fails a deck for an off-slide shape, a table whose columns sum
wider than the slide, or text overlapping text. It fails a slide title that is
a bare topic label, two slides with the same title, centered multi-line body
text, and an aspect ratio that is not 16:9.

**16:9 is a strong default, not a requirement.** The reference set names
legitimate exceptions. When one applies, pass the check explicitly rather than
arguing with it: it is the only check in the set that a correct deck can fail.

## The cognitive-load set

From David JP Phillips, "How to avoid death by PowerPoint", TEDxStockholmSalon.
It converges with the YC, MIT and Stanford guidance in `references/01-narrative.md`,
and `references/10-sources.md` grades how much weight each rule can carry. The six-object
figure is Phillips alone, and it is a talk rather than a cited experiment.

1. **One message per slide.** If the slide makes two points it is two slides.
2. **Six objects maximum.** Working memory holds about six objects, which is the
   same budget as one headline, zero to three supporting lines, one visual and
   one optional source line. A group counts as its members, because the eye sees
   the members; a native chart counts as one.
3. **Never make the audience read and listen at once.** Text on the slide and
   speech compete for one channel and neither lands.
4. **Size signals importance.** The most important element is the largest.
5. **Contrast directs the eye.** Dim rather than delete when a slide builds.
6. **Never read your slides aloud.**

## Non-negotiables

- **The headline is the conclusion, not the topic.** "Market" is a label;
  "Every professional already has a network, and none of them can search it"
  is a claim, illustrated in the manner of LinkedIn's 2004 deck. Read only the
  headlines in order: that sequence must be the argument.
- **If something only fits at 12 pt, the slide has too much on it.** The fix is
  never a smaller font: keep the source line at the floor size for the mode, and
  move only the overflow provenance to the appendix. On a live deck you say the
  provenance out loud, so the slide needs less; on a forwardable deck the source
  line is the only provenance the reader gets.
- **One sans-serif family**, with weight and size doing the work.
- **Count hue families, not hex values.** Counting hex values fails any deck with
  a two-tone chart while letting eleven shades of one blue pass as one color.
  Cluster by hue angle, budget the families, then budget the tints inside a
  family separately; neutrals are structure, not color, and do not count.
- **Validate the palette, do not eyeball it.** Use a contrast validator on
  both the light and the dark surface. A hue that passes on white
  can fail on a dark slide.
- **Left-align body text.** Center only covers, hero statements and big metrics.
- **Keep the frame constant and let the content zone vary.** Same headline
  position and size on every slide, different layout beneath it. Frame
  consistency is the credibility signal; zone variety is what stops the deck
  reading as a template.
- **Numbers read from the model, never retyped.**
- **The ask is a milestone story**, not a runway number.
- **No accent line under a title, and no decorative color bar or edge stripe**,
  including header bands, sidebar stripes, and thin accents along a card edge.
  Both read as machine-generated. Use a background tint, a shadow or whitespace.

## Fixing an existing deck

Run the audit first and keep the output. It turns "this looks bad" into a finite
list and tells you whether the fault is density, hierarchy, palette or geometry,
which need different fixes. Then rebuild from the build script rather than
patching the `.pptx`, because patched geometry drifts again on the next edit.

## The words themselves

This skill owns the surface: type, grid, palette, object count, density. The
`writing-style` skill owns the words, and it applies to every headline, body
line, source line and speaker note in the deck.

Where the two overlap they agree. An assertion headline is the same rule as a
claim-first sentence. The two things `writing-style` adds that this audit does
not measure: the banned machine-generated vocabulary, and one name per thing
reused across every slide rather than rotated for variety.

## Reference

`references/INDEX.md` routes to one file per task. Read the index, then read the
one file you need. Do not load the whole set.

`scripts/audit_deck.py` is the audit. `scripts/build_index.py` regenerates the
index and a single-document view after any reference file changes.
