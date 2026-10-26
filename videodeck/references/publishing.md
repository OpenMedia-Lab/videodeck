# Delivery and publication

Local delivery includes final video, separate cover, canonical subtitles, editable
composition/assets, brief/storyboard/voice recipe/timeline, and review findings.
Present the complete film for human review. A local preview can be delivered while
awaiting feedback; do not call it human-accepted until the user accepts it.

For platform publication, finish the concrete film and copy first. Use a separate
interactive question containing each video's **complete title, complete description
with actual paragraph breaks, category, tags and visibility**, plus collection/order
when applicable. Present exactly what will be submitted, rather than abbreviated
copy or a path to unseen metadata. Wait for the actual answer. General “publish it”
intent, selecting the video direction or accepting the film does not substitute for
confirmation of final metadata. If the same exact version is already confirmed,
proceed without another permission ritual. Reconfirm changed metadata.

Keep titles/descriptions faithful to both the source topic and what this film
teaches. Keep full provenance locally. Adapt public source attribution to the
destination's current rules using the selected adapter before final confirmation.
Use actual newlines in structured JSON, not strings containing literal `\\n` that
will appear in the post.
Persist the submitted metadata version and link the real confirmation to it.

Use the existing platform CLI/connector, inspect its current help/capabilities and
validate formats/limits before writing. Read the [Bilibili adapter](platforms/bilibili.md)
for that destination, or the [Xiaohongshu adapter](platforms/xiaohongshu.md) for
Xiaohongshu; add another adapter only when needed. Authenticate using
the tool's supported method and actual user action. Do not manufacture QR links.

For existing-note revisions, respect the requested original ID and inspect actual
media-replacement capability. Prepare changes for review before writing. A missing
edit capability does not authorize deleting, reposting or appealing; report the
limit and resolve the next action with the user.

After confirmed submission, save receipts and read back exact visible title,
description/newlines, category, tags, media/cover, visibility and collection order.
Platform acceptance, processing, review, recommendation/search restrictions and
public availability are different states: report the observed state and its time,
plus the verified URL/ID. A readable public note can still have a moderation
restriction; inspect creator moderation fields when available. If the call outcome is
unknown, query the receipt/creator state before retrying; avoid duplicate posts.

Respect the user's metadata preferences, including whether to add manual AI-related
text, but verify current destination requirements instead of treating a remembered
platform rule as permanent. Do not alter tags/description silently after approval.
Unavailable publication leaves the complete local bundle and a precise limitation.
