# Source and storyboard

Read the full source and supplied references, including the ending of a reference
video. Use source-platform tools to obtain authorized media: for Xiaohongshu,
check `xhs --help`, then `xhs read URL` and `xhs media URL --output reference.mp4`
when supported. Upgrade an insufficient CLI when authorized; don't silently
substitute a thumbnail or a short preview for the complete reference.

First extract the factual spine: question, initial state, mechanism, result and
limits. Introduce the whole before its parts; track the same token/object/example
across shots so viewers see what changes and why. Preserve the author's terms
(for example Query, Key, Value, Expert, Router), meaningful formulas and numerical
examples. New evidence is distinguishable from the authored source.

Rough storyboard first: each shot records **id, source location, teaching purpose,
canonical narration, visible state/action trigger, camera and connection to the
next shot**. Soundtrack selection then supplies real timing anchors for the
detailed storyboard. A scene change need not coincide with a sentence boundary.
Avoid a sequence of static slides with unrelated decoration.

In the detailed shots, name the viewer's focus, the object's actual change, its
handoff/settle time and the labels or formulas that must stay visible. Reuse the
global design brief; do not repeat its palette/material rules in every scene.

## Visible mathematics

Treat narration, display notation and synthesis text as separate layers. Before
coding, inventory every visible mathematical expression: canonical source meaning,
intended typeset form and all scene/element occurrences, including small labels,
tensor dimensions, axes, captions, closing cards and the cover. Inspect every
occurrence, even with a shared style.

All mathematical notation MUST use real math layout (rendered SVG/HTML or equivalent
explicit subscript/superscript layout). A mathematical `d_model` must display as
the typeset equivalent of `d_{\mathrm{model}}`, not a baseline underscore string;
apply the same distinction
to `W_Q`, `E_i`, powers, fractions and Greek symbols. Preserve literal identifiers
such as `config.d_model` only in explicit code/API context with code typography.
Do not globally rewrite identifiers or remove notation to hide a rendering failure.

Check the inventory against the compiled composition and actual encoded pixels.
Raw TeX/Markdown delimiters, unintended underscores, missing glyphs, renderer error
output or incorrect indices are failures. Source strings, a successful math-renderer
call and correct large equation blocks do not prove the labels rendered. Inspect
native-size crops and intended viewing size; compare weights, dimensions,
operations and arrow direction with the source. A shape morph MUST NOT imply that
distinct mathematical objects are identical.

## Revision scope

Lock accepted claims, narration, formulas, examples, composition and motion when
the user requests only polish; change only the authorized parts. Preserve accepted
transitions under the [art-direction contract](art-direction.md#preserve-transitions).
A known source or audio defect outside that scope should be reported with its
effect; do not quietly rewrite the core. If the user authorizes repair, change
the relevant source/voice/timing contract and regenerate only affected outputs.

For mechanical interval checks and canonical subtitle export, read the
[timeline contract](timeline.md). It does not judge the explanation.
