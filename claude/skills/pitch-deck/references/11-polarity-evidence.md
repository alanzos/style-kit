# Dark versus light: what the evidence actually says

Scope note. This file exists because the question "is dark mode better for your
eyes" comes up constantly and the honest answer is not the popular one in either
direction. `05-color-and-access.md` gives the practical slide rule. This file
gives the evidence behind it, and the limits of that evidence.

**The headline is the absence of a headline.** There is no meta-analysis, no
preregistered replication and no registered report on display polarity. Roughly
fifteen small studies point in different directions. Anyone who tells you the
science is settled, in either direction, has not read it.

---

## The one result that reframes the whole question

**Equate the light output and the polarity effect disappears.** Buchner, Mayr and
Brandt manipulated polarity and overall display luminance independently. No
positive polarity advantage survived luminance matching. The only surviving effect
was luminance itself: brighter displays produced better performance
([Ergonomics 2009, 52(7):882-886](https://pubmed.ncbi.nlm.nih.gov/19562598/)).

So "light mode is better" is really "more light reaching the eye is better, and a
white background is the usual way to get it". Every downstream finding follows
from that, and it means **screen brightness is the variable, not theme**.

It also kills the familiarity explanation. If the advantage came from a lifetime
of reading dark ink on white paper, it would survive luminance matching. It does
not. The authors themselves infer familiarity is of minor or no relevance, and
note that nobody has manipulated familiarity directly.

---

## The mechanism, and where it stops

A brighter background constricts the pupil, and a smaller pupil suffers less
optical aberration, so the retinal image is sharper.

Measured directly: pupils were **2.09 mm** in light mode against **3.65 mm** in
dark mode, `t(34) = -17.49`, `dz = 2.96`. Illuminance at the eye was **118.4 lux
against 2.7 lux**. Proofreading accuracy `dz = 0.77`, reading rate `dz = 0.68`.
(Piepenbrock, Mayr and Buchner,
[Ergonomics 2014, 57(11)](https://pubmed.ncbi.nlm.nih.gov/25135324/), N = 35,
24-inch LCD at 50 cm, 10 pt Helvetica.)

Three limits on that mechanism, and all three matter more than the effect itself:

1. **It saturates.** The sharpening benefit of a smaller pupil runs out around
   2 to 3 mm, below which diffraction takes over. The light-mode pupil in that
   study was already 2.09 mm, at or past the optimum, and the authors concede a
   slightly dimmer white background might have given a *larger* advantage. So
   "brighter is always sharper" is false, and turning a white background up to
   maximum is not how to exploit it.
2. **It shrinks as type gets larger.** The advantage increases linearly as
   character size decreases, tested at 8, 10, 12 and 14 pt (0.22 to 0.34 degrees
   of visual angle). (Piepenbrock, Mayr and Buchner,
   [Human Factors 2014, 56(5)](https://journals.sagepub.com/doi/10.1177/0018720813515509))
3. **It shrinks with age.** Acuity advantage `d = 2.17` in younger adults but only
   `d = 0.58` in older adults, because intraocular scatter in an older eye partly
   cancels the bright-background benefit. (Piepenbrock et al.,
   [Ergonomics 2013, 56(7)](https://pubmed.ncbi.nlm.nih.gov/23654206/), N = 169,
   acuity `F(1,163) = 69.31`, `eta squared = 0.30`.)

Combine limits 2 and 3 and there is a real conclusion nobody states: **an older
reader looking at large text gains almost nothing from a light theme.**

---

## Performance and eye strain are different questions

This is the finding most often skipped. In the **same** N = 169 study that produced
a `d = 2.17` acuity difference, polarity had **no detectable effect on eye
strain**. Pre-minus-post scores for eyestrain, headache and muscle or back pain
gave exactly one significant test out of eighteen, which the authors treat as
chance. Every other test was `F < 2.97`, `p > 0.09`, `eta squared < 0.02`.

So the honest position: light mode has a modest, replicated performance edge
on threshold tasks, and there is **no good evidence that either theme is better
for eye comfort**. Contrast polarity does not appear among the principal causes of
digital eye strain at all. That literature points at accommodative and binocular
stress and at dry eye, managed through refractive correction, blink behavior,
working distance and breaks. (Sheppard and Wolffsohn,
[BMJ Open Ophthalmology 2018](https://pubmed.ncbi.nlm.nih.gov/29963645/))

---

## Room light: the folk rule is backwards

The belief is that a dark room calls for a dark theme, but tested directly it came
out the other way. Under glance-like reading, the negative-polarity penalty was
**large in near-darkness and statistically absent at 4750 lux**. The statistics:
polarity `F(1,33) = 24.40`, polarity by ambient interaction `F = 14.18`,
within-dark `F = 49.60`, within-bright `F = 0.19`, `p = 0.66`. In the dark
condition, light text on dark cost 28 to 45 percent more viewing time per word
(Dobres, Chahine and Reimer,
[Applied Ergonomics 2017, 60:68-73](https://jdobr.es/pdf/Dobres-etal-2017-Ambient.pdf),
n = 34).

State it the way the authors do: the advantage is large in near-darkness and
shrinks to a non-significant nominal advantage in bright light. The study cannot
distinguish a true absence in the bright condition from insufficient power.

An earlier experiment found the polarity advantage independent of ambient
illumination, so the interaction itself is not settled (Buchner and Baumgartner,
[Ergonomics 2007, 50(7)](https://www.tandfonline.com/doi/abs/10.1080/00140130701306413)).
What is consistent across both: no experiment has found dark mode winning in a
dark room.

Meanwhile **absolute screen luminance does move objective fatigue markers, in a
dose-dependent way**, and ISO 9241 recommends roughly 100 to 150 cd/m2 for a
500 lux office. The polarity studies ran their displays at 328 to 350 cd/m2, two
to three times that. Calibrating brightness is a larger lever than choosing a
theme.

---

## Where dark genuinely wins

- **Cloudy ocular media: cataract, corneal scatter, vitreous opacity.** A bright
  background scatters a veiling luminance across the retina that washes out dark
  letters, so reversing the polarity helps. Direct experimental support exists only
  here (Rubin and Legge, Vision Research 1989, and the Legge low-vision series), as
  an unreplicated single-subject result, so treat it as indicative rather than
  established.
- **Central field loss**, such as macular degeneration: polarity does essentially
  nothing. Do not assume "low vision" implies dark mode.
- **Photophobia and migraine**: the variable is retinal irradiance and spectral
  content, not polarity. Dimming works; inverting is incidental.
- **A red laser pointer** is far more visible on a dark projected background.

## Claims that do not survive checking

- **"Dark mode reduces eye strain."** The largest study that measured eye strain
  found no polarity effect.
- **"Dark mode helps because it cuts blue light."** Changing display spectrum at
  night without changing brightness did not reduce melatonin suppression. The
  predictor is melanopic irradiance, which is mostly brightness.
- **"Half the population has astigmatism, so dark mode is unusable for them."**
  The halation mechanism is real, but the prevalence figures circulated for this
  claim trace to accessibility marketing copy, not to a meta-analysis. No study
  has shown astigmats performing worse in dark mode.
- **"Dark mode helps dyslexic readers."** The evidence there concerns background
  luminance and hue, not polarity, and the visual-stress tradition that generates
  most of these claims has a poor replication record.
- **"WCAG recommends one or the other."** It takes no position. A contrast ratio
  is symmetric: black on white and white on black both compute to 21:1, so the
  number cannot distinguish them.
- **"Offering a dark mode makes a product accessible."** It does not, and shipping
  both is the actual accessibility answer.
- **"Dark mode saves my laptop battery."** OLED savings are real but far smaller
  than marketed at realistic brightness, and most laptops are not OLED anyway.
- **"Dark slides are gentler on an audience's eyes."** Nothing supports this. A
  talk is minutes of reflected light at distance, which is not the situation that
  generates digital eye strain.

## What ambient light does to a projected dark slide

Not what is usually claimed. Stray light landing on the screen adds the same
luminance offset to the white state and the black state, so it compresses system
contrast identically for both polarities. A dark background is not selectively
harmed in contrast-ratio terms.

The real asymmetry is appearance and area. On a dark slide the large area is the
projector's black state, which ambient light lifts into visible gray, so the slide
looks muddy and loses impact. On a light slide the large area is the white state,
which stays far above ambient and still reads as white. Judge it as an appearance
risk, not a legibility one, and check the venue's system contrast with the lights
set as they will be during the talk.

---

## The variables that matter more than the theme

Every one of these outranks polarity, and four of them go unmentioned in most
discussions:

1. **Screen brightness**, calibrated to the room. The dominating lever.
2. **Character size and viewing distance**, that is, visual angle. For projection,
   target roughly 20 arcminutes of character height at the back row.
3. **Session length and breaks.** No polarity study runs longer than about an
   hour, and most run 15 to 50 minutes, so nothing in this literature speaks to
   "long hours" at all. Anyone extrapolating an eight-hour recommendation from
   a 20-minute experiment is inventing it.
4. **Text rendering asymmetry.** The same typeface at the same size renders
   optically bolder on one polarity than the other. This is probably the largest
   uncontrolled variable in every real-world comparison, and it means a fair
   comparison needs a weight adjustment that almost nobody makes.
5. **Mixed-polarity switching.** A dark editor beside a light browser and a light
   PDF forces repeated transient light adaptation all day. That is the actual
   daily situation, and no study has measured it.
6. **Panel reflections.** A glossy screen in a dark theme becomes a mirror, which
   is the most common real-world complaint about dark mode and has nothing to do
   with polarity as such.
7. **Flicker.** PWM dimming on some OLED panels is named as a driver of digital
   eye strain, and it interacts with brightness, which interacts with theme.

## Practical answer by scenario

| Scenario | Lean | Why, and how strongly |
|---|---|---|
| Small text, near acuity limit: dense code, footnotes, a laptop panel | **Light** | Where the measured advantage is largest. Strongest case in the literature. |
| Programming specifically | **Light**, weakly | No direct evidence exists. Code is set at smaller visual angles than prose, so the inference runs toward light, the opposite of what most developers choose. The largest syntax-highlighting experiment found no correctness or time benefit. |
| Long prose reading, large type, large monitor | **Either** | The advantage shrinks with character size. Pick by preference and calibrate brightness instead. |
| Dark room, any screen | **Light text loses here**, contrary to folk belief | Dobres 2017. But lower the brightness: a bright screen in a dark room is the measured problem. |
| Bright room or daylight | **Either** | The polarity effect was not significant at 4750 lux. Glare and reflections dominate. |
| Night, before sleep | **Neither matters** | Reduce absolute brightness. Spectrum alone did not help. |
| Long hours | **Unknown** | Off the end of the evidence base. Manage duration, breaks, blink rate and brightness. |
| Cataract or corneal scatter | **Dark** | The one population with direct support. |
| Projected slides | **Light** | A moderate lean, not a result: no experiment has compared slide polarity at lecture distances. Supported indirectly because dark loses most in a dark room, which is the pitch condition. |
| Any product with users | **Ship both** | The only defensible accessibility answer. |
