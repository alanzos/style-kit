#!/usr/bin/env python3
"""Audit a .pptx against the thresholds in ../SKILL.md and ../references/.

"Too much text, not aligned, too many colors" are all measurable, so measure
them. Every finding names the slide and the shape so the fix is mechanical.

    python3 audit_deck.py deck.pptx                 # live deck (projected)
    python3 audit_deck.py deck.pptx --mode read     # read-alone deck (emailed)

Thresholds differ by mode because the two artifacts have different jobs. See
../references/02-artifact-and-length.md.

Exit status is 0 when every check passes, 1 otherwise, so it can gate a build.
"""

from __future__ import annotations

import argparse
import colorsys
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    from pptx import Presentation
except ImportError:  # keep --help usable; main() reports the missing dependency
    Presentation = None

EMU_PER_IN = 914400

# Neutrals are structure, not color, and do not count against the hue budget.
NEUTRAL_MAX_CHROMA = 18          # max(R,G,B) - min(R,G,B), 0-255

# A hue "family" is what the eye reads as one color. Counting distinct hex
# values instead would fail any deck with a two-tone chart while letting eleven
# shades of one blue pass as "one color". So count families for the budget and
# count tints within a family separately: more than three tints of one hue is a
# different fault, and it reads as indecision.
HUE_FAMILY_DEG = 22
MAX_TINTS_PER_FAMILY = 3

# Mode-dependent thresholds. Sources in ../SKILL.md, Numeric thresholds.
MODES = {
    # hard floor: Harvard accessibility 18pt / read-alone practical 14pt
    # headline: the largest text on a slide must reach this, or the slide has
    #           no hierarchy at all
    # body: the bottom of the mode's body range in 04-type-and-layout.md. The
    # absolute floor alone let a deck of all-20pt text pass while sitting a
    # whole step below the range the same reference prescribes.
    "live": {"minpt": 18.0, "body": 24.0, "headline": 36.0, "words": 40},
    "read": {"minpt": 14.0, "body": 20.0, "headline": 30.0, "words": 55},
}

# Bare topic labels. A headline that is only one of these is a table-of-contents
# entry, not an assertion. ../references/01-narrative.md, Use Assertion Headlines.
TOPIC_LABELS = {
    "problem", "solution", "product", "market", "go to market", "go-to-market",
    "gtm", "business model", "model", "traction", "team", "financing", "finance",
    "financials", "competition", "competitors", "the ask", "ask", "why now",
    "vision", "roadmap", "milestones", "summary", "overview", "agenda",
    "technology", "tech", "customers", "pricing", "revenue", "use of funds",
    "appendix", "thank you", "questions", "contact", "defensibility", "moat",
}


def is_neutral(rgb) -> bool:
    return max(rgb) - min(rgb) <= NEUTRAL_MAX_CHROMA


def hue_deg(rgb) -> float:
    r, g, b = (c / 255 for c in rgb)
    return colorsys.rgb_to_hsv(r, g, b)[0] * 360


def hue_families(colors) -> list[list]:
    """Greedily cluster hued colors into families by hue angle."""
    fams: list[list] = []
    for c in sorted(colors, key=hue_deg):
        h = hue_deg(c)
        for f in fams:
            d = abs(h - hue_deg(f[0]))
            if min(d, 360 - d) <= HUE_FAMILY_DEG:
                f.append(c)
                break
        else:
            fams.append([c])
    return fams


def hexs(rgb) -> str:
    return "#%02X%02X%02X" % tuple(rgb)


def walk(shapes, depth=0):
    """Yield (shape, depth). Groups are yielded, then descended into."""
    for sh in shapes:
        yield sh, depth
        if sh.shape_type == 6 and hasattr(sh, "shapes"):        # GROUP
            yield from walk(sh.shapes, depth + 1)


def shape_colors(sh) -> list:
    out = []

    def grab(cf):
        try:
            if cf.type is not None and cf.rgb is not None:
                out.append(tuple(cf.rgb))
        except (AttributeError, TypeError, ValueError):
            pass

    try:
        if sh.fill.type == 1:                                    # SOLID
            grab(sh.fill.fore_color)
    except (AttributeError, TypeError, ValueError, NotImplementedError):
        pass
    try:
        grab(sh.line.color)
    except (AttributeError, TypeError, ValueError, NotImplementedError):
        pass
    if sh.has_text_frame:
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                grab(r.font.color)
    return out


def _frame_runs(tf):
    out = []
    for p in tf.paragraphs:
        for r in p.runs:
            if r.text.strip() and r.font.size is not None:
                out.append((r.text.strip(), r.font.size.pt, p.alignment))
    return out


def runs_with_size(sh):
    """(text, pt, align) for every sized run, INCLUDING table cells.

    Table text is the classic place small type hides, so it counts like any
    other text on the slide.
    """
    out = []
    if sh.has_text_frame:
        out += _frame_runs(sh.text_frame)
    if getattr(sh, "has_table", False):
        for row in sh.table.rows:
            for cell in row.cells:
                out += _frame_runs(cell.text_frame)
    return out


def shape_all_text(sh) -> str:
    t = (sh.text_frame.text or "") if sh.has_text_frame else ""
    if getattr(sh, "has_table", False):
        t += " " + " ".join(c.text or ""
                            for row in sh.table.rows for c in row.cells)
    return t.strip()


def rects_overlap(a, b, slack_in=0.02):
    s = slack_in * EMU_PER_IN
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return (min(ax2, bx2) - max(ax1, bx1) > s
            and min(ay2, by2) - max(ay1, by1) > s)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 -]", "", s.lower()).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--mode", choices=("live", "read"), default="live",
                    help="live = projected while someone speaks (default); "
                         "read = emailed and read alone")
    ap.add_argument("--words", type=int, default=None)
    ap.add_argument("--objects", type=int, default=6)
    ap.add_argument("--minpt", type=float, default=None)
    ap.add_argument("--headline", type=float, default=None)
    ap.add_argument("--body", type=float, default=None,
                    help="floor for the slide's dominant text size, which is "
                         "the body. Below the mode's body range even when every "
                         "run clears the absolute floor.")
    ap.add_argument("--accents", type=int, default=3, help="max hue families")
    ap.add_argument("--grid", type=float, default=0.05,
                    help="inches: edges closer than this but unequal are "
                         "near-miss misalignment")
    ap.add_argument("--contrast", type=float, default=1.8,
                    help="min ratio of largest to smallest text on a slide")
    ap.add_argument("--minutes", type=float, default=None,
                    help="hard time limit of the pitch. Checks that the speaker "
                         "notes can actually be said in it.")
    ap.add_argument("--wpm", type=float, default=110.0,
                    help="speaking rate used with --minutes. 110 is a normal "
                         "pitch pace; slower is safer under pressure.")
    ap.add_argument("--skip", default="",
                    help="comma-separated 1-based slide numbers that are NOT "
                         "projected slides, e.g. appendix pages. They are "
                         "exempt from the word, object, type-size and contrast "
                         "limits and from the spoken-time budget. Overlap, "
                         "off-slide, alignment and palette checks still apply.")
    a = ap.parse_args()
    if Presentation is None:
        sys.exit("python-pptx is not installed. Create a virtual environment and install it:\n"
                 "  python3 -m venv ~/.venv-pptx && ~/.venv-pptx/bin/pip install python-pptx\n"
                 "then run this script with ~/.venv-pptx/bin/python")

    d = MODES[a.mode]
    words_max = a.words if a.words is not None else d["words"]
    minpt = a.minpt if a.minpt is not None else d["minpt"]
    head_min = a.headline if a.headline is not None else d["headline"]
    body_min = a.body if a.body is not None else d["body"]
    skip = {int(x) for x in a.skip.split(",") if x.strip()}

    prs = Presentation(a.deck)
    sw, sh_ = prs.slide_width, prs.slide_height
    fails: list[str] = []

    all_colors: Counter = Counter()
    lefts: dict = defaultdict(list)
    tops: dict = defaultdict(list)
    headlines: dict = {}
    notes_words: dict = {}

    ratio = sw / sh_
    print(f"deck        {Path(a.deck).name}")
    print(f"mode        {a.mode}  (min {minpt:g}pt, body >= {body_min:g}pt, "
          f"headline >= {head_min:g}pt, <= {words_max} words, "
          f"<= {a.objects} objects)")
    print(f"slide size  {sw / EMU_PER_IN:.3f} x {sh_ / EMU_PER_IN:.3f} in "
          f"= {ratio:.3f}:1, {len(prs.slides)} slides")
    if abs(ratio - 16 / 9) > 0.02:
        fails.append(f"aspect ratio is {ratio:.3f}:1, not 16:9. "
                     "16:9 widescreen is the strong default.")
    print()
    print(f"{'#':>3} {'objs':>5} {'words':>6} {'minpt':>6} {'body':>6} "
          f"{'maxpt':>6} {'hues':>5}   notes")
    print("-" * 78)

    for idx, slide in enumerate(prs.slides, 1):
        exempt = idx in skip
        objects = 0
        words = 0
        sizes: list[float] = []
        colors: Counter = Counter()
        boxes: list = []
        biggest = (0.0, "")
        chars_at: dict = defaultdict(int)
        notes_ = []

        for sh, depth in walk(slide.shapes):
            if sh.shape_type == 6:
                continue                        # the group is not itself an object
            if depth == 0:
                objects += 1
            t = shape_all_text(sh)
            words += len(t.split())
            for txt, pt, align in runs_with_size(sh):
                sizes.append(pt)
                chars_at[pt] += len(txt)
                if pt > biggest[0]:
                    biggest = (pt, txt)
                # Harvard: left-align body. Centering is for covers, hero
                # statements and large metrics only.
                if align is not None and str(align).startswith("CENTER") \
                        and len(txt.split()) > 12 and pt < head_min:
                    fails.append(f"slide {idx}: centered multi-line body text "
                                 f"({len(txt.split())} words at {pt:g}pt): "
                                 f"{txt[:40]!r}. Left-align body.")
            for c in shape_colors(sh):
                colors[c] += 1
                all_colors[c] += 1

            if sh.left is None or sh.top is None:
                continue
            x1, y1 = sh.left, sh.top
            x2, y2 = x1 + (sh.width or 0), y1 + (sh.height or 0)
            lefts[idx].append((x1, t[:24]))
            tops[idx].append((y1, t[:24]))
            pad = EMU_PER_IN // 100
            if x1 < -pad or y1 < -pad or x2 > sw + pad or y2 > sh_ + pad:
                fails.append(f"slide {idx}: {t[:30]!r} extends off the slide")
            # A table's declared width is not its rendered width: the build tool
            # lays it out from the column widths, so a colW array that sums
            # wider than the shape walks the last column off the slide. The
            # bounds check above cannot see that, so check the sum.
            if getattr(sh, "has_table", False):
                cols = sum(c.width for c in sh.table.columns)
                if cols > (sh.width or 0) + EMU_PER_IN // 50:
                    fails.append(
                        f"slide {idx}: table columns sum to "
                        f"{cols / EMU_PER_IN:.2f} in but the table is "
                        f"{(sh.width or 0) / EMU_PER_IN:.2f} in wide, so the "
                        "last column renders past its shape")
                if x1 + cols > sw + EMU_PER_IN // 50:
                    fails.append(
                        f"slide {idx}: table runs to "
                        f"{(x1 + cols) / EMU_PER_IN:.2f} in on a "
                        f"{sw / EMU_PER_IN:.2f} in slide")
            if t:
                boxes.append((x1, y1, x2, y2, t[:30]))

        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if rects_overlap(boxes[i][:4], boxes[j][:4]):
                    fails.append(f"slide {idx}: text overlaps text: "
                                 f"{boxes[i][4]!r} x {boxes[j][4]!r}")

        try:
            nt = (slide.notes_slide.notes_text_frame.text or "").strip() \
                if slide.has_notes_slide else ""
        except (AttributeError, ValueError):
            nt = ""
        # An appendix is read, not spoken, so a skipped slide's notes do not
        # count against the clock.
        notes_words[idx] = 0 if exempt else len(nt.split())

        hued = {c for c in colors if not is_neutral(c)}
        lo = min(sizes) if sizes else float("nan")
        hi = max(sizes) if sizes else float("nan")

        if words > words_max and not exempt:
            fails.append(f"slide {idx}: {words} words on slide (limit {words_max})")
            notes_.append("WORDY")
        if objects > a.objects and not exempt:
            fails.append(f"slide {idx}: {objects} objects (limit {a.objects})")
            notes_.append("BUSY")
        if sizes and lo < minpt and not exempt:
            fails.append(f"slide {idx}: smallest text is {lo:g} pt "
                         f"(floor {minpt:g}). If it only fits that small, the "
                         "slide has too much on it.")
            notes_.append("SMALL")
        dominant = max(chars_at, key=lambda k: chars_at[k]) if chars_at else None
        if dominant is not None and dominant < body_min and not exempt:
            fails.append(f"slide {idx}: the dominant text size is {dominant:g} pt, "
                         f"below the {a.mode}-deck body floor of {body_min:g} pt. "
                         "Every run clears the absolute floor, but the body is a "
                         "step below its own range.")
            notes_.append("UNDERSIZED")
        if sizes and hi < head_min and not exempt:
            fails.append(f"slide {idx}: largest text is only {hi:g} pt "
                         f"(headline floor {head_min:g}). No hierarchy.")
            notes_.append("FLAT")
        if sizes and lo > 0 and hi / lo < a.contrast and not exempt:
            fails.append(f"slide {idx}: size contrast is only "
                         f"{hi / lo:.2f}x (min {a.contrast}x). Size is how a "
                         "slide says what matters.")
            notes_.append("NOCONTRAST")

        if biggest[1]:
            headlines[idx] = biggest[1]
            if norm(biggest[1]) in TOPIC_LABELS:
                fails.append(f"slide {idx}: headline {biggest[1]!r} is a topic "
                             "label, not an assertion. Make the title the "
                             "conclusion.")
                notes_.append("LABEL")

        print(f"{idx:>3} {objects:>5} {words:>6} {lo:>6.1f} "
              f"{(dominant or float('nan')):>6.1f} {hi:>6.1f} "
              f"{len(hued):>5}   {' '.join(notes_)}")

    # ------------------------------------------------- duplicate slide titles
    seen: dict = defaultdict(list)
    for idx, h in headlines.items():
        seen[norm(h)].append(idx)
    for h, idxs in seen.items():
        if len(idxs) > 1 and h:
            fails.append(f"slides {idxs}: identical headline {h!r}. Slide "
                         "titles must be unique (screen-reader navigation).")

    # ------------------------------------------------------------- alignment
    print()
    print(f"alignment (edges within {a.grid:.2f} in of each other but unequal)")
    tol = int(a.grid * EMU_PER_IN)
    near = 0
    for axis, table in (("left", lefts), ("top", tops)):
        for idx, entries in table.items():
            vals = sorted(entries)
            for i in range(len(vals) - 1):
                gap = vals[i + 1][0] - vals[i][0]
                if 0 < gap <= tol:
                    near += 1
                    fails.append(
                        f"slide {idx}: {axis} edges differ by "
                        f"{gap / EMU_PER_IN:.3f} in: "
                        f"{vals[i][1]!r} vs {vals[i + 1][1]!r}")
    print(f"  {near} near-miss edge pairs")

    # ------------------------------------------------------------ spoken time
    # A slide's argument belongs in the notes, so the notes are the script. If
    # they do not fit the clock, the deck does not fit the clock either, and the
    # moderator cuts you off mid-sentence.
    total_notes = sum(notes_words.values())
    print()
    if total_notes:
        mins = total_notes / a.wpm
        print(f"speaker notes: {total_notes} words = {mins:.2f} min at "
              f"{a.wpm:g} wpm")
        empty = [i for i in range(1, len(prs.slides) + 1)
                 if not notes_words.get(i) and i not in skip]
        if empty:
            print(f"  slides with no notes: {empty}")
        if a.minutes is not None:
            budget = a.minutes * a.wpm
            if total_notes > budget:
                fails.append(
                    f"speaker notes are {total_notes} words = {mins:.2f} min at "
                    f"{a.wpm:g} wpm, over the {a.minutes:g} min limit "
                    f"({int(budget)} words). Cut {total_notes - int(budget)} words.")
            else:
                print(f"  fits {a.minutes:g} min with "
                      f"{int(budget) - total_notes} words spare")
    else:
        print("speaker notes: none. The argument has nowhere to live except "
              "the slides.")

    # --------------------------------------------------------------- palette
    hued_all = {c: n for c, n in all_colors.items() if not is_neutral(c)}
    neut_all = {c: n for c, n in all_colors.items() if is_neutral(c)}
    fams = hue_families(hued_all.keys())
    print()
    print(f"palette: {len(fams)} hue families ({len(hued_all)} tints), "
          f"{len(neut_all)} neutrals")
    for f in sorted(fams, key=lambda f: -sum(hued_all[c] for c in f)):
        tot = sum(hued_all[c] for c in f)
        print(f"  family @ {hue_deg(f[0]):3.0f}deg  x{tot:<5} {len(f)} tint(s): "
              + " ".join(hexs(c) for c in f))
        if len(f) > MAX_TINTS_PER_FAMILY:
            fails.append(f"palette: {len(f)} tints of one hue "
                         f"(limit {MAX_TINTS_PER_FAMILY}): "
                         + ", ".join(hexs(c) for c in f)
                         + ". Many shades of one color reads as indecision.")
    for c, n in sorted(neut_all.items(), key=lambda kv: -kv[1]):
        print(f"  neutral      x{n:<5} {hexs(c)}")
    if len(fams) > a.accents:
        fails.append(f"palette: {len(fams)} hue families (limit {a.accents}): "
                     + ", ".join(hexs(f[0]) for f in fams))

    # --------------------------------------------------------------- verdict
    print()
    if fails:
        print(f"FAIL  {len(fails)} findings")
        for f in fails:
            print("  - " + f)
    else:
        print("PASS  every check")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
