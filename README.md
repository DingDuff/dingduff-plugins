# DingDuff Plugins & Skills

Distribution home for [DingDuff](https://dingduff.com) legal-research and
legal-workflow skills for Claude. These skills are built to work with the
**DingDuff MCP connector** — if you haven't set that up yet, start with the
[installation wiki](https://github.com/DingDuff/dingduff-public/wiki).

## The skills library

| Skill | What it does |
|-------|--------------|
| `dingduff-legal-research` | Legal research end-to-end — finds, retrieves, reads, and validates controlling cases, statutes, and regulations; maps the citation network and statutory landscape; confirms everything is still good law. Replaces the former case-law (standard/deep) and statute-research skills. |
| `dingduff-citation-check` | After you draft a memo (Markdown, Word, or Google Docs), verifies every citation against your stored opinions and statutes plus any other sources you supply (a Restatement section, an off-CourtListener case, an opposing brief, a factual PDF), and opens an attorney review panel. |
| `dingduff-legal-citation-format` | Formats citations in practitioner / brief style (cases, statutes, signals, pincites, short forms, quotations). Form only — pair with the research / cite-check skills for verification. Standalone (no connector required). |

## Naming & versioning

- Downloadable skill files are named **`dingduff_<skill>_v1.0.skill`** — the
  `dingduff_` prefix marks them as DingDuff skills, and the `_vX.Y` suffix tracks
  the version. New releases bump the suffix.
- In Claude's skill picker, each skill appears under its internal
  **`dingduff-<skill>`** name.

## Install (recommended): upload the .skill file

1. Download the skill(s) you want from [`dist/`](dist/) (open the file and use the
   **Download raw file** button):
   - [`dingduff_legal-research_v2.1.skill`](dist/dingduff_legal-research_v2.1.skill)
   - [`dingduff_citation-check_v1.9.skill`](dist/dingduff_citation-check_v1.9.skill)
   - [`dingduff_legal-citation-format_v1.4.skill`](dist/dingduff_legal-citation-format_v1.4.skill)
2. In Claude, open your **Skills** settings:
   - **Cowork (desktop):** Customize (upper right) → **Skills** → upload skill
   - **claude.ai:** Settings → **Capabilities** → Skills → upload skill
3. Upload the `.skill` file. It then appears in the skill picker under its
   `dingduff-…` name.

The research skills trigger automatically when you ask a legal question (or pick
one from the `/` menu). To cite-check: draft a memo with DingDuff, then ask Claude
to "cite-check this memo."

## Install (alternative, Claude Code CLI)

This repo is also a Claude Code plugin marketplace — installing the plugin gives
you the whole skills library at once:

```
/plugin marketplace add DingDuff/dingduff-public
/plugin install dingduff@dingduff
```

## Requirements

- The **DingDuff MCP connector** added to your Claude client — the skills use
  DingDuff's research tools, and cite-check uses the `citecheck_review` panel.
  See the [wiki](https://github.com/DingDuff/dingduff-public/wiki).
- For `dingduff-citation-check`: `python3` available to the session (Cowork and
  Claude Code provide it).
- `dingduff-legal-citation-format` is standalone — it formats citations and needs
  no connector or `python3`.

## Updates

Re-download the `.skill` file and upload it again (marketplace users:
`/plugin marketplace update dingduff`). New versions bump the `_vX.Y` suffix.

## Source

Skills are developed in the DingDuff MCP server repository and vendored here for
distribution. Each `dist/dingduff_<skill>_v1.0.skill` is a zip of the matching
`plugins/dingduff/skills/dingduff-<skill>/` folder.
