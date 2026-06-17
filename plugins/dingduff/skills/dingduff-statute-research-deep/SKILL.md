---
name: dingduff-statute-research-deep
description: Exhaustive statutory research — bidirectional code mapping (top-down hierarchy + bottom-up keyword search), definition discovery, cross-code interconnections, and targeted retrieval of judicial interpretations whenever a statutory phrase is ambiguous, controlling, or has a known interpretive gloss. Use ONLY when the user explicitly requests deep, comprehensive, or exhaustive statutory research, wants a full map of a statutory regime, asks for "everything in the code on X," needs a practitioner-ready statutory roadmap, or is preparing a brief / opinion / advisory where missing a provision would be costly. Do NOT use for simple "what does § X say" lookups. (v1.1)
---

# Statute Research — Deep

This skill produces a comprehensive map of the statutory landscape on a legal issue, including every relevant code section, the definitional architecture, cross-references, and the judicial interpretations that fix the meaning of any ambiguous or outcome-determinative language. It is slow and thorough. Use it when the user needs to know they haven't missed anything.

## When to use this skill

Use only when the user explicitly asks for deep, comprehensive, exhaustive, or "all the relevant" statutory research, or when context makes clear that a casual answer won't do: a brief, formal opinion letter, regulatory compliance memo, statutory roadmap, or any matter where missing a section or misreading a defined term would materially harm the user.

For a single-section lookup or a quick "what does § X say" question, do not use this skill — call `codes_view` directly and answer.

If you are unsure whether the user wants deep work, ask.

## CRITICAL: Anti-Hallucination Protocol

**NEVER** quote or paraphrase statutory text from a search snippet. Snippets help you find sections; they do not authorize you to discuss the section's content. Before stating or quoting any statutory provision:

1. Retrieve the full section text via `codes_view`.
2. Cite by the proper statutory citation (e.g., Tex. Bus. Orgs. Code § 21.401(a); 18 U.S.C. § 1001(a)(2)). Use the `statute_id` only as an internal retrieval handle, not in user-facing prose.
3. If a section cannot be retrieved, do not discuss its substance. Note the gap and move on.

The same protocol applies to interpreting case law you pull in under Phase 5: retrieve full opinion text via `opinion_store` or `opinion_view` before quoting or asserting holdings. See `dingduff-case-law-research-standard` for the general protocol; this skill follows the same rule.

## CRITICAL: Currency and Validity

CourtListener's code database stores the statute text as imported. It does not guarantee real-time tracking of amendments or repeals. For deep research, build this awareness into the work:

- When `codes_view` returns a section, note its effective date / version annotation if present (via `metadata_view`-style retrieval for the section, or whatever metadata the response carries).
- Where the statutory text drives the answer, run a recency check by searching `opinion_search` for recent cases that cite the section — if the case discusses an amended version different from what you see, flag it.
- For federal statutes, the user's session may have authoritative outside sources (e.g., a `.gov` mirror) the user can confirm against; in that case, surface the statutory text you found and flag amendments for the user to verify.

Never silently rely on a stale version of a statute.

## Local Storage: `saved statutes` and `saved cases`

Whenever a local working directory is available, create two subfolders and save every retrieved provision or opinion there. This gives the user a durable archive of the work and lets you re-read without burning more calls.

**Setup at the start of every research task:**

```bash
mkdir -p "<working_dir>/saved statutes"
mkdir -p "<working_dir>/saved cases"
```

**Naming conventions:**

Statutes:
```
<jurisdiction>_<code>_<section>.md
```
Example: `tx_business_organizations_code_21.401.md`, `us_18_usc_1001.md`

Cases (interpreting decisions retrieved under Phase 5):
```
<cluster_id>_<short_case_name>_<reporter_cite>.md
```
Example: `107252_miranda_v_arizona_384_US_436.md`

Sanitize: lowercase, replace spaces with underscores, strip punctuation other than underscores and dots, drop "v." → "v" in case names.

If no local directory is available, fall back to inline use of `codes_view` / `opinion_view` and tell the user no archive was produced.

## Bookkeeping: The Working Set

Statute deep research expands fast, especially once you start chasing definitions and cross-references across codes. Maintain three running sets in your head (or in a scratch file in `saved statutes/`):

- **Read** — sections you have retrieved with `codes_view` and analyzed.
- **Frontier** — sections, chapters, or keyword leads identified but not yet pulled.
- **Pruned** — items considered and intentionally skipped, with a one-line reason (off-topic, redundant, covered by another section, governs a different fact pattern).

Each iteration moves frontier items into the read set, generates new frontier items from what you read (cross-references, defined terms, adjacent sections), and prunes the rest.

## Phase 1: Jurisdiction Check and Scope

### 1a. Confirm coverage

Verify the jurisdiction's codes are available:

```json
{"jurisdiction": "TX"}
```

If `codes_browse` returns no codes for the jurisdiction, report that clearly and ask the user how to proceed (the user may have other sources, or the question may need to be reframed to a covered jurisdiction).

### 1b. Set scope from context

The user did not give you knobs for depth, breadth, or section count — you set them. Use the question to calibrate. Things that argue for going wider:

- The question turns on the interaction of multiple sections or codes.
- The user mentions a "regime," "scheme," "framework," or asks for "all" provisions.
- The matter is bet-the-company, appellate, or regulatory.

Things that argue for staying tight:

- The question is about one well-defined statutory hook with a known doctrinal frame.
- The user is asking how a specific defined term operates.
- Only one code is plausibly implicated.

Note the working scope to yourself so you can revisit it later — deep research can drift, and it helps to know what you originally set out to map.

## Phase 2: Bidirectional Statutory Search

You must run both directions. They surface different provisions, and either alone will miss sections that matter.

### 2a. TOP-DOWN HIERARCHICAL SEARCH

1. **List codes for the jurisdiction**

   ```json
   {"jurisdiction": "TX"}
   ```

2. **Identify the codes likely to govern the issue**

   Common mappings:
   - Business/corporate matters → Business Organizations / Corporations codes
   - Real property and landlord-tenant → Property code
   - Criminal matters → Penal / Criminal Procedure codes
   - Civil procedure → Civil Practice & Remedies / Code of Civil Procedure
   - Family matters → Family code
   - Tax → Tax code
   - Administrative regulation → the relevant agency's regulatory code

   When in doubt, browse codes whose names plausibly touch the issue — over-inclusion at this stage is cheaper than missing a sleeper code.

3. **Drill down the hierarchy**

   For each relevant code, browse titles → divisions → chapters → subchapters → sections using `codes_browse` with the appropriate `code_id` or `node_id`. Document the hierarchy as you go; you'll need it for the tree diagram.

4. **Pull section text where the title or context suggests relevance**

   ```json
   {"statute_id": "TX/business_organizations/21.401"}
   ```

   Save to `saved statutes/<filename>.md`.

### 2b. BOTTOM-UP KEYWORD SEARCH

1. **Text search**

   ```json
   {"jurisdiction": "TX", "search_type": "text",
    "query": "shareholder derivative action", "limit": 25}
   ```

   Run multiple queries — exact phrases, individual keywords, legal synonyms. Statutes use idiosyncratic terminology; cast wide.

2. **Title search**

   ```json
   {"jurisdiction": "TX", "search_type": "title",
    "query": "derivative"}
   ```

   Title search is the quickest way to surface whole chapters dedicated to the issue.

3. **Upward exploration**

   For any section a search returns, browse the parent chapter/subchapter and check adjacent sections — related provisions are nearly always grouped. Pull adjacent sections that look relevant; prune the rest.

### 2c. Reconcile the two directions

Cross-check: every section found bottom-up should appear somewhere in your top-down hierarchy (or be added to it). Every section in your top-down hierarchy that looks relevant should be picked up by at least one keyword search (if not, your keyword set is too narrow — broaden it).

## Phase 3: Definition Discovery

Definitions control statutory interpretation. They are often where the answer actually lives. Track them down deliberately.

1. **Code-wide definition sections**

   Browse for sections titled "Definitions" near the top of relevant titles or chapters. Common patterns: section .001, .01, or the first section of a chapter. Use `codes_search` with `search_type: "title", query: "definitions"` scoped to the jurisdiction.

2. **Chapter and subchapter definitions**

   Each major chapter often has its own definition section that supersedes general definitions for that chapter's purposes. Pull them.

3. **In-line definitions**

   Statutes also define terms in-line ("As used in this section…" / "For purposes of this subsection…"). Note these as you read.

4. **Definitional conflicts**

   When the same term is defined differently in different chapters or codes, flag the conflict and identify which definition governs the user's fact pattern. This is a common trap and exactly the kind of thing deep research should catch.

Document every applicable definition in your notes — these go into the final report.

## Phase 4: Identify Phrases That Need Interpretation

Once you have the statutory landscape mapped, read the sections you've collected and flag every phrase that meets any of these tests:

- **Ambiguous on its face** — the words can carry more than one defensible meaning in the user's fact pattern.
- **Outcome-controlling** — the section's application turns on what this phrase means; the answer changes depending on the interpretation.
- **Term of art** — the phrase is a known legal term of art whose meaning is set by case law (e.g., "reasonable suspicion," "good faith," "arising out of," "in the course of employment," "knowingly," "willfully," "actual notice").
- **Definitionally underspecified** — the statute uses an undefined term that has been judicially construed.
- **Recently amended** — if you have indications of recent amendment, courts may have construed the prior language; you need to know whether the construction still applies.
- **Cross-referenced** — the phrase ties this section to another section, code, or common-law doctrine.

Flag each such phrase with: the section it appears in, the phrase itself, why interpretation is needed, and the specific question you'll ask the case law in Phase 5.

If no flagged phrases emerge, that is itself a finding: report that the text is unambiguous on its face for this question and skip Phase 5.

## Phase 5: Targeted Case Law on Flagged Phrases

For each flagged phrase, run a targeted case-law pull. This is *not* a full citation-network expansion — that is what `dingduff-case-law-research-deep` is for. The objective here is bounded: find the controlling or persuasive judicial gloss on the phrase as it appears in this section.

### 5a. Search interpreting decisions

Best queries use the statutory citation itself, the exact phrase, or both:

```json
{"query": "\"Tex. Bus. Orgs. Code § 21.401\" AND \"interest of the corporation\"",
 "court_types": "S,SA,F,FD", "order_by": "-citeCount"}
```

Or by phrase alone, scoped to the relevant courts:

```json
{"query": "\"in the course of employment\"",
 "court_types": "S,SA", "states": "TX", "order_by": "-citeCount"}
```

For binding interpretations of state statutes, focus on the state's high court and intermediate appellate courts; for federal statutes, focus on the Supreme Court and the relevant circuit. Don't ignore federal courts construing state law (Erie context) when the user's fact pattern may end up there.

### 5b. Triage and bulk retrieve

Triage candidates from snippets (don't quote snippets). Aim for **5–15 cases per flagged phrase**, weighted toward the most-cited and the most-recent. Bulk retrieve via `opinion_store` (up to 25 cluster IDs per call), download each URL with `curl` into `saved cases/`, and read.

If the user gives you a single reporter citation rather than a cluster ID, `opinion_view` accepts reporter cites directly — handy for a quick spot check.

### 5c. Extract the gloss

For each case, identify:
- The court's articulation of the phrase's meaning (the test, the elements, the rule).
- A pinpoint-cited quote stating the rule.
- Whether the rule is binding (same jurisdiction, same court level or higher) or persuasive.
- Whether it conflicts with another case in the set (intra-jurisdiction split, circuit split, or older-but-uncertain authority).

### 5d. Validity check on interpreting cases

CourtListener does not flag overturned cases. For any case you'll rely on, run `show_citing_opinions` ordered by `-dateFiled` and scan recent snippets for treatment signals (overruled, abrogated, no longer good law, rejected, declined to follow, limited). Confirm the gloss still holds. If a key interpretation has been narrowed or abrogated, do not present it as controlling — find the case that did the narrowing, retrieve it, and report the current state.

### 5e. Know when to escalate

If a flagged phrase turns out to be the subject of a sprawling, contested body of case law — circuit splits, sharp doctrinal evolution, dispositive for the user's question — say so and recommend running `dingduff-case-law-research-deep` on that phrase as a focused follow-up. This skill should not silently turn into a citation-network build.

## Phase 6: Self-Directed Expansion and Stopping

Phases 2–5 iterate. Each pass adds sections to the read set, surfaces new cross-references, finds new defined terms, raises new flagged phrases. Keep going until the network is saturated.

### When to stop

Stop when most of these are true:

- **Saturation**: New browses and searches return sections you've already pulled. You're going in circles.
- **All relevant codes covered**: Every code you flagged as plausibly implicated has been browsed and triaged.
- **Definitions mapped**: Every defined term that controls the user's question has been pulled and noted.
- **Cross-references resolved**: Every cross-reference inside the sections you rely on either points to a section in your read set or has been intentionally pruned.
- **Interpretation captured**: Every flagged phrase has either a documented judicial gloss or an explicit note that no controlling interpretation was found.
- **Currency checked**: Effective-date/amendment annotations have been read; recent case law has been used to spot any amendment indicators.
- **Diminishing returns**: Each additional pull is adding less than the marginal cost. Be honest.

### When NOT to stop

- A code you flagged as possibly relevant in Phase 1 hasn't been browsed.
- A defined term controlling the answer is still undefined in your notes.
- A flagged phrase doesn't yet have an interpretation or an explicit "no case law" finding.
- A cross-reference points somewhere you haven't followed.
- You have an unread citing case showing recent amendment or adverse treatment.

If the read set grows past ~50 sections, the scope was probably set too broadly. Narrow it (specific element, sub-issue, or fact pattern) and re-anchor.

## Phase 7: Synthesize the Report

Structure the output as follows. This format is designed to be a practitioner's reference; preserve the order even if a particular section is brief.

1. **Executive Summary**
   - Jurisdiction.
   - Area of law / question framed.
   - Codes reviewed (list).
   - Sections identified vs. sections viewed (counts).
   - Headline answer (2–4 sentences).

2. **Statutory Tree**

   A hierarchical diagram of the codes mapped, with viewed sections marked. Example:

   ```text
   TEXAS LEGAL CODES — Shareholder Derivative Actions
   │
   ├── Business Organizations Code
   │   ├── Title 2: Corporations
   │   │   ├── Chapter 21: For-Profit Corporations
   │   │   │   ├── Subchapter L: Derivative Proceedings
   │   │   │   │   ├── § 21.551: Definitions (viewed)
   │   │   │   │   ├── § 21.552: Standing (viewed)
   │   │   │   │   └── § 21.553: Demand (viewed)
   │   │   │   └── Subchapter M: …
   │   │   └── Chapter 22: Nonprofit Corporations
   │   └── Title 1: General Provisions
   │       └── Chapter 1: Definitions (viewed)
   └── DEFINITIONAL PROVISIONS
       ├── BOC § 1.002: General defined terms (viewed)
       └── BOC § 21.551: Subchapter-specific definitions (viewed)
   ```

3. **Key Provisions Analysis**

   The 5–15 sections that drive the answer. For each:
   - Citation (proper format).
   - One-sentence description of what the section does.
   - The operative language (short quote with pin reference if statutes use subsections).
   - How it interacts with other sections in the set.

4. **Applicable Definitions**

   Every definition relevant to the question, with the section, the term, and the operative definitional language. Flag any conflicts across chapters or codes and identify which controls.

5. **Judicial Interpretation of Flagged Phrases**

   For each Phase 4 phrase: the phrase, the section it appears in, the controlling or best-persuasive case(s), the rule the case extracts, and a pinpoint quote. For phrases with no controlling interpretation, say so explicitly.

6. **Cross-References and Interconnections**

   How the sections fit together. Where one section depends on another. Where definitions in one code govern a term used in another.

7. **Issue-Specific Findings**

   Direct answer to the user's question(s), mapping each question to the controlling sections + interpretive cases.

8. **Currency and Validity Notes**

   Effective dates noted, amendment indicators flagged, interpreting cases validity-checked. Brief — the user just needs to see you did this work.

9. **Practitioner's Roadmap**

   A short sequence: read these sections first, in this order; check these definitions before applying them; look out for these traps.

10. **Research Notes**

    Gaps, ambiguities, recommendations for further research, and any phrase or sub-issue where deep case-law research is warranted as a separate workstream.

## Phase 8: Comprehensive Section / Case Table

Include a table of every section and every interpreting case you retrieved — not just the ones cited in the final answer. This is the audit trail.

**Statutes:**

| Citation | Statute ID | Role | Status | Operative Language | Local File |
|---|---|---|---|---|---|
| Tex. Bus. Orgs. Code § 21.552 | TX/business_organizations/21.552 | Primary | Effective | "A shareholder may not commence or maintain a derivative proceeding unless…" | `tx_business_organizations_code_21.552.md` |

**Interpreting cases (Phase 5):**

| Case Name & Citation | Cluster ID | Phrase Construed | Validity | Key Quote | Local File |
|---|---|---|---|---|---|
| *In re XYZ Corp.*, 555 S.W.3d 100 (Tex. 2018) | ###### | "fairly and adequately represent" | Good law | "[quote]" *Id.* at 110. | `..._in_re_xyz_corp_555_swd_100.md` |

## Quick Reference

### Tool choice

- **`codes_browse`** — Hierarchy navigation. No args = jurisdictions. `{jurisdiction}` = codes. `{code_id}` or `{node_id}` = drill down.
- **`codes_search`** — Keyword search. `search_type: "title"` for chapter/section discovery; `search_type: "text"` for substantive language search. Max `limit: 25`.
- **`codes_view`** — Full section text. `statute_id` format: `[jurisdiction]/[code]/[section]`.
- **`opinion_search`** / **`opinion_store`** / **`opinion_view`** — For Phase 5 interpreting cases. See `dingduff-case-law-research-standard` for the full case-retrieval workflow.
- **`show_citing_opinions`** — Forward validity check on interpreting cases.

### Patterns

```text
# Bidirectional sweep
codes_browse {jurisdiction}           # what codes exist
codes_browse {code_id}                # what's in a code
codes_search {text + title}           # what mentions the issue
codes_view {statute_id}               # the actual text

# Definition discovery
codes_search {search_type: "title", query: "definitions"}
codes_browse to find chapter-level definition sections

# Interpreting case law on a flagged phrase
opinion_search "<statutory cite>" AND "<phrase>"
  → triage → opinion_store bulk → save → read
show_citing_opinions on each retained case (validity)
```

### Quality checklist

- [ ] Jurisdiction confirmed via `codes_browse`.
- [ ] Top-down hierarchy mapped for every plausibly relevant code.
- [ ] Bottom-up keyword and title searches run with multiple terminologies.
- [ ] Adjacent sections checked, not just hits.
- [ ] All applicable definitions identified and pulled.
- [ ] Phrases requiring interpretation flagged with explicit reasons.
- [ ] Targeted case-law pulled for each flagged phrase (or "no interpretation found" recorded).
- [ ] Validity check run on each interpreting case via `show_citing_opinions`.
- [ ] Currency / amendment annotations noted; stale text flagged.
- [ ] `saved statutes/` and `saved cases/` populated.
- [ ] Citations are in proper statutory and reporter format (statute_id and cluster_id stay internal).
- [ ] Tree diagram included.
- [ ] Comprehensive section + case table included.

## Remember

Deep statutory research is not about pulling every section in the code — it is about producing a map the user can rely on, with no missing chapters and no defined term silently reshaping the answer. Show the work: definitions documented, ambiguous phrases construed, currency confirmed. Where the case law gets too deep for this skill to handle properly, say so and recommend the dingduff-case-law-research-deep skill as a focused follow-up.
