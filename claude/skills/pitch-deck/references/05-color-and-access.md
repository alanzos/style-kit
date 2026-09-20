# Color and accessibility

Palette architecture, contrast targets, dark against light, and the accessibility pass.

## Color System

A strong deck uses a restrained palette. Build it by role, not by picking colors you like.

### Recommended palette architecture

1. **Background**
   - White or off-white, or
   - Very dark neutral

2. **Primary text**
   - Near black on light backgrounds
   - Near white on dark backgrounds

3. **Secondary neutral**
   - Gray for secondary context

4. **Brand color**
   - Consistent identity

5. **Accent or highlight**
   - Used sparingly for the key insight

6. **Semantic colors**
   - Positive
   - Negative
   - Warning
   - Only when necessary

Tableau recommends using neutral colors for most of a visualization and reserving accent colors for emphasis.

Source:

- https://help.tableau.com/current/blueprint/en-us/bp_visual_best_practices.htm

Tableau also recommends keeping color simple and using it to highlight information rather than decorating every category.

Source:

- https://www.tableau.com/visualization/data-visualization-best-practices

### Implementation view

The same architecture, written as the roles you actually fill in when you set up
a theme:

| Role | Example use |
|---|---|
| Background | White or near-white |
| Primary text | Near-black |
| Secondary text | Medium gray |
| Brand | Company identity |
| Highlight | Key number or selected series |
| Positive | Above plan |
| Negative | Below plan |
| Warning | Risk or attention |

### One color, one meaning

Do not assign multiple meanings to the same color.

For example, if red means "competitor" on one slide, do not use red for "our
growth" on the next slide. The audience carries the first meaning forward and
reads the second slide backwards.

Tableau emphasizes semantic consistency in color.

Source:

- https://help.tableau.com/current/blueprint/en-us/bp_visual_best_practices.htm

### Semantic colors are a named exception to the hue cap

Read the architecture above literally and you get background, text, neutral,
brand, accent and three semantic colors, which is more hue families than the cap
below allows. That is expected. Semantic colors, meaning positive, negative and
warning, are a **named exception** to the cap, not a fourth family to be squeezed
in. Neutrals are free as well.

So count the cap against background, brand and accent, and let positive, negative
and warning sit outside it. Do not spend a hue family on a semantic role, and do
not drop a semantic role to get under the cap.

### Enforced (see SKILL.md)

At most **three hue families** in the deck and at most **three tints inside one
family**; tints of one hue count as one family. Neutrals are free, and the
semantic colors are the named exception described above. Validate with a
contrast checker against both surfaces before shipping, rather than reasoning
about it. The enforced numbers themselves live in `../SKILL.md`.

---

## Contrast and Accessibility

W3C WCAG 2.2 provides widely used contrast targets:

- **4.5:1** for normal text
- **3:1** for large text

Source:

- https://www.w3.org/TR/WCAG22/

WCAG is formally a web-content standard rather than a PowerPoint-specific
standard, so treat it as a borrowed target. The ratios are still the best
available benchmark for slide legibility, and a slide that clears them survives a
bad projector.

### Do not use color alone

W3C recommends ensuring information conveyed by color also has another cue.

Source:

- https://www.w3.org/WAI/WCAG22/Understanding/use-of-color

Add a non-color cue:

- Labels
- Shapes
- Symbols
- Patterns
- Line styles
- Direct annotation

Do not rely only on red against green.

---

## Dark vs Light Decks

### Default: light

Light is the safe default. Dark is a deliberate exception you choose for a
reason you can name.

### Light background

Advantages:

- Reliable on projectors
- Easy to print
- Strong text readability
- Good for data-heavy decks

### Dark background

Advantages:

- Strong visual impact
- Excellent for product imagery
- Works well on modern displays

Risks:

- Thin gray text becomes unreadable
- Charts can become overly decorative
- Projectors may wash out dark colors

### Recommendation

The deciding reason for the light default is projector wash-out, and that reason
is specific to a **projected** deck. A room with an aging projector and ambient
light flattens a dark background into gray mud, and the thin text on top of it
disappears. That is what makes light the default rather than a matter of taste.

Where the deck never meets a projector, the reason weakens. A read-alone PDF, a
screen-shared deck, or a deck shown on a large panel you control can go dark
without paying that cost, so treat those as the named exceptions.

Otherwise choose based on:

- Venue
- Brand
- Product
- Content density

Do not alternate randomly between light and dark slides unless the transition has
a deliberate structural purpose.

### Mixing light and dark in one deck

Inverting the background at a structural boundary is a recognized technique, not
a compromise. A breaker or section slide in reversed polarity gives the audience
a visible seam between parts of the argument. Practitioner sources recommend it,
and some argue a mix keeps a long deck more comfortable to watch than an
unbroken run of either polarity.
([Design Shack](https://designshack.net/articles/business-articles/dark-mode-presentations/),
[pi.inc](https://www.pi.inc/blog/dark-mode-presentation-design),
[PolicyViz](https://policyviz.com/2014/04/03/light-vs-dark-backgrounds/))

The named risk is **not the mixing, it is inconsistency**. A deck where one slide
uses bright white headlines, the next muted gray body text, and a third several
competing accents loses coherence. The audience registers it as a lack of polish
without being able to say why. So the test is systematic, not sparing:

- Does each polarity have its own complete, deliberate palette, or is the dark
  slide just the light slide with the colors flipped?
- Does every inversion sit at a real boundary in the argument?
- How many transitions are there? Two or three reads as structure. Six reads as
  indecision.
- Does every element on the dark ground clear the contrast floor after a weak
  projector lifts the black toward gray? Light text survives that; a mid gray or
  a saturated mid-tone does not. Measure it rather than assuming.

Evidence class: these are practitioner design blogs, which is weaker than the
institutional sources behind the type and contrast rules. Treat the technique as
permitted and useful, not as established.

One naming caution. In presentation literature **"sandwich" means the narrative
structure**, the opening and closing that bracket the body, resting on primacy
and recency
([Spoken with Authority](https://www.spokenwithauthority.com/blog/craft-better-presentations-in-less-time-with-our-sandwich-structure-method)).
It is not a term for a dark-light-dark visual pattern, and no source was found
that uses it that way. Describe the visual pattern as inverted opening and
closing slides instead.

---

## Accessibility

Accessibility improves the deck for everyone.

### Unique slide titles

Harvard recommends unique and descriptive titles.

Source:

- https://accessibility.huit.harvard.edu/microsoft-powerpoint

### Reading order

When sharing a `.pptx`, check that screen-reader reading order is logical.

Microsoft PowerPoint provides accessibility-checking features for this purpose.

Source:

- https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities

### Alt text

Provide useful alt text for meaningful images and diagrams when accessibility is
required.

Source:

- https://accessibility.huit.harvard.edu/microsoft-powerpoint

### Font size floor

Use at least 18 pt as a broad accessibility floor for a live presentation,
and preferably larger.

Source:

- https://accessibility.huit.harvard.edu/microsoft-powerpoint

For a read-alone deck the working floor is 14 pt. That figure is a judgment
about reading a PDF at arm's length, not a Harvard recommendation, so do not cite
it as one. Nothing you prescribe should fall below the floor for its mode. A
source line or a footer set at 12 pt is a defect; it goes to 18 pt in a live deck
and 14 pt in a read-alone deck.

Both floors are minimums, not targets. The type scale for headlines and body text
is the two tables in the Typography section of `04-type-and-layout.md`.

### The contrast and color checks belong here too

The contrast targets and the do-not-use-color-alone rule are part of the
accessibility pass, not a separate concern. Run them from the Contrast and
Accessibility section above rather than restating them here.

Sources:

- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/WAI/WCAG22/Understanding/use-of-color

---
