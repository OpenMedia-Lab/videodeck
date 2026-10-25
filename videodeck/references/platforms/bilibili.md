# Bilibili

Use the current [bilibili-cli](https://github.com/OpenMedia-Lab/bilibili-cli) help
for login, upload, metadata, submission, querying and collections. Confirm actual
category ids, limits, video/cover formats and visibility capabilities for the
installed version. Do not guess unsupported flags or imply a private state exists
when the platform/tool cannot provide it.

The repository's executable is `bilibili`: discover it, then run `bilibili --help`
and the relevant subcommand help. Repository names need not be executable names.

When a series profile specifies landscape 1080p/30fps, reuse it; other projects can
choose another supported format. Series name and episode order come from this task.
Validate the independent cover and subtitle file against destination constraints.

Follow the [final metadata gate](../publishing.md) before submission. Preserve true
paragraph newlines end-to-end; verify the creator-side readback, not just the local
JSON serialization. After submission distinguish review/processing from public
playability. Confirm collection membership and numeric episode ordering separately.

Use the CLI's real QR login if authentication is needed and supported. Retain its
private session in its own state directory. Query an uncertain submission before
retrying; receipts and creator views reconcile it. Return only actual identifiers,
URLs and observed states. Do not automatically add AI labels or series tags from
another project's metadata; use confirmed copy and current platform requirements.
