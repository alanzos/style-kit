# Type and layout

Text density, the type scale, font choice and compatibility, the grid, alignment, and the reusable layouts they imply.

## Text Density

Harvard T.H. Chan School of Public Health recommends:

- Text used sparingly
- Lists limited to roughly **2-4 items**
- Continuous text blocks limited to roughly **two lines**
- Generous white space
- Headline-oriented slide structure

Source:

- https://hsph.harvard.edu/research/health-communication/resources/slide-checklist/

### Practical default

For live decks:

- 1 headline
- 0-3 short supporting lines
- 1 visual or data display
- 1 source line, at the live floor

For read-alone decks:

- 1 headline
- 1 short explanatory sentence
- 1-3 evidence points
- 1 visual/data element
- 1 source line, at the read-alone floor

### Avoid

- Paragraphs
- 8-12 bullet points
- Full sentences read aloud verbatim
- Text boxes spread randomly around the slide
- Important information hidden in a footnote below the floor for the mode

### Where the explanation goes

Text you cut from a slide still has to live somewhere, and where depends on the mode.

- Live deck: the speaker notes. You are in the room, so you say it out loud.
- Read-alone deck: the appendix. An emailed PDF carries no narration, so notes nobody opens are not a cure.

#### Enforced (see SKILL.md)

At live-deck type sizes the word limit is close to a physical limit anyway: 40
words of on-slide text (JUDGMENT), and at most six visible objects. That object
budget is one headline plus zero to three lines plus one visual. Harvard's
2-to-4-item lists and two-line text blocks are the shape that budget produces.

The audit counts **table cells and chart category labels as on-slide text**,
because a dense table is the commonest place a paragraph hides.

---

## Typography

### Source-backed guidance

Harvard accessibility guidance recommends sans-serif fonts and at least **18 pt** for slide presentations.

Source:

- https://accessibility.huit.harvard.edu/microsoft-powerpoint

Stanford recommends 24 pt or larger sans-serif type for visible presentation slides.

Source:

- https://oralcommprogram.stanford.edu/presentation-and-delivery/visuals-and-powerpoint

Harvard T.H. Chan's slide checklist recommends approximately:

- **28 pt** headline
- **18-24 pt** body

Source:

- https://hsph.harvard.edu/research/health-communication/resources/slide-checklist/

These are institutional minimum/guideline values, not maximums.

They describe type read across a room, so they govern the live table below. That is why the read-alone table can sit below Stanford's 24 pt without contradicting it: an emailed deck is read at arm's length on a screen the reader controls.

### Practical startup-deck typography

The middle column is the range. The right column is the single value to put in the slide master if you do not want to think about it.

#### Live presentation

| Element | Recommended range | Pick these |
|---|---:|---:|
| Hero number | 48-80+ pt | 60-72 pt Bold |
| Main headline | 36-54 pt | 42 pt Semibold |
| Subheadline or supporting heading | 28-36 pt | 28 pt Regular |
| Body | 24-30 pt | 24 pt Regular |
| Labels and chart labels | 18-24 pt | 20 pt Medium |
| Source/footer | 18 pt floor | 18 pt Regular |

#### Sent/read-alone deck

| Element | Recommended range | Pick these |
|---|---:|---:|
| Hero number | 40-64 pt | 48-60 pt Bold |
| Main headline | 30-44 pt | 36 pt Semibold |
| Subheadline or supporting heading | 24-32 pt | 24 pt Regular |
| Body | 20-26 pt | 22 pt Regular |
| Labels and chart labels | 16-20 pt | 18 pt Medium |
| Source/footer | 14 pt floor | 14 pt Regular |

The pick-these values are practical defaults derived from the institutional minimums and live-presentation guidance above. Two notes on them:

- The weights are part of the default: semibold headline, regular body and subheadline, medium labels.
- An older draft of this file used 26 pt for the live subheadline and 12-16 pt for source lines. Both sat below the range or the floor for their mode, so they are raised here: 28 pt and 18 pt live, 14 pt read-alone.

#### Rule

If important information only fits below the floor for the mode, the slide contains too much. Cut the content, do not shrink the type.

#### Enforced (see SKILL.md)

18 pt is a hard floor for a live deck and 14 pt for a read-alone one: the audit
fails on any run below it, including inside tables. The 18 pt live floor is
Harvard accessibility guidance. The 14 pt read-alone floor is a judgment of this
skill, not Harvard.

The audit also fails a slide whose *largest* text is under 36 pt on a live deck, or 30 pt on a read-alone deck, which catches a
slide with no hierarchy at all. And it fails a slide whose largest-to-smallest
ratio is under 1.8x, which catches a slide where everything is the same size and
nothing says what matters.

The source line stays on the slide, set at the floor for the mode. Only overflow
provenance, meaning the full citation, the methodology and the sample sizes,
moves to the appendix. A live projected deck is the one case where the visible
line can go, because the presenter says the provenance out loud.

---

## Font Selection

Microsoft accessibility guidance favors simple, familiar fonts and recommends avoiding overly decorative or difficult-to-read styles.

Source:

- https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities

### Good general choices

#### High compatibility

- Aptos
- Arial
- Calibri
- Segoe UI

#### Common professional choices

- Inter
- Helvetica or Helvetica Neue
- Avenir
- Source Sans
- IBM Plex Sans
- Neue Haas Grotesk
- Similar highly legible sans-serif families

### How many families

One sans-serif family is the default. A second family only with a reason you can say in a sentence, and two is the ceiling. An optional monospace for code or technical identifiers does not spend the second slot.

One family carries the whole deck through weight:

- **Bold/Semibold** for headlines
- **Medium** for labels
- **Regular** for body
- Optional Mono for code and technical identifiers only

### Avoid

- A second family with no reason, and any third family at all (the optional monospace does not count toward the two)
- Ultra-light body type
- Condensed body type
- Excessive italics
- Underlining as decoration
- Decorative script/display fonts
- Large amounts of ALL CAPS

---

## Font Compatibility and Embedding

Microsoft explains that font embedding can preserve layout when recipients do not have a custom font installed. It recommends embedding all characters when others may edit the file.

Source:

- https://support.microsoft.com/en-us/office/benefits-of-embedding-custom-fonts-cb3982aa-ea76-4323-b008-86670f222dbc

### Practical recommendation

For a pitch:

- Keep a version using broadly available fonts.
- If using a custom font in `.pptx`, embed it where licensing permits.
- Always test the deck on a second computer.
- Export a PDF before sending externally.
- Check whether text reflows after export.

---

## Aspect Ratio and Slide Dimensions

Microsoft states that 16:9 widescreen is the default for new PowerPoint presentations and describes widescreen as the best choice for presentations because it provides more slide surface.

Official widescreen dimensions:

- **33.867 x 19.05 cm**
- Aspect ratio: 16:9

Source:

- https://support.microsoft.com/en-US/PowerPoint/change-the-size-of-your-powerpoint-slides

### Recommendation

Treat 16:9 as the strong default, not a requirement. Named exceptions:

- A conference requires 4:3
- A specific venue gives another format
- You are designing a printable document rather than a presentation

Do not resize the deck near the end of the process; changing aspect ratio can cause layout problems.

---

## Layout and Grid

A pitch deck should feel designed as one system.

Standardize:

- Left/right margins
- Top headline position
- Line spacing
- Section spacing
- Font system
- Logo position
- Footer/source style
- Number formatting
- Chart style
- Image corner treatment
- Color meaning

One footer and source style, used on every slide that carries data. The footer zone is reserved because the source line normally stays on the slide, set at the floor for the mode: 18 pt live, 14 pt read-alone. Overflow provenance goes to the appendix. A live projected deck may drop the visible line, because the presenter says the provenance out loud; a read-alone deck keeps it.

### Useful practical grid

For widescreen:

- Outer margin: roughly 5-7% of slide width
- Headline zone: top 15-20%
- Main evidence zone: central 65-75%
- Footer/source zone: bottom 5-10%

These are practical defaults, not official PowerPoint rules.

### White space

Harvard's slide checklist explicitly recommends generous blank space.

Source:

- https://hsph.harvard.edu/research/health-communication/resources/slide-checklist/

White space is not wasted space. It establishes hierarchy.

---

## Alignment

For most Western-language pitch decks:

- Left-align body text
- Use consistent visual edges
- Align charts, labels, and images to the same grid
- Avoid arbitrary centering

Harvard accessibility guidance recommends left alignment where possible because it creates a predictable reading edge.

Source:

- https://accessibility.huit.harvard.edu/microsoft-powerpoint

Center alignment is appropriate for:

- Cover slides
- Short hero statements
- Large metrics

It is weaker for:

- Paragraphs
- Lists
- Multi-line explanations

#### Enforced (see SKILL.md)

Declare the grid once, as constants, and take every x and every width from it. A
hand-typed offset is where drift comes from.

The audit flags any pair of left or top edges **closer than 0.05 in without
being identical**. Near-misses are worse than obvious offsets: two edges 0.03 in
apart look like a mistake, 0.5 in apart looks like a decision.

It also checks that a table's column widths sum to no more than the table's own
width, because a wider sum silently walks the last column off the slide.

One more, from practice: **keep the frame constant and let the content zone
vary.** Same headline position and size on every slide, different layout beneath
it. Consistency in the frame is the credibility signal; variety in the zone is
what stops the deck reading as a template.

---

## Reusable Layouts and the Slide Master

A strong startup deck can usually be built from 7-9 reusable layouts. These are content layouts, not PowerPoint slide masters: the master underneath them is the frame plus one type scale.

| Layout | Use |
|---|---|
| Hero | Cover, vision, major statement |
| Assertion + visual | Problem, solution |
| Assertion + metric | Traction, market |
| Assertion + chart | Growth, financials |
| Product screenshot | Product or workflow |
| Two-column comparison | Competition, before/after |
| Matrix/table | Competition, pricing |
| Team | Founders |
| Ask | Raise + milestones |

This is generally better than creating a unique visual system for every slide.

### The type scale for the master

One scale governs every layout. It is the two tables in the Typography section above, ranges plus pick-these defaults and weights. Set those values once in the master and do not define a per-layout scale.
