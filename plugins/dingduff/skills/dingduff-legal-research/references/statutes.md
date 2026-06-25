# Statutory Research

Method for mapping the statutory landscape on an issue — every relevant code section, the definitional architecture, the cross-references, and the judicial gloss on any ambiguous or outcome-controlling language — so the user can rely on the map with no missing chapters and no defined term silently reshaping the answer. Validate currency per `validity.md`.

## The working set

Maintain **Read** (sections retrieved via `codes_view` and analyzed), **Frontier** (sections, chapters, or keyword leads not yet pulled), and **Pruned** (skipped, with a reason). Each pass moves frontier → read and generates new frontier from cross-references, defined terms, and adjacent sections.

## 1. Jurisdiction and scope

Confirm the jurisdiction's codes are available: `codes_browse {"jurisdiction": "TX"}`. If none are returned, say so and ask how to proceed. Set breadth from the question (wider for a "regime/scheme/framework" or bet-the-matter question; tighter for one well-defined hook or a single defined term).

## 2. Bidirectional code mapping (run both directions)

**Top-down (hierarchy):**
1. List codes for the jurisdiction (`codes_browse {jurisdiction}`).
2. Identify the codes likely to govern (business/corporate → Business Organizations; real property → Property; criminal → Penal / Crim. Proc.; civil procedure → Civil Practice & Remedies; family → Family; tax → Tax; agency regulation → that agency's code). When unsure, browse any code whose name plausibly touches the issue — over-inclusion here is cheap.
3. Drill titles → divisions → chapters → subchapters → sections (`codes_browse` with `code_id`/`node_id`); document the hierarchy (you need it for the tree).
4. Pull section text where the title/context suggests relevance (`codes_view {"statute_id": "TX/business_organizations/21.401"}`); save to `saved statutes/`.

**Bottom-up (keyword):**
1. Text search — `codes_search {"jurisdiction":"TX","search_type":"text","query":"shareholder derivative action","limit":25}`. Run several queries (exact phrases, individual keywords, synonyms — statutes use idiosyncratic terms).
2. Title search — `codes_search {"search_type":"title","query":"derivative"}` surfaces whole chapters on the issue.
3. For any hit, browse the parent chapter and adjacent sections — related provisions are nearly always grouped.

**Reconcile:** every bottom-up hit should appear in your top-down hierarchy (or be added); every relevant top-down section should be caught by some keyword search (if not, broaden the keywords).

**Regulations** are handled the same way: administrative/agency codes (a state administrative code, or the C.F.R. for federal regulations) are browsed and retrieved with the same `codes_browse` / `codes_view` tools, and mapped, defined, and currency-checked just like statutes. Where a statute delegates to an agency, follow the cross-reference into the regulatory code.

## 3. Definition discovery

Definitions control interpretation and are often where the answer lives. Pull: **code-wide** definition sections (`codes_search {"search_type":"title","query":"definitions"}`; often section .001/.01); **chapter/subchapter** definitions (these supersede general ones for that chapter); **in-line** definitions ("As used in this section…"). Flag **definitional conflicts** — the same term defined differently across chapters/codes — and identify which governs the fact pattern. Document every applicable definition.

## 4. Flag phrases that need interpretation

Read the collected sections and flag every phrase that is: **ambiguous on its face**; **outcome-controlling**; a **term of art** set by case law ("reasonable suspicion," "good faith," "in the course of employment," "knowingly"); **definitionally underspecified**; **recently amended** (prior constructions may or may not still apply); or **cross-referenced** to another section/code/doctrine. For each, record the section, the phrase, why interpretation is needed, and the question you'll put to the case law. If nothing needs interpretation, that's a finding — say the text is unambiguous for this question and skip step 5.

## 5. Targeted interpreting case law

This is a *bounded* pull — the judicial gloss on each flagged phrase, not a full citation network (that's `case-law.md` if it's warranted). For each phrase:
- Search interpreting decisions, best by statutory cite + exact phrase: `opinion_search {"query":"\"Tex. Bus. Orgs. Code § 21.401\" AND \"interest of the corporation\"","court_types":"S,SA,F,FD","order_by":"-citeCount"}`. For state statutes focus on the state high court + intermediate appellate; for federal, SCOTUS + the relevant circuit (don't ignore federal courts construing state law in Erie posture).
- Aim for **5–15 cases per phrase**, weighted to most-cited and most-recent. Triage from snippets; bulk-retrieve via `opinion_store`; save to `saved cases/`; read.
- Extract the gloss: the court's articulation of the phrase's meaning (test/elements/rule), a pinpoint quote, whether binding or persuasive, and any conflict in the set.
- Validity-check each retained case (`validity.md`).
- **Escalate** if a phrase turns out to sit on a sprawling, contested body of case law — say so and run the full case-law method on it as a focused follow-up rather than letting this silently become a network build.

## 6. Recurse until saturated

Steps 2–5 iterate — each adds sections, surfaces cross-references and defined terms, raises new flagged phrases. Stop when: searches return only already-read sections; every plausibly-relevant code is browsed; every controlling defined term is pulled; every cross-reference is resolved or pruned; every flagged phrase has a gloss or an explicit "no controlling interpretation" note; currency is checked. If the read set passes ~50 sections, the scope was too broad — narrow and re-anchor.

## Output format (statutory deliverable)

1. **Executive summary** — jurisdiction; question framed; codes reviewed; sections identified vs. viewed (counts); headline answer (2–4 sentences).
2. **Statutory tree** — the hierarchy mapped, viewed sections marked:
   ```text
   Business Organizations Code
   └─ Title 2: Corporations
      └─ Ch. 21: For-Profit Corporations
         └─ Subch. L: Derivative Proceedings
            ├─ § 21.551 Definitions (viewed)
            └─ § 21.552 Standing (viewed)
   ```
3. **Key provisions analysis** — the 5–15 driving sections (citation; one-line function; operative language with subsection pin; interactions).
4. **Applicable definitions** — section, term, operative definitional language; conflicts flagged with which controls.
5. **Judicial interpretation of flagged phrases** — phrase, section, controlling/best case(s), the rule extracted, a pinpoint quote (or an explicit "no controlling interpretation").
6. **Cross-references and interconnections** — how the sections fit; where one depends on another; cross-code definitional reach.
7. **Issue-specific findings** — the direct answer, mapping each question to its controlling sections + cases.
8. **Currency and validity notes** — effective dates, amendment indicators, interpreting-case validity (brief; show the work).
9. **Practitioner's roadmap** — read these sections first, in this order; check these definitions; watch these traps.

**Comprehensive tables** (the audit trail — every section and interpreting case retrieved):

| Citation | Statute ID | Role | Status | Operative Language | Local File |
|---|---|---|---|---|---|
| Tex. Bus. Orgs. Code § 21.552 | TX/business_organizations/21.552 | Primary | Effective | "A shareholder may not commence or maintain a derivative proceeding unless…" | `tx_business_organizations_code_21.552.md` |

## Tool quick reference

- `codes_browse` — hierarchy (no args = jurisdictions; `{jurisdiction}` = codes; `{code_id}`/`{node_id}` = drill down).
- `codes_search` — keyword (`search_type:"title"` for chapter/section discovery; `"text"` for substantive language; max `limit:25`).
- `codes_view` — full section text (`statute_id` = `jurisdiction/code/section`).
- `metadata_view` — section metadata (effective date / version where available — see `validity.md`).
- `opinion_search` / `opinion_store` / `opinion_view` / `show_citing_opinions` — step 5 interpreting cases (see `case-law.md`).
