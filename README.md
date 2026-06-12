# DingDuff Plugins & Skills

Distribution home for [DingDuff](https://dingduff.com) legal-workflow skills
for Claude.

## The citation-check skill

**`dingduff-citation-check`** — after you draft a legal memo with the DingDuff
MCP tools, verifies every citation against your locally stored opinion and
statute files and opens an attorney review panel showing the memo and each
cited source side by side, with supporting passages highlighted. Verification
runs entirely in your own Claude session.

## Requirements

- The **DingDuff MCP connector** added to your Claude client (the skill uses
  DingDuff's `opinion_store` / `statute_store` tools and the
  `citecheck_review` review panel).
- `python3` available to the session (Cowork and Claude Code provide this).

## Install (recommended): upload the .skill file

1. Download **[`dist/dingduff-citation-check.skill`](dist/dingduff-citation-check.skill)**
   (use the "Download raw file" button).
2. In Claude, open your **Skills** settings:
   - **Cowork (desktop):** Customize (upper right) → **Skills** → upload skill
   - **claude.ai:** Settings → **Capabilities** → Skills → upload skill
3. Upload the `.skill` file. The skill then appears in the skill picker as
   **dingduff-citation-check**.

To use it: draft a memo with DingDuff, then ask Claude to "cite-check this
memo" (or pick the skill from the `/` menu).

## Install (alternative, Claude Code CLI)

This repo is also a Claude Code plugin marketplace:

```
/plugin marketplace add DingDuff/dingduff-plugins
/plugin install dingduff@dingduff
```

## Updates

Re-download the `.skill` file and upload it again (marketplace users:
`/plugin marketplace update dingduff`).

## Source

The skill is developed in the DingDuff MCP server repository and vendored here
for distribution. `dist/dingduff-citation-check.skill` is a zip of
`plugins/dingduff/skills/dingduff-citation-check/`.
