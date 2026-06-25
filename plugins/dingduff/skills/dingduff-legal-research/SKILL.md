---
name: dingduff-legal-research
description: Research the law on a question — find, retrieve, read, and validate the controlling cases, statutes, and regulations; map the citation network and the statutory landscape; and verify everything is still good law. Use for ANY legal-research task — "what's the law on X," "find cases/statutes on Y," "research precedent," "is this still good law," "map the statutory scheme," "what does § __ mean" — and as the authority-gathering step behind any analysis, memo, or brief. Research is thorough by default. It interleaves with dingduff-legal-analysis (analysis guides research; research guides analysis) and feeds dingduff-legal-writing. Method detail for case law, statutes, and validity lives in references/ and is loaded as needed. (v2.1)
---

# Legal Research

One skill for finding and verifying legal authority — case law, statutes, and regulations. It produces a reliable, citation-anchored body of authority you can build an analysis or a document on, having personally confirmed it is still good law. Research here is **thorough by default**: assume the user wants the full picture, not a single snippet. Keep this file in context; pull in a `references/` file for the method you need.

This skill runs on the DingDuff research tools (CourtListener + code databases): `opinion_search`, `courtlistener_full_search`, `opinion_store`, `opinion_view`, `show_citing_opinions`, `show_related_opinions` for cases; `codes_browse`, `codes_search`, `codes_view`, `metadata_view` for statutes/regulations.

## CRITICAL: Retrieve before you assert (anti-hallucination)

**Never** state a holding, quote any language, or recite statutory text from a search snippet. Snippets only help you decide what to retrieve — they are not citable substance.

- Cases: retrieve the actual opinion via `opinion_store` (preferred — saves a local copy) or `opinion_view`, then cite by reporter citation + pinpoint page (*Miranda v. Arizona*, 384 U.S. 436, 444 (1966)). Cluster IDs are internal retrieval handles — keep them in your notes, never in user-facing citations.
- Statutes: retrieve the full section via `codes_view`, then cite by proper statutory citation (Tex. Bus. Orgs. Code § 21.401(a); 18 U.S.C. § 1001(a)(2)). `statute_id` stays internal.
- If you cannot retrieve a source's text, do not discuss its substance — note the gap and move on.

## CRITICAL: Verify it's still good law

The databases do **not** flag overturned, abrogated, or limited cases, and do not guarantee real-time tracking of statutory amendments. You must check, yourself, for every authority you will rely on — overturn/treatment checks for cases, currency/amendment checks for statutes. This is the single discipline that separates real research from a snippet dump. Method in `references/validity.md`; do it before anything you find becomes part of an answer.

## Research and analysis interleave (the recursive loop)

Research and analysis are one intertwined process, not two phases. **Analysis guides research** (you research the specific issues, elements, and ambiguous terms the analysis has framed) and **research guides analysis** (what you find reshapes the issues, the rule, and the framing — a new exception, a circuit split, a controlling definition, an issue that turns out to be moot).

So do not treat research as a single up-front pass. Loop:

1. Start from the framed issues (from `dingduff-legal-analysis`; if none exist yet, frame them lightly first).
2. Research them (cases and/or statutes, below).
3. Hand findings to analysis — let it synthesize the rule, analyze the facts, structure the proof.
4. **Return to research whenever analysis surfaces a new question** — an ambiguous controlling term needing its judicial gloss, a newly-spotted sub-issue, a missing element, a needed counter-authority, an adverse case to confirm.
5. Repeat until **both** the research network is saturated **and** the analysis has no unresearched gaps.

`dingduff-legal-analysis` escalates *back* to research when it hits a hole; this skill closes the loop by sending you *forward* into analysis and back again. Neither is done until both are done.

## Calibrate scope to the question

Thorough by default — but set the breadth to the question. A regime-mapping, bet-the-matter, or appellate question gets the full sweep (deep citation network; complete statutory map). A tightly-bounded question (one well-defined hook, one defined term) gets a focused pass — don't expand a one-section lookup into a 100-case network. If a network grows past ~75–100 cases or ~50 statute sections, the issue was scoped too broadly: narrow it (to an element, jurisdiction, or fact pattern) and re-anchor. Rank what you find by **weight of authority** (binding > persuasive; higher court > lower; more recent and on-point > older and tangential) and spend your effort there.

## Local storage: saved cases / saved statutes

When the user has connected a folder, create archive subfolders in it and save every retrieved opinion and section as markdown — a durable record for the user and a way for you to re-read without spending more tool calls.

```bash
mkdir -p "<user_folder>/saved cases"
mkdir -p "<user_folder>/saved statutes"
```

Naming: cases `<cluster_id>_<short_case_name>_<reporter_cite>.md` (e.g., `107252_miranda_v_arizona_384_US_436.md`); statutes `<jurisdiction>_<code>_<section>.md` (e.g., `us_18_usc_1001.md`). Sanitize: lowercase, spaces → underscores, strip punctuation except underscores/dots, "v." → "v". If no folder is available, fall back to inline retrieval (`opinion_view` / `codes_view`) and tell the user no archive was produced.

## Workflow

1. **Take the issues** — from `dingduff-legal-analysis`, or frame them lightly. Decide whether the question is statute-driven, case-law-driven, or both.
2. **Statutes & regulations** (when a statutory or regulatory scheme governs) — map the code bidirectionally, pull definitions, flag phrases needing interpretation. → `references/statutes.md`
3. **Case law** — search broadly, then map the citation network (back to the anchor, forward to current applications, plus a topical sweep). → `references/case-law.md`
4. **Validate** everything you'll rely on — overturn checks for cases, currency for statutes. → `references/validity.md`
5. **Interleave with analysis** (the loop above) — feed findings to `dingduff-legal-analysis`; return here for each new question it surfaces. Continue until saturated and gap-free.
6. **Synthesize** — present the authority with its current-validity status. Output formats (doctrinal genealogy + network diagram + case table for cases; statutory tree + roadmap + section table for statutes) are in the domain references.

## References map

- `references/case-law.md` — finding cases (search strategies, tool patterns), mapping the citation network (ancestors / descendants / topical sweep), the working set, and the case-law output format (genealogy, network diagram, case table).
- `references/statutes.md` — jurisdiction/scope check, bidirectional code mapping (top-down hierarchy + bottom-up keyword), definition discovery, flagging phrases that need interpretation, targeted interpreting case law, and the statutory output format (tree, roadmap, section table).
- `references/validity.md` — the overturn problem and the case-validity check; statutory currency and amendment checks; the verification pass before any authority enters an answer.

## Related skills

Interleaves with `dingduff-legal-analysis` (the reasoning it feeds and takes direction from). Downstream: `dingduff-legal-writing` (drafts from the authority + analysis). QC: `dingduff-legal-citation-format`, `dingduff-citation-check`.
