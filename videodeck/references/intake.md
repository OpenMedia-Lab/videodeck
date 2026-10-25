# Intake and project memory

Use the current request, prior answers for this project and explicitly established
standing preferences. A previous article's settings are not automatically defaults.

Resolve only missing choices that materially affect production:

| Choice | What to establish |
| --- | --- |
| Goal and audience | What viewers should understand or do; assumed knowledge and omissions |
| Source | Complete article/material/script; factual authority and allowed new writing |
| Destination | Platform, aspect ratio, length strategy; delivery and visibility per platform |
| Direction | Reference or accepted style; important dislikes; allow the agent to propose aesthetics |
| Sound | Narration/language, voice selection or reuse; music and effects direction |

Use an interactive tool such as `request_user_input_async`; `request_user_input`
only when available in the current mode. Bundle related choices into a short
questionnaire, showing recognizable options. If no interactive tool exists, explain
that limitation, ask in text and keep dependent work paused. An unanswered
recommended option is still unanswered. Read sources, inspect references and check
tools while awaiting answers. Do not repeatedly ask settled questions.

Creative detail can be resolved through actual auditions and keyframes later;
the user need not supply design jargon. For “more fluid” or “more polished,” propose
concrete comparable changes and show their effect. Length follows the explanation;
do not stretch a short idea or remove its mechanism to meet an invented duration.

Keep a small `brief.json` or equivalent, with each decision's value, provenance
(request/answer/standing preference), pending fields and locked content. Save
references to accepted voice/frame/film versions. File hashes identify versions;
an `approved: true` field alone is not evidence of an actual answer.

If present, read project `videodeck.local.json`, then the installed skill's
`videodeck.local.json` for personal standing choices. Apply only preferences whose
record identifies an explicit selection; task answers take priority. Missing local
assets are unresolved capabilities, not permission to substitute another voice.

Suggested project files (names are flexible): source snapshots/pointers, brief,
rough storyboard, voice recipe, full master audio, detailed timeline, cover,
captions, composition, renders, review and publication receipts. Store credentials
in the platform tool's own state, outside the project.

Optional profiles store explicitly adopted preferences. The
[technical profile](../assets/technical-profile.example.json) is an opt-in example,
not a new user's answer. Keep local voice paths and account details in ignored
`*.local.json` files. In an existing series reuse the confirmed reference voice and
style; music remains a per-task choice unless a standing preference says otherwise.
