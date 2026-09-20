#!/usr/bin/env python3
"""Measure a project's prose against the house writing bands.

The rules and their sources are in `references/` beside this script. This file is
the canonical copy; a project that ships its own copy should sync from here
rather than diverge.

The bands come from a measured corpus, not from taste. The target profile is a
published data-led investigation that scored Flesch-Kincaid 8.9, Reading Ease
53.8, 12.7 words per sentence, and 2 percent of sentences over 30 words. Prose
that reads like that carries argument without becoming a wall.

Averages are easy to pass and hard to feel. The band that does the work is the
tail: one 90-word sentence undoes a page of short ones, and a table cell holding
a paragraph is worse, because a reader cannot skim it or skip it.

The length and readability bands are measured on running prose. Table cells and
checklist rows answer to a word cap instead, because a requirements table is
short by design and averaging its labels in would score a dense document as easy.

Each band is marked SOURCED, meaning measured from the target corpus, or
JUDGMENT, meaning a defensible call made here. Do not present a JUDGMENT band as
research.

    python3 scripts/prose_check.py              # report
    python3 scripts/prose_check.py --verbose    # also print every long sentence
    python3 scripts/prose_check.py --files a.md # check specific files
"""

from __future__ import annotations

import argparse
import re
import subprocess
import statistics as st
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path.cwd()
RULES = "the writing-style skill, references/"   # where this project keeps the rules; the only per-project line
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__",
             ".pytest_cache", ".ruff_cache", ".mypy_cache", "site-packages"}
VERBATIM_DIRS = {"discarded", "overrides", "verbatim", "vendor", "third_party",
                 "fixtures"}
"""Directories holding text that is preserved as evidence rather than authored.

A discarded approach and an overridden agent output are kept to show what was
actually tried and what was actually wrong. Editing either to shorten a sentence
would falsify the record, so the checker leaves them alone.
"""

# --- the bands ---------------------------------------------------------------
MEDIAN_WORDS = (12, 16)   # SOURCED: target corpus measured 12.7
SENTENCE_CAP = 30         # JUDGMENT: the hard tail cap
TAIL_SHARE = 0.02         # SOURCED: target corpus had 2 percent over 30 words
EASE_FLOOR = 50.0         # SOURCED: target corpus 53.8
GRADE_CEIL = 9.0          # SOURCED: target corpus 8.9
CELL_WORDS = 40           # JUDGMENT: a table cell is a label, not a paragraph
PARA_WORDS = 110          # JUDGMENT: past this a paragraph is a wall
PARA_SENTENCES = 4        # JUDGMENT: the house preference is one or two
BULLET_SENTENCES = 3      # JUDGMENT: the house preference is one or two
INLINE_BOLD = 4           # SOURCED: the parent guide says 2 to 4, unevenly

# Words that read as machine-generated. From the house writing style.
TELLS = re.compile(
    r"\b(delve[sd]?|underscore[sd]?|showcas(e|es|ed|ing)|pivotal|comprehensive"
    r"|crucial|furthermore|moreover|intricate|indispensable|meticulous(ly)?"
    r"|it is worth noting|taken together)\b", re.I)
DASHES = re.compile(r"[—–]")
BRITISH = re.compile(
    r"\b(modelling|modelled|behaviour\w*|licence|organis\w+|analyse[sd]?"
    r"|theatre|centre|colour\w*|favour\w*|catalogue|programme|whilst|amongst|grey(?:s|ish|scale)?)\b", re.I)
CONTRACTION = re.compile(
    r"\b(?:[A-Za-z]+n't|(?:it|that|there|what|who|let|we|you|they|he|she|I)"
    r"'(?:s|re|ve|ll|d|m))\b")
# Slash compounds in prose. A path has no spaces, so spaces are the signal.
SLASH = re.compile(r"\b[A-Za-z]{3,} / [A-Za-z]{3,}\b")
# Leading with the authority instead of the claim.
AUTHORITY_FIRST = re.compile(r"^(Under the|Per the|According to the|Following the)\b")
# Signpost glue and self-praise: the two content tells the parent guide names.
GLUE = re.compile(r"^(First|Second|Third|Finally|In conclusion|To summarize)[,.]\s"
                  r"|\bNote that\b|One further point|\bTo be clear\b", re.M)
# Self-praise needs a first-person subject. "sets the value to null rather than
# guessing one" describes the system; "I searched rather than guessing" praises
# the author. Only the second is a tell.
PRAISE = re.compile(
    r"\b(?:I|we)\b[^.!?]{0,60}?(?:rather than guessing|systematically rather than"
    r"|thoroughly researched|exhaustively)"
    r"|as one would expect|it should be noted that", re.I)
# A bare fraction with no stated numerator and denominator.
BARE_FRACTION = re.compile(r"(?<![\w/.\-])\d+\s+/\s+\d+(?![\w/.\-])")
# Bold used as a paragraph or bullet label, which is structure rather than emphasis.
LABEL_BOLD = re.compile(r"^\s*(?:[-*]\s|\d+\.\s)?\*\*[^*]+\*\*[.:]?")
# A heading that names a topic instead of stating a claim.
TOPIC_HEADING = re.compile(
    r"^(overview|introduction|background|summary|details?|notes?|misc\w*"
    r"|considerations?|architecture|approach|results?|conclusion)$", re.I)


def syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(len(re.findall(r"[aeiouy]{1,2}", w)), 1)


@dataclass
class Unit:
    """One measurable piece of a document: a paragraph, a bullet, or a cell.

    A bullet keeps kind "para" so it still counts as running prose for the
    length and readability bands. The flag only changes which sentence cap it
    answers to.
    """
    kind: str
    line: int
    text: str
    bullet: bool = False
    quoted: bool = False
    """True when the unit came from a block quote.

    Somebody else's wording is not ours to edit, so the rules that ask the
    author to rewrite a phrase do not apply to it. The length and readability
    bands still do, because a quotation you chose to include is still text the
    reader has to get through.
    """
    quotable: str = ""
    """`text` with code spans blanked.

    Used by the checks that look for a word being *used*. A contraction shown as
    `don't` in a rules table is a citation, not a use.
    """


WARN_ONLY = {"Flesch-Kincaid grade", "Flesch Reading Ease"}
"""Reported, never gated.

Both scores are a function of sentence length and of vocabulary. Sentence length
is gated hard above. The vocabulary is set by the subject: `confidence
interval`, `heteroscedasticity` and `idempotent` have no shorter synonyms, and a
document that has to use them sits a few tenths of a grade above a
general-audience target however short its sentences are. Gate what is controlled,
warn on what is not, which is the same rule a test suite applies to network
latency.
"""


@dataclass
class Finding:
    band: str
    where: str
    detail: str

    @property
    def gating(self) -> bool:
        return self.band not in WARN_ONLY


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, band: str, where: str, detail: str) -> None:
        self.findings.append(Finding(band, where, detail))


def link_text(match: re.Match) -> str:
    """Keep short link text, collapse a long one to a single token.

    Link text of four words or fewer is being used as prose: "see [the harness
    plan](...)". Anything longer is a citation title, which the eye skims past,
    so counting its words would score a well-sourced paragraph as a wall of
    text.
    """
    inner = match.group(1)
    return inner if len(inner.split()) <= 4 else "source"


def blank_code(text: str) -> str:
    return re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), text)


def clean(text: str) -> str:
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", link_text, text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[*_]{1,3}", "", text)
    return re.sub(r"\s+", " ", text).strip()


def units(path: Path) -> tuple[list[Unit], list[Unit]]:
    """Split a markdown file into prose units and headings.

    Fenced code, HTML comments, table rules, bare link bullets, and generated
    blocks are dropped. A bibliography line is not a sentence, and a finding
    inside a generated block points at a file the author cannot fix.
    """
    prose: list[Unit] = []
    headings: list[Unit] = []
    para: list[tuple[int, str]] = []
    in_code = False
    in_generated = False
    in_front = False
    is_bullet = False
    is_quote = False

    def flush() -> None:
        nonlocal is_bullet, is_quote
        if para:
            joined = " ".join(t for _, t in para)
            prose.append(Unit("para", para[0][0], clean(joined), is_bullet,
                              is_quote, clean(blank_code(joined))))
            para.clear()
        is_bullet = False
        is_quote = False

    for n, raw in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        line = raw.rstrip()
        # A block quote is prose with a marker in front. Strip the marker so the
        # bullets, blank lines and paragraphs inside it are seen as themselves.
        if line.lstrip().startswith(">"):
            line = re.sub(r"^\s*>\s?", "", line)
            is_quote = True
        # YAML frontmatter is machine-read metadata. A skill description is
        # written to be matched, not read, so the prose bands do not apply.
        if n == 1 and line.strip() == "---":
            in_front = True
            continue
        if in_front:
            if line.strip() == "---":
                in_front = False
            continue
        if "BEGIN GENERATED" in line:
            flush()
            in_generated = True
            continue
        if "END GENERATED" in line:
            in_generated = False
            continue
        # Generated blocks are excluded: the wording comes from a log entry, so a
        # finding here would point at a file the author cannot fix.
        if in_generated:
            continue
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.strip().startswith("<!--"):
            continue
        if line.startswith("#"):
            flush()
            headings.append(Unit("heading", n, clean(line.lstrip("# "))))
            continue
        if line.startswith("|"):
            flush()
            if re.match(r"^\|[\s\-:|]+\|$", line.strip()):
                continue
            for cell in line.strip().strip("|").split("|"):
                if cell.strip():
                    prose.append(Unit("cell", n, clean(cell), False, False,
                                      clean(blank_code(cell))))
            continue
        if not line.strip():
            flush()
            continue
        if re.match(r"^\s*(?:[-*]|\d+\.|\[[ xX]\])\s", line):
            flush()
            stripped = re.sub(r"^\s*(?:[-*]|\d+\.|\[[ xX]\])\s*", "", line).strip()
            # A bullet that is only a link is a citation, not prose.
            if re.fullmatch(r"\[[^\]]*\]\([^)]*\)\.?", stripped):
                continue
            is_bullet = True
            para.append((n, stripped))
        else:
            para.append((n, line.strip()))
    flush()
    return prose, headings


def sentences(text: str) -> list[str]:
    # Abbreviations that end in a period but not a sentence, so "see fig. 3 vs.
    # fig. 4" is not split into three sentences, which would inflate both the
    # count and the paragraph band.
    text = re.sub(r"\b(e\.g|i\.e|etc|vs|approx|no|fig|cf|art|para|sec|al)\.",
                  r"\1<DOT>", text, flags=re.I)
    text = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", text)
    # A sentence can end on a closing quote or bracket: `... an LLM call".` The
    # boundary is taken after it, so a quoted question does not merge with the
    # sentence that answers it. Slicing rather than splitting keeps every
    # character, which the quotation check downstream depends on.
    cuts = [0] + [m.end() for m in re.finditer(r"""[.!?]["')\]]*(?=\s)""", text)] + [len(text)]
    out = []
    for a, b in zip(cuts, cuts[1:]):
        part = text[a:b].replace("<DOT>", ".").strip()
        if len(part.split()) >= 3:
            out.append(part)
    return out


QUOTE_EXEMPT_WORDS = 20  # JUDGMENT: a quotation this long is not yours to cut


def quoted_words(sentence: str) -> int:
    """Words inside the longest double-quoted span.

    A sentence built around a long quotation cannot be shortened without
    misquoting, and the house style says quoted wording is left as it stands. So
    the cap exempts it, and the report says how many were exempted rather than
    dropping them silently.
    """
    spans = re.findall(r'"([^"]+)"', sentence)
    return max((len(s.split()) for s in spans), default=0)


def readability(sents: list[str]) -> tuple[float, float, float]:
    """Reading Ease, Flesch-Kincaid grade, and syllables per word."""
    words = [w for s in sents for w in re.findall(r"[A-Za-z][A-Za-z'-]*", s)]
    if not words or not sents:
        return 0.0, 0.0, 0.0
    wps = len(words) / len(sents)
    spw = sum(syllables(w) for w in words) / len(words)
    return (206.835 - 1.015 * wps - 84.6 * spw,
            0.39 * wps + 11.8 * spw - 15.59,
            spw)


def outside_quotes(text: str, pattern: re.Pattern) -> list[str]:
    """Matches that are not inside double quotes.

    Quoted material is somebody else's wording and is left alone, which is the
    rule the house style already states.
    """
    spans = [(m.start(), m.end()) for m in re.finditer(r'"[^"]*"', text)]
    hits = []
    for m in pattern.finditer(text):
        if not any(a <= m.start() < b for a, b in spans):
            hits.append(m.group(0))
    return hits


def check(path: Path, report: Report, verbose: bool) -> dict:
    prose, headings = units(path)
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        rel = path
    sents = [(u, s) for u in prose for s in sentences(u.text)]
    if not sents:
        return {}

    # Length and readability bands are measured on running prose only. A
    # requirements table has short cells by design, and averaging them in would
    # score a dense document as easy because half of it is labels. Cells answer
    # to the cell cap and to the sentence cap instead.
    flowing = [s for u, s in sents if u.kind == "para"]
    lengths = [len(s.split()) for s in flowing]
    over = [(u, s) for u, s in sents if len(s.split()) > SENTENCE_CAP]
    quoted = [(u, s) for u, s in over if quoted_words(s) >= QUOTE_EXEMPT_WORDS]
    long = [(u, s, len(s.split())) for u, s in over
            if quoted_words(s) < QUOTE_EXEMPT_WORDS]
    if not lengths:
        ease = grade = spw = median = 0.0
    else:
        ease, grade, spw = readability(flowing)
        median = st.median(lengths)

    if lengths and median > MEDIAN_WORDS[1]:
        report.add("median words per sentence", f"{rel}",
                   f"{median:.0f}, band is {MEDIAN_WORDS[0]} to {MEDIAN_WORDS[1]}")
    if lengths and ease < EASE_FLOOR:
        report.add("Flesch Reading Ease", f"{rel}", f"{ease:.1f}, floor is {EASE_FLOOR:.0f}")
    if lengths and grade > GRADE_CEIL:
        report.add("Flesch-Kincaid grade", f"{rel}", f"{grade:.1f}, ceiling is {GRADE_CEIL:.0f}")
    share = len(long) / len(sents)
    if share > TAIL_SHARE:
        report.add("sentences over the cap", f"{rel}",
                   f"{len(long)} of {len(sents)} ({share:.1%}), band is {TAIL_SHARE:.0%}")
    for u, s, n in sorted(long, key=lambda x: -x[2]):
        if verbose:
            report.add("sentence over 30 words", f"{rel}:{u.line}", f"{n} words in a {u.kind}: {s}")
    for u, s in quoted:
        if verbose:
            report.add("long quotation, exempt", f"{rel}:{u.line}",
                       f"{len(s.split())} words, {quoted_words(s)} of them quoted")

    for u in prose:
        if u.kind == "cell" and len(u.text.split()) > CELL_WORDS:
            report.add(f"table cell over {CELL_WORDS} words", f"{rel}:{u.line}",
                       f"{len(u.text.split())} words: {u.text[:70]}...")
        for hit in SLASH.findall(u.quotable):
            report.add("slash compound", f"{rel}:{u.line}",
                       f"{hit!r}: write it with \"and\" or \"or\"")
        for m in BARE_FRACTION.finditer(u.quotable):
            report.add("bare fraction", f"{rel}:{u.line}",
                       f"{m.group(0)!r}: say what the numerator and denominator are")
        if u.kind != "para":
            continue
        if len(u.text.split()) > PARA_WORDS:
            report.add(f"paragraph over {PARA_WORDS} words", f"{rel}:{u.line}",
                       f"{len(u.text.split())} words")
        count = len(sentences(u.text))
        cap = BULLET_SENTENCES if u.bullet else PARA_SENTENCES
        if count > cap:
            what = "bullet" if u.bullet else "paragraph"
            report.add(f"{what} over {cap} sentences", f"{rel}:{u.line}",
                       f"{count} sentences: {u.text[:64]}...")
        for s in sentences(u.text):
            if AUTHORITY_FIRST.match(s):
                report.add("authority before the claim", f"{rel}:{u.line}",
                           f"{s[:64]}...")
        run = 0
        for s in sentences(u.text):
            run = run + 1 if re.match(r"^(I|We)\b", s) else 0
            if run >= 3:
                report.add("first person stacked", f"{rel}:{u.line}",
                           f"{run} sentences in a row open with I or We")
                break

    # Document-level checks run with code spans blanked out. A banned word shown
    # as `delve` in a rules table is a citation of the word, not a use of it, and
    # a style guide has to be able to quote what it forbids.
    raw = path.read_text(encoding="utf-8")
    body = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S)
    body = re.sub(r"`[^`\n]*`", lambda m: " " * len(m.group(0)), body)
    for pattern, band in ((TELLS, "machine-generated word"),
                          (DASHES, "en or em dash"),
                          (BRITISH, "British spelling"),
                          (GLUE, "signpost glue"),
                          (PRAISE, "self-praise")):
        for m in pattern.finditer(body):
            report.add(band, f"{rel}:{body[:m.start()].count(chr(10)) + 1}",
                       repr(m.group(0).strip()))

    # Bold that opens a paragraph or a bullet is structure, not emphasis, so only
    # bold used inside a sentence counts against the budget.
    inline = 0
    in_fence = False
    for n, line in enumerate(raw.split("\n"), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or line.startswith(("|", "#")):
            continue
        m = LABEL_BOLD.match(line)
        rest = line[m.end():] if m else line
        for hit in re.findall(r"\*\*[^*]+\*\*", rest):
            inline += 1
            if inline > INLINE_BOLD:
                report.add(f"inline bold over {INLINE_BOLD} in one document",
                           f"{rel}:{n}", f"#{inline}: {hit[:48]}")
    for u in prose:
        if u.quoted:
            continue
        for hit in outside_quotes(u.quotable, CONTRACTION):
            report.add("contraction outside a quote", f"{rel}:{u.line}", repr(hit))
    for h in headings:
        if TOPIC_HEADING.fullmatch(h.text.strip()):
            report.add("topic-label heading", f"{rel}:{h.line}",
                       f"{h.text!r} names a topic; state the claim")

    return {"file": str(rel), "sentences": len(sents), "prose": len(lengths),
            "median": median, "mean": st.mean(lengths) if lengths else 0.0,
            "max": max((n for _, _, n in long), default=0), "over": len(long),
            "quoted": len(quoted), "ease": ease, "grade": grade, "spw": spw}


def repo_root(start: Path) -> Path:
    """The git top level for `start`, or `start` itself if it is not in a repo."""
    result = subprocess.run(["git", "-C", str(start), "rev-parse", "--show-toplevel"],
                            capture_output=True, text=True, check=False)
    return Path(result.stdout.strip()) if result.returncode == 0 else start


def project_excludes(root: Path) -> list[str]:
    """Glob patterns from .prosecheckignore, one per line, # for a comment.

    A project needs a way to say "this markdown is an input, not my writing":
    a supplied fixture, a vendored README, a generated report. Guessing from
    directory names would either miss those or exclude real prose.
    """
    listing = root / ".prosecheckignore"
    if not listing.is_file():
        return []
    return [line.strip() for line in listing.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def git_ignored(path: Path) -> bool:
    """True if git ignores the file or any directory above it.

    `git check-ignore` reports an excluded directory but not the files inside it,
    so each ancestor is asked separately up to the repository root.
    """
    root = repo_root(path.parent)
    if root == path.parent and not (root / ".git").exists():
        return False
    current = path
    while True:
        result = subprocess.run(["git", "-C", str(root), "check-ignore", "-q",
                                 str(current)], capture_output=True, check=False)
        if result.returncode == 0:
            return True
        if current.parent == current or current.parent == root:
            return False
        current = current.parent


def excluded(path: Path, root: Path, patterns: list[str]) -> bool:
    """Whether this file is outside what the bands govern."""
    if SKIP_DIRS & set(path.parts) or VERBATIM_DIRS & set(path.parts):
        return True
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path
    for pattern in patterns:
        stem = pattern.rstrip("/")
        if fnmatch(str(relative), pattern) or fnmatch(str(relative), f"{stem}/*"):
            return True
        if any(fnmatch(part, stem) for part in relative.parts[:-1]):
            return True
    return git_ignored(path)


def discover() -> list[Path]:
    """Every markdown file in this project that is ours to write.

    Inside a git repository, ask git. That excludes anything gitignored, which is
    how a supplied data bundle or a vendored dependency stays out of the report
    without a second list to maintain. Outside one, walk the tree and skip the
    usual build and dependency directories.
    """
    found: set[Path] = set()
    queries = (["git", "ls-files", "-z", "*.md"],
               ["git", "ls-files", "-z", "--others", "--exclude-standard", "*.md"])
    for query in queries:
        result = subprocess.run(query, cwd=ROOT, capture_output=True, text=True,
                                check=False)
        if result.returncode != 0:
            found.clear()
            break
        found |= {ROOT / name for name in result.stdout.split("\0") if name}
    if not found:
        found = {p for p in ROOT.rglob("*.md")
                 if not SKIP_DIRS & set(p.relative_to(ROOT).parts)}
    patterns = project_excludes(ROOT)
    return sorted(p for p in found
                  if p.is_file() and not excluded(p, ROOT, patterns))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true",
                    help="print every sentence over the cap, not just the count")
    ap.add_argument("--files", nargs="*",
                    help="check these files instead of every markdown file")
    args = ap.parse_args()

    if args.files:
        named = [Path(f).resolve() for f in args.files]
        patterns = project_excludes(repo_root(named[0].parent)) if named else []
        paths = [p for p in named
                 if p.is_file() and not excluded(p, repo_root(p.parent), patterns)]
        if not paths:
            # Named files that are all excluded is a silent pass, not an error:
            # the hook points at whatever was written, including inputs.
            return 0
    else:
        paths = [p for p in discover() if p.is_file()]
        if not paths:
            sys.exit("no markdown files found")

    report = Report()
    stats = [s for s in (check(p, report, args.verbose) for p in paths) if s]

    head = (f"{'file':<38}{'sents':>6}{'med':>5}{'mean':>6}{'max':>5}{'>30':>5}"
            f"{'quot':>5}{'syl/w':>7}{'grade':>7}{'ease':>7}")
    print(head)
    print("-" * len(head))
    for s in stats:
        flag = "" if (s["median"] <= MEDIAN_WORDS[1]
                      and s["over"] / s["sentences"] <= TAIL_SHARE) else "  <-"
        print(f"{s['file']:<38}{s['sentences']:>6}{s['median']:>5.0f}{s['mean']:>6.1f}"
              f"{s['max']:>5}{s['over']:>5}{s['quoted']:>5}{s['spw']:>7.2f}"
              f"{s['grade']:>7.1f}{s['ease']:>7.1f}{flag}")

    print("-" * len(head))
    print(f"{'all files':<38}{sum(s['sentences'] for s in stats):>6}{'':>5}{'':>6}"
          f"{max(s['max'] for s in stats):>5}{sum(s['over'] for s in stats):>5}"
          f"{sum(s['quoted'] for s in stats):>5}")
    print(f"\nbands: median {MEDIAN_WORDS[0]}-{MEDIAN_WORDS[1]} words, no sentence over "
          f"{SENTENCE_CAP}, at most {TAIL_SHARE:.0%} near the cap, {PARA_SENTENCES} sentences "
          f"per paragraph, {BULLET_SENTENCES} per bullet, {CELL_WORDS} words per cell, "
          f"{INLINE_BOLD} inline bolds per document")
    print(f"warned, not gated: Ease {EASE_FLOOR:.0f} or higher, grade {GRADE_CEIL:.0f} or under")
    print(f"the rules and their sources: {RULES}")
    print(f"quot: sentences over the cap built around a quotation of "
          f"{QUOTE_EXEMPT_WORDS} words or more, exempt because the wording is not ours to cut")

    def show(title: str, findings: list[Finding]) -> None:
        by_band: dict[str, list[Finding]] = {}
        for f in findings:
            by_band.setdefault(f.band, []).append(f)
        print(f"\n{len(findings)} {title}")
        for band, items in sorted(by_band.items(), key=lambda kv: -len(kv[1])):
            print(f"\n{band}  ({len(items)})")
            for i in items[:40]:
                print(f"  {i.where:<44} {i.detail}")
            if len(items) > 40:
                print(f"  ... and {len(items) - 40} more")

    gating = [f for f in report.findings if f.gating]
    warnings = [f for f in report.findings if not f.gating]
    if warnings:
        show("warnings, reported and not gated", warnings)
    if gating:
        show("findings", gating)
        return 1

    print("\nPASS  every file inside the gated bands")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
