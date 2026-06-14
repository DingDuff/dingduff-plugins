<!--
INSTRUCTIONS FOR CLAUDE
These are optional but recommended add-ons. Help the user install the skills they
want and apply the recommended settings. Skill install location differs by
environment (Cowork desktop vs claude.ai vs Claude Code). The citation-check
skill needs python3 and stored source files. Keep it simple; the research skills
trigger on their own once installed.
-->

# Skills & Recommended Settings

DingDuff works on its own, but these skills make it noticeably better. None are
required. Each is a one-time download that you upload to Claude; it then stays in
your skill picker.

> Skill files are named `dingduff_<skill>_v1.0.skill`. In Claude's skill picker
> they appear under their `dingduff-…` name.

## The skills

### Research skills

- **`dingduff-case-law-research-standard`** — the right default for most legal
  questions. Runs systematic searches, reads the actual opinions, and builds a
  cited answer.
  Download: [`dingduff_case-law-research-standard_v1.0.skill`](https://github.com/DingDuff/dingduff-plugins/blob/HEAD/dist/dingduff_case-law-research-standard_v1.0.skill)
- **`dingduff-case-law-research-deep`** — exhaustive case-law research that maps
  the full citation network and validity-checks every key case. For briefs,
  dispositive motions, and formal opinions.
  Download: [`dingduff_case-law-research-deep_v1.0.skill`](https://github.com/DingDuff/dingduff-plugins/blob/HEAD/dist/dingduff_case-law-research-deep_v1.0.skill)
- **`dingduff-statute-research-deep`** — exhaustive statutory research: full code
  mapping, definitions, cross-references, and judicial gloss on ambiguous terms.
  Download: [`dingduff_statute-research-deep_v1.0.skill`](https://github.com/DingDuff/dingduff-plugins/blob/HEAD/dist/dingduff_statute-research-deep_v1.0.skill)

### Citation checking

- **`dingduff-citation-check`** — after you draft a memo with DingDuff, verifies
  every citation against the opinion and statute files you saved and opens a
  review panel showing the memo and each source side by side. Runs entirely in
  your own session.
  Download: [`dingduff_citation-check_v1.1.skill`](https://github.com/DingDuff/dingduff-plugins/blob/HEAD/dist/dingduff_citation-check_v1.1.skill)
  Needs `python3` (Cowork and Claude Code provide it) and the cited sources saved
  first via `opinion_store` / `statute_store`.

## How to install a skill

Download the `.skill` file(s) above (on GitHub, open the file and use the
**Download raw file** button), then upload to Claude — pick the row that matches
how you use Claude:

- **Cowork (desktop):** **Customize** (upper right) → **Skills** → upload the file.
- **claude.ai (browser):** **Settings → Capabilities → Skills** → upload the file.
- **Claude Code (CLI):** install the whole library at once as a plugin instead:
  ```
  /plugin marketplace add DingDuff/dingduff-plugins
  /plugin install dingduff@dingduff
  ```

Once uploaded, the skill appears in the skill picker (the `/` menu). The research
skills trigger automatically when you ask a legal question; to cite-check, draft a
memo with DingDuff, then ask Claude to **"cite-check this memo."**

## Recommended Claude settings

### Always use DingDuff for legal research

Add a custom instruction so you don't have to ask every time:

1. Open **Profile → Instructions for Claude** (in your general settings).
2. Add something like:
   > *When I ask a legal question, always use the DingDuff connector and rely only
   > on the DingDuff database. Tell me the jurisdiction you searched and include
   > citations.*

### Turn off chat training (privacy)

In your Claude privacy settings, turn **off** the option that lets Claude train on
your chats. Recommended for confidential legal work.

## Tips for better results

When you ask a legal question, it helps to tell Claude to:

1. **Use only the DingDuff database** (so it doesn't pull from the open web) —
   handled automatically if you set the custom instruction above.
2. **Specify the jurisdiction** you want cases or statutes from.
3. **Ask for citations** in the answer.

Complex questions can take several minutes — that's normal while Claude researches.
