# Visual identity

Neutral technical explanation on a warm white canvas. Dark text and fine gray
construction lines keep the mechanism readable; one blue accent identifies the
token and its weighted contributions. The same contributions physically migrate
from expert outputs into the equation, so motion explains the computation.

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

- Neon, gradients, glow, decorative patterns, or cloud-generated media.
- Raw TeX, unreadably small mathematics, or motion unrelated to the mechanism.
- CDN scripts, remote fonts, nondeterministic randomness, timers, or autoplay.
