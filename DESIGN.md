# </Cy> Profile Design System

## Intent

This is Ali Sh's personal GitHub profile, not a product landing page and not an agent dashboard.

It should read as one person with two disciplines:
- software developer
- motion graphics designer

The visual world mixes two things that genuinely belong to that identity:
- pen-tool / easing-curve precision from motion work
- quiet terminal / tooling language from development

The result should feel technical, designed, personal, and a little playful without becoming cyberpunk, gamer UI, or enterprise software.

## Visual language

### Palette

- Transparent plane — GitHub itself is the canvas.
- Tile black: `#050607`
- Raised black: `#090C0F`
- White: `#F4F6F8`
- Muted text: `#929BA5`
- Dim text: `#68727D`
- Cyan accent: `#69C8FF`
- Lime accent: `#8DFF78`

No color gradients.
No full-width filled background panels.
Glow stays tiny and local to nodes/cursors.

### Typography

Direction:
- Heading: Bricolage Grotesque 700
- Utility/accent: Geist Mono 500
- Body: Instrument Sans 400/500

GitHub-hosted SVGs keep system fallbacks because external web fonts are not guaranteed inside README images.

### Composition

The shape language borrows the useful parts of ROG Strix industrial graphics without copying its branding: asymmetrical slash energy, clipped corners, dot-matrix microtexture, and typography placed like part markings.

That gets fused with softer radii so the profile stays personal rather than looking like gaming hardware.

Use an 8px base rhythm, but do not turn the page into a grid of identical cards.

- 16px: tight internal relationships
- 24px: normal gaps/padding
- 32px: major card padding
- 48px: chapter separation

The transparent plane is active composition space.

Black shapes can be:
- large rounded tiles
- docked pills
- half-exposed labels
- overlapping extensions
- compact floating modules

Every overlap must communicate a relationship. Core vs extension, project vs stack, motion vs tooling, live data vs explanation.

### Motion blueprint layer

Use sparse Swiss-style construction lines as a motion-design blueprint, never as a decorative HUD.

They must align to something real:
- Bézier anchors
- control points
- tile edges
- connector intersections
- graph baselines
- pill centers

Hairlines stay faint and should fade naturally into the transparent plane rather than ending as hard random marks.

### Signature motif

The whole page should read like a semi-circuit-board blueprint drawn by someone who also lives in a motion graph editor.

A real cubic Bézier construction with visible anchors/control handles is the recurring motion motif. Thin system buses connect only genuinely related sections. Chipped card edges carry the technical side; soft corners keep the profile human.

Avoid:
- fake orbits
- planets
- hexagons
- fake HUDs
- generic circuit traces
- random code snippets
- decorative lines with no alignment or relationship

### Motion

One coordinated grammar:
- path tracers on real curves
- soft node pulses
- a quiet rotating terminal command
- short entrance fades on the landing

Durations stay calm, roughly 6–12 seconds.
No fast loops.
No constant large movement.
Respect `prefers-reduced-motion`.

## Copy voice

The copy should sound like Ali wrote it after cleaning up the spelling, not like product marketing.

Short, first person, direct, a little casual.

Good:
- “I build native tools, internal software, and systems I actually use.”
- “Rust · GPUI are where I keep ending up.”
- “I built this because screenshot-click guessing got annoying.”
- “I still care way too much about timing, rhythm, hierarchy, and transitions.”

Avoid:
- “selected surface”
- “build close to the machine”
- “design for humans”
- “typed doorway”
- “active systems”
- “deterministic interaction”
- “local ownership where it makes sense”
- generic poetic lines that could belong to anyone

## Deletion test

Every line, node, pill, label, animation, and sentence needs a reason to exist.

If removing it does not hurt hierarchy, identity, relationship, legibility, or motion, remove it.

## Identity

Public name stays **Ali Sh**.

The personal mark is **</Cy>**.

Role line:
**Software developer & motion graphics designer**
