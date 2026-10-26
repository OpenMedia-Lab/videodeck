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

Treat narration, screen text and synthesis text as separate layers. Render math
as actual SVG/HTML/math layout; inspect the visible expression against the source.
Weights, tensor dimensions, operations and arrow direction must agree. A convenient
shape morph must not imply that distinct mathematical objects are identical.

Lock accepted claims, narration, formulas and examples when the user requests only
polish. A known source or audio defect outside that scope should be reported with
its effect; do not quietly rewrite the core. If the user authorizes repair, change
the relevant source/voice/timing contract and regenerate only affected outputs.

For mechanical interval checks and canonical subtitle export, read the
[timeline contract](timeline.md). It does not judge the explanation.
