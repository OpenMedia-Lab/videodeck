# Production workflow

```mermaid
flowchart TD
    A[Articles, project material, script and references] --> B[Resolve consequential missing choices interactively]
    B --> C[Read sources, preserve terms and formulas, rough storyboard]
    C --> D{Narration or music?}
    D -->|Yes| E[Audition or reuse accepted voice; complete coherent master audio]
    E --> F[Refine timing from real acoustic anchors]
    D -->|No| F0[Time narrative actions and optional effects]
    F --> G[Code key static frames and independent cover]
    F0 --> G
    G --> H{Direction accepted?}
    H -->|Adjust| G
    H -->|Yes or previously accepted| I[Deterministic HyperFrames animation]
    I --> J[Check and render actual MP4]
    J --> K[caption-cli evidence; agent review; focused dense inspection]
    K --> L{Content, visual and audio checks}
    L -->|Repair affected layer| J
    L -->|Ready| M[Human reviews complete film]
    M -->|Revise authorized scope| J
    M -->|Accepted| N{Delivery}
    N -->|Local| O[Video, cover, captions, sources and review record]
    N -->|Publish| P[Interactive confirmation of full final metadata]
    P -->|Actual answer| Q[Submit, save receipt and read back platform state]
    Q --> O
```

Repairs return to the earliest bad layer (source, sound, timing, animation or encoding),
not necessarily only to rendering. Present actual audio/frame candidates rather
than asking the user to specify professional design terminology. Routine edits
reuse accepted directions; local previews can be delivered before final acceptance.

The workflow incorporates the reference tutorial
[如何用 agent 做视频](https://xhslink.cn/o/3NjfcrXedKu): rough storyboard, coherent audio,
audio-informed timing, code-first keyframes, then full animation and agent review.
Its full 380.82-second range was examined through 382 sampled images in 32 sheets
and independent local speech transcription, including the ending. This is sampled
visual inspection and transcript verification, not a claim of continuous motion
review or native listening. Tutorial media is not redistributed.

Audio providers are interchangeable. The tutorial separately credits narration
and music providers; those choices do not become dependencies of this skill.
The skill records constraints, decisions and evidence while leaving composition
and motion design open to the agent.
