# DingDuff Plugins & Skills

Distribution home for [DingDuff](https://dingduff.com) legal-research and
legal-workflow skills for Claude. These skills are built to work with the
**DingDuff MCP connector** — if you haven't set that up yet, start with the
[installation wiki](https://github.com/DingDuff/dingduff-plugins/wiki).

## The skills library

| Skill | What it does |
|-------|--------------|
| `dingduff-case-law-research-standard` | Systematic case-law research — strategic searches, retrieves and reads the actual opinions, builds a cited answer. The right default for most legal-research questions. |
| `dingduff-case-law-research-deep` | Exhaustive, recursive case-law research that maps the full citation network (ancestors + descendants) and validity-checks every key case. For briefs, dispositive motions, and formal opinions. |
| `dingduff-statute-research-deep` | Exhaustive statutory research — bidirectional code mapping, definitions, cross-references, and judicial gloss on ambiguous terms. |
| `dingduff-citation-check` | After you draft a memo, verifies every citation against your stored opinion/statute files and opens an attorney review panel. |
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
   - [`dingduff_case-law-research-standard_v1.0.skill`](dist/dingduff_case-law-research-standard_v1.0.skill)
   - [`dingduff_case-law-research-deep_v1.0.skill`](dist/dingduff_case-law-research-deep_v1.0.skill)
   - [`dingduff_statute-research-deep_v1.0.skill`](dist/dingduff_statute-research-deep_v1.0.skill)
   - [`dingduff_citation-check_v1.1.skill`](dist/dingduff_citation-check_v1.1.skill)
   - [`dingduff_legal-citation-format_v1.1.skill`](dist/dingduff_legal-citation-format_v1.1.skill)
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
/plugin marketplace add DingDuff/dingduff-plugins
/plugin install dingduff@dingduff
```

## Requirements

- The **DingDuff MCP connector** added to your Claude client — the skills use
  DingDuff's research tools, and cite-check uses the `citecheck_review` panel.
  See the [wiki](https://github.com/DingDuff/dingduff-plugins/wiki).
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
