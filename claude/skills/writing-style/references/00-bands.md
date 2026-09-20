# The measured bands

Every number here is either **SOURCED**, meaning measured from a target corpus,
or **JUDGMENT**, meaning a defensible call made for this style. Do not present a
JUDGMENT band as research.

## The target profile

The bands are anchored on measurements of one published, data-led investigation
that reads well while carrying real numbers. The text is not named here, because
only the measurements carry. Measured across its running copy: Flesch-Kincaid
8.9, Reading Ease 53.8, 12.7 words per sentence, and 2 percent of sentences over
30 words.

For contrast, opinion columns measured alongside it ran 21.6 to 28.3 words per
sentence, with 22 to 37 percent of sentences over 30 words. That is the gap the
bands exist to hold.

## The table

| Band | Value | Gated | Source |
| --- | --- | --- | --- |
| Median words per sentence | 12 to 16 | yes | the corpus measured 12.7 |
| Any single sentence | 30 words | yes, as the share below | JUDGMENT, the tail cap |
| Share of sentences near the cap | 2 percent | yes | the corpus measured 2 percent |
| Sentences per paragraph | 4 | yes | JUDGMENT, the preference is one or two |
| Sentences per bullet | 3 | yes | JUDGMENT, the preference is one or two |
| Words per paragraph | 110 | yes | JUDGMENT |
| Words per table cell | 40 | yes | JUDGMENT |
| Inline bold per document | 4 | yes | JUDGMENT, two to four per memo-length document |
| Flesch Reading Ease | 50 or higher | no, warn | the corpus measured 53.8 |
| Flesch-Kincaid grade | 9 or under | no, warn | the corpus measured 8.9 |

## Why the tail matters more than the average

The averages are the easy half. One 90-word sentence undoes a page of short ones.
A table cell holding a paragraph is worse, because a reader can neither skim it
nor skip it.

This is why the gated bands are a hard sentence cap and a density cap, not just
a mean. A document can sit at a median of 13 words and still be exhausting if 9
percent of its sentences run past 30.

**How the cap is actually gated.** Not absolutely. The gate is the share of
sentences over 30 words, set at 2 percent, which is what the target corpus
measured. An individual over-cap sentence is reported under `--verbose` and does
not fail a run on its own.

A hard zero would be stricter than the source. And saying "cap" while enforcing a
share would be exactly the overstatement these bands exist to catch.

## Why the two readability scores warn rather than gate

Both are a function of sentence length and of vocabulary. Sentence length is
gated hard above. The vocabulary is set by the subject.

A document that has to say `confidence interval`, `heteroscedasticity` or
`idempotent` sits a few tenths above a general-audience grade, however short
its sentences are. Those words have no shorter synonyms. The report prints
syllables per word beside the score so the vocabulary contribution is visible.

Gate what is controlled, warn on what is not.

## The bold budget, and why it is inline only

A memo can carry bold two to four times, unevenly. That budget does not survive
contact with a long technical document.

Bold that opens a paragraph or a bullet, as in `**How.**`, is structure. Bold
inside a sentence is emphasis. Only the second kind competes for attention, so
only the second kind is counted. Measured on a 600-line plan, that distinction
was the difference between 78 uses and 8.

## A stricter alternative, and when to use it

A tighter band exists for spoken and one-page work: mean 10 to 16 words per
sentence, no sentence over 18, Flesch-Kincaid 8 or under, Gunning Fog under 10.
It was measured off a 90-second spoken script.

Use it for an elevator script or a single page that must be read in two minutes. Do not use it for technical documentation. The same source that
defines it records that Reading Ease 70 and syllables per word under 1.5 are
unreachable once required domain terms are in play.
