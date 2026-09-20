# Export and QA

What to send, in what format, and the checklist to run before you send it.

## Export and Sharing

### PDF

Microsoft notes that saving as PDF preserves presentation formatting and allows viewing without PowerPoint.

Source:

- https://support.microsoft.com/en-us/powerpoint/training/save-powerpoint-presentations-as-pdf-files

#### Advantages

- Stable layout
- Font consistency
- Easy forwarding
- Easy viewing
- Good for read-alone decks

#### Disadvantages

- No animation
- Harder to edit
- No live product interaction

### PowerPoint

Keep `.pptx` for:

- Live presenting
- Animation
- Editing
- Internal collaboration

### Controlled links

DocSend recommends controlled links when founders want document-level access control and engagement analytics.

Sources:

- https://www.docsend.com/blog/how-to-share-your-pitch-deck-with-investors-without-losing-control-of-your-document/
- https://www.docsend.com/blog/tracking-investor-engagement-pitch-deck/

#### Caveat

The DocSend sources describe DocSend's own product, so treat them as vendor guidance rather than neutral evidence about whether tracking improves fundraising outcomes.

### Where the explanation goes, by mode

A shared deck is read without you in the room, so the mode decides where an
explanation belongs.

- Live deck: the explanation goes in the speaker notes, because you say it out loud.
- Read-alone or forwardable deck: the explanation goes in the appendix. An emailed
  PDF carries no narration, and a deck that gets forwarded must work without the
  founder present, so anything parked in speaker notes nobody will open is lost.

Before sending, decide which deck you are sending. If it is the forwardable one,
move the load-bearing explanation out of the notes and into appendix slides.

---

## File QA Before Sending

There is one list, and it is the checklist below. Run the Technical block of
"Pitch Deck QA Checklist" before every send: it covers export, fonts, links,
hidden material, figure accuracy and file hygiene.

---

## Pitch Deck QA Checklist

### Enforced (see SKILL.md)

The threshold checks in this checklist are the enforced layer. The numbers
themselves live in `../SKILL.md`, and the audit script measures them:
`../scripts/audit_deck.py`. Each enforced tick below is phrased so a script
failure maps to one line.

### Story

- [ ] Company is understandable in one sentence.
- [ ] Strongest proof is not buried.
- [ ] Problem is specific.
- [ ] Customer is clear.
- [ ] Solution shows an outcome.
- [ ] Why-now argument is credible.
- [ ] Market is bottom-up where possible.
- [ ] Product is visible.
- [ ] Traction shows trend and scale.
- [ ] GTM is understandable.
- [ ] Business model explains how money is made.
- [ ] Competition includes alternatives.
- [ ] Differentiation is customer-relevant.
- [ ] Defensibility is more than a label.
- [ ] Team slide explains founder-market fit.
- [ ] Financials are internally consistent.
- [ ] Ask is explicit.
- [ ] Ask is connected to milestones.
- [ ] Vision explains what the company can become.

### Slide structure

- [ ] Each slide has one primary point.
- [ ] Each body slide has a meaningful headline.
- [ ] Headlines form a coherent narrative when read alone.
- [ ] No slide contains multiple unrelated arguments.
- [ ] No essential detail is hidden in footnotes.
- [ ] Dense detail is moved to appendix.
- [ ] Enforced: every slide title is a conclusion, and no two slide titles are identical.
- [ ] Enforced: no slide carries more than 40 words of on-slide text, live, or 55 read-alone.
- [ ] Enforced: no slide carries more than six visible objects.

### Typography

- [ ] One sans-serif family is the default, and two is the ceiling. An optional
      monospace for code or technical identifiers does not spend the second slot.
- [ ] Headline size is consistent, and sizes follow the canonical scale in the
      Typography section of `04-type-and-layout.md`. Do not set a second scale here.
- [ ] Body text is comfortably readable at the distance the deck will be read from.
- [ ] No unnecessary ALL CAPS.
- [ ] No excessive italics.
- [ ] No ultra-light body weights.
- [ ] Enforced: no text below 18 pt live, or 14 pt read-alone. The 18 pt live floor
      is the Harvard accessibility floor; the 14 pt read-alone floor is a judgment
      and is not Harvard's.
- [ ] Enforced: the largest text on every slide is at least 36 pt live, or 30 pt read-alone.
- [ ] Enforced: largest over smallest type on a slide is at least 1.8 times.

### Color

- [ ] Palette is consistent.
- [ ] Accent color is used intentionally.
- [ ] Contrast is strong.
- [ ] Information does not depend only on color.
- [ ] Semantic colors mean the same thing everywhere.
- [ ] Enforced: at most three hue families, and at most three tints inside one
      family. Tints of one hue count as one family. Semantic colors, meaning
      positive, negative and warning, are a named exception to the cap, not a
      fourth family squeezed in.

### Layout and alignment

- [ ] Enforced: no pair of left or top edges closer than 0.05 inch without being identical.

### Charts

- [ ] Chart title states the insight.
- [ ] Correct chart type is used.
- [ ] Units are clear.
- [ ] Dates are clear.
- [ ] A source line is on the slide, set at the mode floor: 18 pt live, 14 pt
      read-alone. Only overflow provenance moves to the appendix. Drop the
      on-slide line only for a live projected deck, where you say the provenance
      out loud.
- [ ] Main series is highlighted.
- [ ] Legends are replaced with direct labels where practical.
- [ ] Gridlines and borders are minimized.
- [ ] Axes are honest.
- [ ] Decimals are not excessive.

### Visuals

- [ ] Screenshots are readable.
- [ ] Product areas are cropped and enlarged.
- [ ] Images are high-resolution.
- [ ] Stock imagery is minimized.
- [ ] Icon style is consistent.
- [ ] Customer relationships are labeled accurately.

### Technical

- [ ] 16:9 unless another format is required. Treat 16:9 as a strong default with
      named exceptions, not a requirement.
- [ ] PDF export has been checked, and the PDF opens correctly.
- [ ] Fonts render correctly, with no missing fonts and no broken characters.
- [ ] No cropped content.
- [ ] No meaning depends on animation.
- [ ] Hyperlinks work.
- [ ] Hidden comments and notes are removed where appropriate, and no speaker
      notes are accidentally exposed.
- [ ] No template placeholders and no "Lorem ipsum".
- [ ] Confidential slides are removed if needed.
- [ ] Correct company name.
- [ ] Correct round amount.
- [ ] Current metrics are used, with no conflicting versions of a metric across slides.
- [ ] Correct dates, and date format is consistent.
- [ ] Correct currency, and currency format is consistent.
- [ ] No old investor names.
- [ ] File name is clean and dated, for example `company-deck-2026-08-21.pdf`.
- [ ] File size is small enough to email.

### Delivery

- [ ] 30-second company explanation is rehearsed.
- [ ] Short deck version is rehearsed.
- [ ] Longer version is rehearsed.
- [ ] Interruptions have been practiced.
- [ ] Key metrics are memorized.
- [ ] Appendix covers predictable objections.
- [ ] Final slide ends with a meaningful proposition.
- [ ] Enforced: the speaker notes fit the time limit at 110 words a minute.

---
