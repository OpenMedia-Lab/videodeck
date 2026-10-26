# Visual identity

Neutral technical explanation on a warm white canvas. Dark text and fine gray
construction lines keep the mechanism readable; one blue accent identifies the
token and its weighted contributions. The same contributions physically migrate
from expert outputs into the equation, so motion explains the computation.

This small 2D fixture tests deterministic seeking, object continuity and complete
audio. Production art direction still needs its own spatial/material system and
representative motion proof; this fixture is not a template for every shot.

## Colors

- Canvas: `#f7f8fa`
- Ink: `#182027`
- Secondary text: `#52606d`
- Accent: `#1c5bd7`
- Construction line: `#c3cbd4`

## Typography

IBM Plex Sans for labels and Libre Baskerville Italic for mathematical variables,
loaded through local `@font-face` aliases from exact npm dependencies. No font
downloads during rendering. HyperFrames 0.8.198 otherwise maps generic primary
families to Inter and fetches Google Fonts during compilation.

## Motion

One paused GSAP timeline. The routing view becomes a weighted-sum view by moving
the actual two contribution objects into the equation. Headings and explanatory
sentences crossfade over 0.45 seconds while the objects preserve their identity.

## Avoid

- Unmotivated neon, glow or decorative patterns. This fixture uses flat fills;
  production depth may use restrained tonal gradients, highlights and shadows.
- Raw TeX, unreadably small mathematics, or motion unrelated to the mechanism.
- CDN scripts, remote fonts, nondeterministic randomness, timers, or autoplay.
