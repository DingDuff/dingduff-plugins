---
name: dingduff-citation-check
description: Verify every citation in a drafted legal memo (Markdown, Word, or Google Docs) against stored opinions and statutes plus any other source documents the attorney supplies (a Restatement section, an off-CourtListener case, an opposing brief, a factual PDF). Use after drafting a memo when the user asks to cite-check, citecheck, verify citations, verify quotes, check cites, or validate authorities. Produces cites.json, opens the interactive attorney review panel (or a standalone review.html), and records the attorney's verdicts in review.json. (v1.6)
---

# Cite-Check: verify a memo's citations against stored sources

You orchestrate a propose-and-verify loop: YOU propose verbatim supporting
quotes; a deterministic local script verifies them and computes anchors. A
hallucinated quote cannot become a highlight — the script only accepts text
that actually exists in the source file.

Privacy: verification runs entirely in this session. When the review panel
opens via `citecheck_review`, the memo transits the DingDuff server once as
tool arguments and is never stored or logged. The standalone `review.html`
fallback never leaves the machine at all. State this plainly if the user
asks.

## Step 0 — Preflight

1. Run `python3 --version`. If python3 is missing, stop and tell the user it
   is required (macOS: `xcode-select --install` or `brew install python3`).
2. Resolve `<skill-dir>` — the directory holding this skill's `scripts/`:
   - If the `CLAUDE_PLUGIN_ROOT` environment variable is set (the skill was
     installed as a plugin), use
     `${CLAUDE_PLUGIN_ROOT}/skills/dingduff-citation-check`.
   - Otherwise (running from a source checkout) use the absolute directory
     containing this SKILL.md.
   Confirm `<skill-dir>/scripts/verify_anchors.py` exists before proceeding.
3. Run every script from the PROJECT ROOT (the working folder containing the
   memo), so all recorded paths are project-root-relative.

## Step 1 — Locate and normalize the memo

Cite-check verifies plain UTF-8 text, so accept the memo in any common form and
convert it to a Markdown working file first. **That converted `.md` is the memo
of record** — its path and SHA-256 are what flows through `cites.json` and what
the audit certifies, so everything below uses it as `memo.path`. Tell the user
plainly which file you are checking.

- **Markdown / plain text** (`.md`, `.txt`): use as-is.
- **Word** (`.docx`): convert with the bundled extractor —
  ```
  python3 <skill-dir>/scripts/extract_docx.py --in <memo>.docx --out <memo>.md
  ```
  It keeps paragraph order and pulls in **footnotes and endnotes** (where legal
  cites often live) and the accept-all view of tracked changes. If its stderr
  warns about unaccepted tracked changes, say so — the check ran against the
  accepted text — and ask the user to confirm that is the version they mean.
- **Google Docs**: export/download the doc to `.docx` (the connected Google
  Drive tool's export, or in the browser File → Download → Microsoft Word),
  then convert it the same way.
- **PDF** (only when the PDF itself is the work product): extract its text layer
  to `.md`/`.txt` with available PDF tooling, then check that. There is **no
  OCR** — a scanned PDF with no text layer cannot be checked.

If multiple memo candidates exist, ask the user which to check.

## Step 2 — Inventory the stored sources

Convention: source files live in `sources/` under the project root, saved
there from `opinion_store`/`statute_store` download URLs. (Going forward,
always save those downloads into `sources/`.)

Also search the rest of the working folder for strays:
- Opinion files contain a `**Cluster ID:** <id>` line.
- Statute files start with `# <citation>` and contain `**Code:**` and
  `**Section:**` lines.

If the same cluster is stored twice, use the newest file and tell the user.

Build the sources map:
- Opinions: key `cl-{cluster_id}` (cluster id from the FILE's Cluster ID
  line), with `type, path, cluster_id, case_name, citation`.
- Statutes: key `stat-{filename stem}`, with `type, path, statute_id, code,
  section, jurisdiction`. `statute_id` is the `[jurisdiction]/[code]/[section]`
  identifier used with statute_store (e.g. `TX/property/92.006`,
  `US/18-usc/1001`) — reconstruct it from the file's metadata block. The
  review panel needs it to re-fetch the statute, so get it right.

### Working-file sources (non-DingDuff)

The DingDuff corpus isn't comprehensive. The attorney can also cite-check
against sources they supply — a Restatement section, a case missing from
CourtListener, the other side's brief, a factual PDF. Treat any such file as a
`document` source:

- Accept it as text/markdown (pasted in or saved into `sources/`), or extract
  it first: `.docx` via `python3 <skill-dir>/scripts/extract_docx.py --in
  <file>.docx --out sources/<name>.md`; a **text-layer** PDF via available PDF
  tooling. There is **no OCR** — a scanned image-only PDF can't be checked.
- Map it as key `doc-{filename stem}`, with `type: "document", path, title`
  (a human label, e.g. `"Defendant's MSJ Brief"`, `"Restatement (Second) of
  Torts § 46"`) and `kind` ∈ `case | secondary | brief | evidence | other`.
- Two honest limits to state to the attorney: the tool verifies only that the
  quoted/paraphrased text **appears in the file** — for an off-CourtListener
  "case" it does **not** confirm the case is real or still good law; and a
  document is only as trustworthy as the file supplied (extraction can be
  lossy, so a noisy PDF yields more `anchor_failed` rows to eyeball).

## Step 3 — Enumerate every citation INSTANCE

Read the memo end to end. Every citation instance gets its own entry — the
same case cited five times yields five entries, and `Id.`, `supra`, and
short forms count. Resolve what each `Id.`/short cite refers to by reading
context.

For each instance record:
- `id`: `c001`, `c002`, … in memo order.
- `cite_text`: the citation EXACTLY as it appears in the memo.
- `memo_context`: ~40+ chars of surrounding memo text containing cite_text.
  REQUIRED whenever cite_text appears more than once in the memo (always
  required for `Id.` forms); the snippet itself must be unique in the memo.
- `pin`: the pin-cite page, if any (e.g. "461").
- `proposition`: one sentence stating what this citation is offered to
  support — the claim the attorney will verify.
- `support_type`: `"quotation"` if the memo quotes the source, else
  `"paraphrase"`.
- `anchors_proposed`: 1–3 quotes copied VERBATIM from the stored source
  file that support the proposition.

Hard rules for quotes:
- Open the stored file and COPY the passage — reproduce the source's own
  punctuation and capitalization, not the memo's bracketed alterations or
  cleaned-up quotation marks.
- Use `...` only for genuine omissions; every segment around an ellipsis
  must be at least ~10 characters, segments must appear in document order,
  and they must be reasonably close together.
- NEVER quote from the `## Citing Cases` section or the file footer — only
  the opinion body (the verifier rejects these). This guard is opinion-only;
  for a `document` source the whole file is quotable.
- Signal cites (*see generally*, string-cite tails) where no specific
  passage is claimable: set `"no_quote_claimed": true` with empty
  `anchors_proposed`. Use sparingly — every no-quote citation is one the
  attorney must verify entirely by hand.

## Step 4 — Missing sources

If a cited authority has no stored file, tell the user and offer to fetch it
now (opinion_store / statute_store → save into `sources/`). If the user
declines, still include the citation, with a source entry of
`{"type": "opinion"|"statute", "missing": true, "case_name"/"citation": ...}`
so it is tracked as unverifiable rather than silently dropped.

## Step 5 — Write proposals and verify

Write `.cite-check/proposals.json` (create the scratch dir):

```json
{
  "schema_version": 1,
  "memo": { "path": "memo.md" },
  "sources": {
    "cl-12345": { "type": "opinion", "path": "sources/smith_v_jones_12345.md",
                  "cluster_id": "12345", "case_name": "Smith v. Jones",
                  "citation": "123 F.3d 456" },
    "stat-tex_prop_code_92_006": { "type": "statute",
                  "path": "sources/tex_prop_code_92_006.md",
                  "statute_id": "TX/property/92.006",
                  "code": "Property Code", "section": "92.006" },
    "doc-restatement_torts_46": { "type": "document",
                  "path": "sources/restatement_torts_46.md",
                  "title": "Restatement (Second) of Torts § 46",
                  "kind": "secondary" }
  },
  "citations": [
    { "id": "c001", "source": "cl-12345",
      "cite_text": "Smith v. Jones, 123 F.3d 456, 461 (9th Cir. 1997)",
      "pin": "461",
      "memo_context": "The discovery rule controls. Smith v. Jones, 123 F.3d 456, 461",
      "proposition": "The discovery rule governs accrual.",
      "support_type": "paraphrase",
      "anchors_proposed": [ { "quote": "the limitations period does not begin to run until ..." } ],
      "no_quote_claimed": false }
  ]
}
```

Then run:

```
python3 <skill-dir>/scripts/verify_anchors.py \
    --proposals .cite-check/proposals.json --out cites.json \
    --generated-by "<model name> via /cite-check"
```

Exit codes: `0` all anchored → continue. `2` fatal → relay stderr and stop.
`1` retryable failures → the stdout JSON report lists each failure with a
`reason` and a `hint`:
- `not_found`: re-open the source near the hint text and re-copy verbatim.
- `case_mismatch`: the hint IS the exact source text — use it.
- `only_in_citing_cases`: you quoted the appendix; find body support.
- `ambiguous_in_memo` / `memo_context_not_found` / `cite_text_not_in_context`:
  fix the memo_context snippet.
- `segment_too_short` / `ellipsis_gap_too_large`: quote more around the
  ellipsis or drop it.

Fix proposals and re-run. MAXIMUM 2 retries; anything still failing stays
`anchor_failed` in cites.json (the attorney sees it flagged red — that is
working as designed, not something to hide). `source_missing` entries are
not retryable.

## Step 6 — Open the attorney review

Call the `citecheck_review` MCP tool with:
- `memo_text`: the memo file content, passed VERBATIM (do not re-wrap,
  reformat, or "clean up" — the panel verifies it against the memo's
  SHA-256 from cites.json and flags any transcription drift).
- `cites`: the parsed content of cites.json.
- `documents`: **required if cites.sources has any `document` entries** — a map
  from each `document` source key to `{ "text": "<the file's full contents,
  verbatim>", "title": "<same label>" }`. These working files ride inline to
  the panel and, like the memo, are never stored or logged. Do **not** include
  opinions or statutes here (those are fetched live from DingDuff). Omit the
  argument entirely when there are no document sources.

This renders the two-pane review panel in the conversation. Then ALWAYS
build the standalone fallback too (cheap, local, and the only path on
clients without app support):

```
python3 <skill-dir>/scripts/build_review.py --cites cites.json --out review.html
```

(add `--review review.json` if a prior review export exists). Check the
tool result's `structuredContent.panel` field: if it is `"may_not_render"`,
LEAD with the fallback — tell the user to open `review.html` in a browser
rather than waiting for a panel that won't appear. Otherwise mention
review.html as the backup if no panel appears above.

## Step 7 — Summarize for the attorney

Give a compact table: id · citation · source · status · match quality ·
warnings. Then explicitly call out, in prose:
- every `anchor_failed` citation and why,
- every `source_missing` (unverifiable) citation,
- every `no_quote_claimed` citation,
- any verifier warnings (`multiple_matches`, `short_quote`,
  `match_in_header`, `cluster_id_mismatch`).

Explain next steps: review each citation in the panel (j/k to move, 1–3 for
verdicts), then click "Send review to Claude" (panel) or "Export
review.json" (standalone).

## Step 8 — Record the verdicts

When the attorney finishes, the panel sends a message containing a fenced
```json review.json block. Save it VERBATIM as `review.json` in the project
root (next to cites.json). Confirm the save and summarize the verdicts —
especially any `rejected` (‼️) or `needs_attention` (⚠️) citations, which need
memo revisions. After revising the memo, re-run /cite-check; verdicts whose
citation and proposition are unchanged carry forward automatically.

## Step 9 — Generate the audit log

After review.json is saved, generate the printable audit record:

```
python3 <skill-dir>/scripts/build_audit.py --cites cites.json \
    --review review.json --out cite-check-audit.html
```

Tell the attorney `cite-check-audit.html` is ready — it prints on landscape
letter paper and records, per citation: the source, the proposition, whether
the verifier anchored it, the attorney's verdict (✅ ⚠️ ‼️ ❓), the review
note, and the reviewer — plus an integrity footer (memo hash, verification
provenance). This is the firm's record that the work product was checked.
If the user wants the audit before any attorney review, run it without
`--review` (all rows show ❓).
