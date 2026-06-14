<!--
INSTRUCTIONS FOR CLAUDE
This page explains how the DingDuff citation-check system works — what it can
check, the design choices behind its reliability and privacy, and the workflow.
Surface it when a user asks whether cite-check is accurate/reliable, whether their
document or data stays private, what kinds of writing or sources it can check, or
how the process works. For *installing* the skill, point to the Skills page; the
dingduff-citation-check skill drives the actual run — this page is the explainer.
Be precise about privacy: the local verification sends nothing, but the interactive
review panel passes the document through DingDuff once as call arguments (never
stored or logged), and the standalone review.html keeps everything on the machine.
-->

# How Citation Checking Works

DingDuff's citation checker takes a piece of legal writing you've drafted, checks
every citation in it against the actual source text, and opens a review panel where
you — the attorney — give the final word on each one. It then produces a printable
audit record for the file. This page explains what it can do and the design choices
that make it reliable and private. To install it, see [Skills & Settings](Skills).

## What it can check

**Any legal writing that cites authority** — a brief, motion, memorandum, demand or
opinion letter, or any block of text with citations. Hand it your document as
**Markdown, Word (.docx), Google Docs** (downloaded as .docx), or a text-based PDF.

It checks those citations against:

- **Authorities you pulled from DingDuff** — opinions and statutes you saved with
  the `opinion_store` and `statute_store` tools.
- **Any source you supply yourself** — a Restatement section, a case that isn't in
  CourtListener, the opposing party's brief, a factual exhibit: any text-based file
  you drop into your working folder. Citation checking is **not** limited to
  DingDuff's library.

And it produces:

- An **interactive review panel** showing your document on one side and each cited
  source on the other, with the supporting passage highlighted.
- Your **recorded verdicts** on each citation.
- A **printable audit log** for the file and the court.

## How it stays reliable

The job of the tool is to confirm a citation actually says what your draft claims —
and to do it in a way you can trust.

- **Quotes are verified by code, not by the AI's memory.** Claude proposes the
  passage that supports each point, but a small program running in your own session
  then searches the real source file for that exact text. If the text isn't there,
  it can't be marked as supported. **A made-up or misremembered quote can't slip
  through as a verified highlight.** The matching is forgiving about formatting —
  spacing, curly vs. straight quotes, hyphenation across line breaks — so honest
  quotes aren't flagged over cosmetic differences.
- **It shows you the evidence, not just a verdict.** For every citation you see the
  claim, the exact highlighted passage in the source, and your document side by
  side — so you can judge it yourself instead of taking the tool's word for it.
- **You give the final verdict — and there are three.** On each citation you mark it
  **verified**, **needs attention** (supported, but with a caveat you note), or
  **rejected**. The tool flags the ones that deserve scrutiny — a quote it couldn't
  find, a quote that turned out to be from a different case, or a source you never
  provided — but the attorney is always the guardrail. That's DingDuff's whole
  philosophy: the lawyer checks the work, so the tool never pretends to be
  infallible.

## How it protects your privacy

Legal drafts are confidential, so the design keeps your work on your machine as much
as possible:

- **The checking itself is entirely local.** The program that matches quotes to
  sources runs in your own session and sends nothing anywhere.
- **The interactive review panel** passes your document and the cited excerpts
  through the DingDuff server **once** — only as the arguments needed to draw the
  panel — and they are **never stored or logged**. If you'd rather nothing transit
  at all, the tool also generates a **standalone `review.html`** you can open
  locally; that version never leaves your machine.
- **Sources you supply** are handled locally, and **the only thing sent back into
  the chat is your own verdicts**, as text, when you choose to send them.
- Everything lands in your working folder (the verification results, your verdicts,
  the audit log), and you can delete any of it whenever you like. DingDuff keeps no
  copy of your document or your verdicts.

## How to use it

1. **Draft your document** — brief, motion, letter, memo — in any format.
2. **Save the sources it cites.** Use `opinion_store` / `statute_store` for DingDuff
   authorities; for anything else, drop a text copy into your working folder.
3. **Ask Claude to cite-check it** (e.g., *"cite-check this brief"*). Claude reads
   your draft, lines each citation up with its source, and runs the local verifier.
4. **Review in the panel.** Step through each citation, read the highlighted support,
   and mark it verified / needs attention / rejected, adding a note where useful —
   then send your verdicts back.
5. **Revise if needed and re-run** — citations you've already cleared carry their
   verdicts forward automatically.
6. **Generate the audit log** — a printable record of what was checked, the verdicts,
   and who reviewed it, for the file.

You'll need `python3` available (Cowork and Claude Code include it). To install the
skill, see [Skills & Settings](Skills); if a step fails, see
[Troubleshooting](Troubleshooting).

## What it does not do

Citation checking confirms that a cited source **actually contains the language and
supports the point** your draft relies on. It does **not** tell you whether an
authority is still good law (overruled, abrogated, superseded) — use the research
skills for that — and it doesn't replace your professional judgment about whether an
authority fits your argument.
