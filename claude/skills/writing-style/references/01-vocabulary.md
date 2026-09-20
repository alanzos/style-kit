# One name per thing

The rule is short: once a thing is named, reuse that name. The reason is that a
reader cannot tell a new word from a new concept. Rotating synonyms for variety
makes a document feel richer to the writer and vaguer to the reader.

This is the rule the checker cannot enforce for you, and it is the one that does
most for a document nobody has read before.

## The method

Do it before polishing sentences, because renaming a concept rewrites every
sentence it appears in.

1. **List the concepts**, not the words. Ten to twenty for most documents.
2. **Give each one word.** Prefer the ordinary one over the abstract one.
3. **Name the neighbor you rejected**, and why it is a different thing or the
   same thing. This is the step people skip, and it is where the value is.
4. **Grep for the rejected words.** A hit is either drift to fix or a genuine
   second concept that needs its own row.
5. **Put the table in the project**, so the next person and the next agent
   inherit it.

## What a finished table looks like

Built on the vocabulary of LinkedIn's 2004 Series B deck, which its founder
published with commentary at
https://www.reidhoffman.org/linkedin-pitch-to-greylock/. The point is not the
words; it is that each row names what it is *not*, and that two rows are a pair
a careless writer would collapse.

| Concept | The word | Not |
| --- | --- | --- |
| The person who has a profile | member | user, customer |
| The link between two members | connection | contact, friend |
| A member's own page | profile | page, CV |
| A paid posting by a company for an open position | job listing | ad, post |

The `member` and `connection` rows are the load-bearing pair. "Contact" can name
either the person or the link, so one careless word would hide which of the two a
sentence means.

## A supplied field name wins over the table

Suppose a data export calls the field `contacts`. The code keeps `contacts`, and
the prose says connection. The two disagree on purpose, and the disagreement is
the lesson.

Renaming someone else's field to match a style guide breaks the code and hides
the join. Write the field name in backticks and the concept in words, and the two
never collide.

## Borrowed words stay borrowed

When a brief, a client or a source uses a particular word, that word is theirs
inside quotation of their material, even if your table rejects it elsewhere.

Worked example: a table can forbid `user` as a word for the person, while the
deck's own phrases "registered users" and "user growth" stay exactly as
written. Rewriting a quotation to match your vocabulary misquotes it.

## Jargon, and the one-line definition

Prefer the ordinary word over the abstract label, even when the code uses the
abstract one. Say `sign-in page`, not `authentication surface`.

Define a term on first use in the body, then use the short form. Do not rely on
an appendix or a glossary for a term the opening paragraph needs. And do not drop
an unexplained count: "every sign-in page a member can reach" beats
`14 surfaces`.
