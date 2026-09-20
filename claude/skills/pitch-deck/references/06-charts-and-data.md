# Charts, data and images

Charts, tables, numbers, screenshots, icons, logos, and how to treat sources, dates and units.

## Graphics: Evidence Before Decoration

Harvard Catalyst recommends supporting headlines with strong visual evidence and avoiding clip art.

Source:

- https://catalyst.harvard.edu/writing-communication-center/visualize-science/slides/

Harvard T.H. Chan recommends high-resolution photos or illustrations and a consistent visual system.

Source:

- https://hsph.harvard.edu/research/health-communication/resources/slide-checklist/

### Strong graphics for pitch decks

- Product screenshots
- Workflow diagrams
- Customer photographs
- Real before/after examples
- Charts
- Maps
- Schematics
- Simple architecture diagrams
- Customer logos
- Annotated documents
- Short demos

### Weak graphics

- Generic handshake photos
- Random "AI brain" stock imagery
- Decorative city skylines
- Clip art
- Icons that repeat the words next to them
- 3D mockups that obscure the actual product

---

## Product Screenshots

A screenshot is only useful if the audience can see the relevant part.

### Recommended method

1. Capture at high resolution.
2. Crop to the relevant workflow.
3. Enlarge the key area.
4. De-emphasize irrelevant UI.
5. Add one or two callouts.
6. Explain the customer outcome.
7. Avoid trying to show the entire product on one slide.

YC specifically discusses the problem of product screenshots forcing text and UI into unreadably small sizes.

Source:

- https://www.ycombinator.com/blog/how-to-design-a-better-pitch-deck

---

## Chart Selection Cheat Sheet

Start with the decision, not with the chart type. MIT Communication Lab recommends selecting a visual form based on the message the audience should extract. So write down the one thing the audience should take away first, then pick the form that carries it. That decision-first framing is the reason this table exists: the left column is the message, not the data.

Tableau similarly notes that tables are better for exact values while visual marks such as bars make comparison easier.

Sources:

- https://mitcommlab.mit.edu/broad/commkit/figure-design/
- https://www.tableau.com/data-insights/reference-library/visual-analytics
- https://www.tableau.com/learn/get-started/desktop-viz-design

| Question | Strong default |
|---|---|
| Compare categories | Horizontal/vertical bar |
| Show trend over time | Line |
| Show growth over time | Line or columns |
| Show exact values | Table |
| Show conversion stages | Funnel only if stages truly narrow; otherwise bars |
| Show retention | Cohort heatmap or retention curves |
| Show composition, for example revenue mix | Stacked bar or area, used with care |
| Show a relationship between two variables | Scatter |
| Show a distribution | Histogram or box plot |
| Show geographic pattern | Map |
| Show competitor attributes | Matrix or table |
| Show unit economics | Waterfall, bridge or simple equation |
| Show TAM/SAM/beachhead | Bottom-up calculation + simple hierarchy |

Tableau provides a broader chart-selection reference.

Source:

- https://www.tableau.com/learn/whitepapers/which-type-chart-or-graph-right-for-you-ungated

---

## Chart Design Rules

### Write the conclusion above the chart

The chart headline is an assertion headline: it states the finding, and the chart then proves it. See `01-narrative.md` for the rule and its sources.

### Highlight one series

Use an accent color for the important series and neutral colors for context.

Tableau recommends restrained color and using emphasis intentionally.

Source:

- https://www.tableau.com/visualization/data-visualization-best-practices

### Direct-label when possible

Datawrapper recommends direct labeling because it reduces the effort required to match a legend to data series.

Sources:

- https://www.datawrapper.de/blog/improved-stacked-column-charts
- https://www.datawrapper.de/blog/10-ways-to-use-fewer-colors-in-your-data-visualizations

### Remove non-essential chart furniture

Reduce:

- Heavy gridlines
- Chart borders
- Background fills
- Excessive tick marks
- Unnecessary decimals
- Redundant legends

Keep only elements necessary to interpret the result.

### Use honest axes

Do not manipulate scale to exaggerate the result.

When a truncated axis is analytically justified, make the scale conspicuous.

Tableau provides guidance on identifying misleading charts and the importance of source integrity.

Source:

- https://www.tableau.com/blog/how-spot-misleading-charts-know-source

### Label units and time periods

Always make clear:

- Currency
- Thousands/millions
- Percentage vs percentage points
- Month/quarter/year
- Cohort period
- Geography

The source line is governed by one rule for the whole reference set: see "Recommended Source Treatment" below.

### Use colorblind-safe design

Datawrapper recommends direct labels and other non-color cues for colorblind accessibility.

Source:

- https://www.datawrapper.de/blog/colorblindness-part2

---

## Tables

Use tables when **exact values matter**.

Examples:

- Pricing tiers
- Competitive features
- Financial assumptions
- Customer segments
- Unit economics

### Size the table in words, not cells

A table is on-slide text, so it is measured the same way the rest of the slide is measured: in words. The enforced word limit for each mode lives in `../SKILL.md`, and header cells count toward it.

A table of roughly six columns by five rows is thirty cells. At two words a cell that is over sixty words, which fails the live limit outright no matter how neatly it is laid out. In practice a live slide holds about three columns by four short rows.

If a table does not fit the word budget for its mode, it does not belong on a main slide. Move it to the appendix and put the single number it supports on the slide instead. A 20-row spreadsheet is always an appendix table.

### Better table design

- Highlight one row or column
- Right-align numbers
- Use consistent units
- Remove most borders
- Use whitespace to create grouping

---

## Numbers, Units and Currency

Startup decks are full of numbers, and inconsistent formatting makes them hard to scan. Pick one system and use it everywhere.

### Pick one number and unit system

Examples:

- $4.2M
- $450k
- $42
- 18%
- 3.4×
- 14 months
- 2.1 years
- 320 ms
- 2.4 kg

Prefer metric and SI units unless the relevant industry or investor audience uses another convention.

Avoid mixing:

- $4,200,000
- $4.2 million
- $4.2M
- 4.2m USD

on adjacent slides. Switching notation between neighboring slides forces the reader to re-anchor on every slide, which is the actual cost of inconsistent formatting.

### Highlight the number that matters

One large number is stronger than six equally weighted KPIs.

Use a metric wall only when the slide's claim is explicitly:

> "The business is strong across multiple dimensions."

---

## Date Formatting

Use one format consistently.

Recommended:

- **21-August-2026**
- **Jul-2026** for monthly charts
- **Q2 2026** for quarters

Avoid mixing:

- 8/21/26
- 21.08.26
- August 21

unless localization requires it. The house default for prose is the ISO form,
2026-08-21, from the writing-style skill. The spelled-out month is a slide-only
exception, because a room reads it faster.

---

## Icons

Use icons to:

- Aid scanning
- Represent repeatable categories
- Replace redundant small labels
- Create simple process diagrams

Do not use icons merely because empty space exists.

### Icons spend the object budget

Each icon in a row counts as one object, both to the eye and to the audit. A row of six icons with six labels is not one graphic: it is twelve objects, and it consumes the whole per-slide object budget on its own. The enforced object count lives in `../SKILL.md`.

So an icon row of more than four items has to change form. Either flatten it into one image, meaning a single grouped or exported graphic, or move it to the appendix. In that case keep the one item that carries the argument on the slide.

### Consistency

Use one icon system:

- Same stroke weight
- Same fill style
- Same corner language
- Same scale

Avoid mixing:

- Outline icons
- 3D icons
- Emojis
- Filled icons
- Clip art

on one slide.

---

## Logos

Customer logos can be persuasive evidence.

Use them only when:

- The company is genuinely a customer, partner, pilot, or design partner as labeled.
- You can explain what the relationship means.
- You have appropriate permission if required.

Do not create a misleading "logo wall" that implies customers when they are merely conversations or prospects.

---

## Recommended Source Treatment

Every external number should contain enough information to audit it. This section owns the source-line rule for the whole reference set.

### One rule, two clauses

1. The source line stays on the slide, set at the floor for the mode: 18 pt on a live deck, 14 pt on a read-alone deck. Do not delete it, and do not shrink it below the floor. A 12 pt source or footer line is a defect.
2. Only overflow provenance moves to the appendix: methodology, full citations, sample sizes, calculation walkthroughs, and anything else that does not fit the one-line form.

On a live projected deck the presenter also says the provenance out loud, so the on-slide line can stay to the short form. It still stays on the slide, because the deck is forwarded after the meeting and the spoken half does not travel with it.

### Examples

For market claims:

> Source: Gartner, 2025; company analysis

For internal metrics:

> Source: Company data, Jul-2026

For calculated metrics:

> Source: Company data; calculated as paid accounts × current ACV

### Practical rule

A source should answer:

- Who produced the data?
- What period?
- What geography?
- Is the number observed or estimated?

Do not use "Source: Internet".

---
