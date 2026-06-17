---
name: dingduff-case-law-research-standard
description: Find and analyze relevant case law systematically. Use for any legal research requiring court opinions, precedent analysis, citation verification, or comprehensive case law documentation. Trigger whenever the user asks about "the law on X," wants to "find cases" or "research precedent," asks "what does the case law say," wants a memo or brief built on authority, or needs to verify holdings, quotes, citations, or a circuit split — even if the user never says the words "case law" or "research." (v1.1)
---

# Case Law Research

## CRITICAL: Anti-Hallucination Protocol

**NEVER** discuss a case's holding, reasoning, or quotes based on search snippets alone. Search snippets exist only to help you decide which cases to retrieve — they are not citable substance.

Before stating *any* holding or quoting *any* language:
1. Retrieve the actual opinion text via `opinion_store` (preferred — saves a local copy) or `opinion_view` (inline text only).
2. Cite by reporter citation and pinpoint page (e.g., *Miranda v. Arizona*, 384 U.S. 436, 444 (1966)). Reporter citations are the standard format for legal work product; cluster IDs are an internal CourtListener identifier and should not appear in citations to the user. Keep cluster IDs in your working notes and the case table for retrieval, but cite the reporter cite in any prose, memo, or brief.
3. If you cannot retrieve a case's text, do not discuss its substance — note that retrieval failed and move on.

This protocol is the single most important rule in this skill. Every other phase exists to support it.

## Local Storage: The `saved cases` Folder

Whenever the user has connected (mounted, selected) a folder from their own computer, create a subfolder called `saved cases` inside that user-selected folder and save every retrieved opinion there as a markdown file. This gives the user a durable, browsable archive of the cases you actually read, lets you re-open them without burning more tool calls, and makes downstream drafting (memos, briefs, tables) far cheaper.

Use the user-visible folder you have been given access to — the same folder you would save any other user deliverable into. If you are unsure which folder that is, check the working-directory or folder-selection context in your environment before falling back. Do not use an internal agent scratchpad or temporary outputs directory for these files.

**Setup at the start of every research task:**

```bash
mkdir -p "<user_selected_folder>/saved cases"
```

If no user-visible folder is available (e.g., a pure-chat session with no mounted folder), skip the save step and rely on `opinion_view` for inline retrieval. Note this to the user so they know no archive was produced.

**Naming convention** (use this so files are sortable and self-describing):

```
<cluster_id>_<short_case_name>_<reporter_cite>.md
```

Example: `107252_miranda_v_arizona_384_US_436.md`

Sanitize names: lowercase, replace spaces with underscores, strip punctuation other than underscores and dots, drop "v." → "v".

## Phase 1: Strategic Search (Cast a Wide Net)

Run 3–5 different search strategies in parallel to maximize coverage. Different strategies catch different cases; relying on one query is how you miss the on-point authority.

### A. Natural Language Keyword Search (`opinion_search`)
```json
{"query": "vehicle warrant automobile exception traffic stop",
 "court_ids": "scotus", "filed_after": "2010-01-01"}
```

### B. Boolean / Phrase Search (`opinion_search`)
```json
{"query": "(automobile OR vehicle) AND warrant* AND \"probable cause\"",
 "court_types": "F", "precedential_status": "published"}
```

### C. High-Authority Anchor Search (`opinion_search`)
```json
{"query": "[core legal issue]", "court_ids": "scotus",
 "order_by": "-citeCount", "page_size": 20}
```

### D. Jurisdiction-Specific (`opinion_search`)
```json
{"query": "[issue]", "court_types": "S,SA", "states": "TX,CA,NY"}
```

### E. Field-Specific via `courtlistener_full_search`
```json
{"type": "o", "q": "court_id:scotus AND \"qualified immunity\"",
 "order_by": "-citeCount"}
```

**Court type codes**: F = federal circuit, FD = federal district, FB = federal bankruptcy, S = state supreme, SA = state appellate, ST = state trial.
**SCOTUS**: use `court_ids: "scotus"` (it's a court ID, not a court type).
**States**: 2-letter codes (TX, CA, NY).
**Boolean syntax**: `AND`, `OR`, `NOT`, `-`, parentheses, `"exact phrase"`, `term*` (wildcard), `term~2` (fuzzy).

Collect cluster IDs from the snippets. Aim for 15–30 candidates across your strategies before moving to Phase 2.

## Phase 2: Triage and Retrieve via `opinion_store`

Triage candidates by reading their search snippets, then bulk-retrieve the promising ones in a single `opinion_store` call.

### Step 2a: Triage from snippets

From your Phase 1 search results, rank candidates by how clearly the snippet engages the specific legal question. Look for:
- Direct doctrinal language (the rule statement, the test, the elements).
- The court's own articulation of the issue (not a party's argument).
- Procedural posture that matches your problem.
- Recency where the area is evolving; foundational age where the area is settled.

Discard snippets that only tangentially mention the keywords. You want roughly **10–20 cases worth reading in full**.

### Step 2b: Bulk retrieve with `opinion_store`

Call `opinion_store` with up to 25 cluster IDs at a time. It returns a download URL per case — each URL serves the opinion as markdown and is valid for one hour.

```json
{"cluster_ids": ["107252", "108713", "117150", "..."]}
```

### Step 2c: Save each opinion to `saved cases`

For each returned URL, download with `curl` and save under the naming convention above. Run downloads in parallel — they are independent.

```bash
cd "<working_dir>/saved cases"

# Example: one download per case. Use the cluster_id + case name you already know from search results.
curl -sSL "<url_from_opinion_store>" -o "107252_miranda_v_arizona_384_US_436.md"
curl -sSL "<url_from_opinion_store>" -o "108713_terry_v_ohio_392_US_1.md"
# ...etc
```

If a URL expires before you finish (the 1-hour window lapses), call `opinion_store` again for the remaining cluster IDs — URLs are cheap to regenerate.

### Step 2d: Read what you saved

Open each saved markdown file with `Read` (or `cat` via bash). This is where actual analysis happens. Look for:
- The court's holding (the rule, not the disposition).
- The reasoning path (why the rule applies).
- Pinpoint-citable quotes.
- The case's posture toward your specific issue (helpful, harmful, distinguishable).

If a case turns out to be off-point on close reading, note that briefly and move on — don't pad the analysis.

### When to use `opinion_view` instead

Use `opinion_view` when you need a single case's text inline and either (a) you have no local directory, or (b) you only need a quick look and don't want to keep a copy. `opinion_view` accepts reporter citations directly (e.g., `"347 U.S. 483"`), which is handy when the user gives you a citation rather than a cluster ID.

```json
{"identifier": "347 U.S. 483"}
```

Prefer `opinion_store` for any case you'll actually quote from or analyze — having the markdown on disk saves tokens and lets the user verify.

## Phase 3: Build the Case Network

Once you have your core set of on-point cases, expand the network so you can speak to how the doctrine has been applied and whether it still holds.

### Find recent applications and treatment (`show_citing_opinions`)
```json
{"identifier": "[citation or cluster_id]", "court_types": "F,FD",
 "limit_results": 20, "order_by": "-dateFiled"}
```
Use this to confirm the case is still good law, surface circuit splits, and find recent applications worth citing.

### Find topically related cases (`show_related_opinions`)
```json
{"identifier": "[cluster_id]", "court_ids": "scotus",
 "limit_results": 15, "order_by": "-citeCount"}
```
Use this to catch authoritative cases that don't share keywords with your query but address the same doctrine.

When a citing or related case looks important, run it through Phase 2 (retrieve via `opinion_store`, save to `saved cases`, read). Don't quote citing-result snippets directly.

## Phase 4: Validate

Before writing anything for the user, run this checklist:

- Did I retrieve full text (not just snippets) for every case I plan to discuss?
- Do I have the verified citation, court, and year for each?
- For every quote, do I have a pinpoint page?
- Have I checked whether key cases were overruled, abrogated, or limited? (Try a citing-opinions search with terms like `overruled OR abrogated OR "no longer good law"`.)
- For each holding I state, can I point to the exact paragraph in the saved markdown?

If any answer is "no," go back and fix it before drafting.

## Phase 5: Synthesize the Answer

Structure your written output like this:

1. **Answer** — Direct response to the research question, in 1–3 sentences.
2. **Primary Authority** — The 3–5 most on-point cases. For each:
   - *Case Name*, Citation (Court Year)
   - Holding: [the rule the case stands for, in your words]
   - Key Quote: "[exact quote]" *Id.* at [page].
   - Cluster ID: ######
3. **Supporting Authority** — Cases that reinforce or extend the primary authority.
4. **Contrary Authority** — Conflicting holdings, distinguishable cases, or limits on the rule. Engage honestly; do not hide adverse authority.
5. **Trends and Open Questions** — Circuit splits, recent shifts, unresolved issues.

## Phase 6: Comprehensive Case Table

Include a table of **every case for which you retrieved text**, even ones that ended up tangential. This lets the user audit your work and reuse cases later.

| Case Name & Citation | Cluster ID | Relevant Quote(s) | Local File |
|---|---|---|---|
| *Brown v. Board of Educ.*, 347 U.S. 483 (1954) | 107252 | "Separate educational facilities are inherently unequal." *Id.* at 495. | `107252_brown_v_board_347_US_483.md` |
| *Miranda v. Arizona*, 384 U.S. 436 (1966) | 108713 | "The prosecution may not use statements … stemming from custodial interrogation … unless it demonstrates the use of procedural safeguards." *Id.* at 444. | `108713_miranda_v_arizona_384_US_436.md` |
| *United States v. Ross*, 456 U.S. 798 (1982) | 117150 | "Police officers who have legitimately stopped an automobile and who have probable cause to believe that contraband is concealed somewhere within it may conduct a warrantless search." *Id.* at 799. | `117150_us_v_ross_456_US_798.md` |

**Table requirements:**
- Full case name in italics.
- Complete citation with year.
- The most useful quote(s) with pinpoint pages.
- Order by relevance (most relevant first) — or chronologically if the user is tracing doctrinal development.
- If the `saved cases` folder is in play, include the local filename so the user can open it directly.

## Quick Reference

### Search optimization
- **Too few results?** Drop date filters, broaden terms, use fuzzy match (`~`), try a synonym set.
- **Too many results?** Add `court_types`, `states`, date ranges, or sort by `-citeCount`.
- **Looking for circuit splits?** Try queries like `"circuit split" OR "conflict among circuits" OR "we disagree with"`.
- **Checking validity?** Search `overruled OR abrogated OR "no longer good law"` against the cluster.

### Retrieval choice
- **`opinion_store`** — Bulk retrieval (1–25 cluster IDs). Returns markdown URLs. Use whenever you have a local folder; save to `saved cases`.
- **`opinion_view`** — Single-case, inline text. Use when no local folder, when working from a reporter cite the user gave you, or for a quick spot check.

### Common workflow patterns
```text
# Constitutional issue
1. opinion_search: court_ids="scotus", filed_after="2000-01-01"
2. opinion_search: court_types="F", filed_after="2015-01-01"
3. show_citing_opinions on the anchor SCOTUS case → circuit splits

# Statutory interpretation
1. opinion_search: "18 U.S.C. 1001" AND interpret*
2. opinion_search: "18 U.S.C. 1001" AND "legislative history"
3. opinion_store the top results, read for the operative construction

# State law question
1. opinion_search: court_types="S", states="TX"
2. opinion_search: court_types="SA", states="TX"
3. opinion_search across federal courts applying Texas law (Erie context)
```

### Quality checklist
- [ ] Multiple search strategies run, not just one.
- [ ] 15–30 candidates triaged before retrieval.
- [ ] `saved cases` folder created and populated with markdown.
- [ ] Full text retrieved (not snippets) for every case I discuss.
- [ ] Citations verified, including cluster IDs.
- [ ] Quotes have pinpoint page citations.
- [ ] Both binding and persuasive authority weighed.
- [ ] Validity checked via `show_citing_opinions`.
- [ ] Case table includes every retrieved case.

## Remember

Quality beats quantity. Five truly on-point cases serve the user better than fifty tangential ones. Show your work: full citations, pinpoint quotes, a local archive the user can open, and an honest account of contrary authority.
