# Case Law Research

Method for finding the controlling and persuasive cases on an issue and mapping the citation network until you can speak to where the rule came from, what it says now, how it has been applied, and where it is contested. Validate everything per `validity.md`.

## The working set (keep it tractable)

Citation networks expand fast. Maintain three running lists (in your head or a scratch file in `saved cases/`):
- **Read** — cases retrieved, opened, analyzed.
- **Frontier** — cases identified as worth retrieving, not yet read.
- **Pruned** — cases considered and skipped, each with a one-line reason (off-topic, distinguishable on irrelevant grounds, redundant with stronger authority).

Each iteration moves frontier → read, generates new frontier candidates from what you read, and prunes dead ends. Done when the frontier is empty or only redundant.

## 1. Strategic search (cast a wide net)

Run 3–5 different strategies — each catches cases the others miss:
- **Natural language** — `opinion_search` with the issue in plain language plus `court_ids`, `court_types`, `states`, date filters.
- **Boolean / phrase** — `opinion_search` with Boolean operators and exact doctrinal phrases.
- **High-authority anchor** — `opinion_search` with `court_ids: "scotus"` and `order_by: "-citeCount"` to find the foundational treatment.
- **Jurisdiction-specific** — `court_types` + `states` filters for the operative jurisdiction.
- **Field-specific** — `courtlistener_full_search` with `type: "o"` and field-scoped queries (e.g., `court_id:scotus AND "qualified immunity"`).

Court-type codes: F = federal circuit, FD = federal district, FB = bankruptcy, S = state supreme, SA = state appellate, ST = state trial; SCOTUS = `court_ids: "scotus"`.

Triage candidates from snippets (snippets are *only* for triage — see anti-hallucination). Bulk-retrieve the promising ones (up to 25 per call) via `opinion_store`; download each returned URL with `curl` into `saved cases/` (URLs expire in ~1 hour — regenerate if needed). Read each; note holdings/reasoning/quotable language, and mark every case it cites *on the focus issue* as a frontier candidate.

## 2. Backward tracing (ancestors → the anchor)

Trace the doctrine to its source. From each read case, list the cases it cites in connection with the focus issue; resolve those cites to cluster IDs (`opinion_search`/`opinion_view`); bulk-retrieve, save, read; recurse. Stop a branch when a case cites no earlier authority on the issue, cites only general/unrelated authority, or is the case multiple branches converge on (a strong anchor signal). **Document the anchor case(s) explicitly** — the reader needs to know where the rule comes from.

## 3. Forward tracing (descendants → current law)

From each pivotal case, run `show_citing_opinions`:
```json
{"identifier": "<reporter cite or cluster_id>", "court_types": "F,FD,S,SA",
 "limit_results": 30, "order_by": "-dateFiled"}
```
Order by `-dateFiled` first (this doubles as the overturn check — see `validity.md`), then a pass by `-citeCount` for the most influential applications. In the snippets, look for cases that **apply**, **narrow**, **criticize**, **extend**, or **follow** the rule — and for adverse-treatment signals. Add informative cases to the frontier; prune the rest with a reason; retrieve, save, read, and recurse (run `show_citing_opinions` on significant descendants too). The forward network branches fast — lean on pruning.

## 4. Topical sweep

`show_related_opinions` finds cases related by subject matter, not citation — catching on-point authority your keywords and citation chains miss. Run it on your two or three most central cases:
```json
{"identifier": "<cluster_id>", "court_ids": "scotus", "limit_results": 20, "order_by": "-citeCount"}
```
Triage; new cases to the frontier, off-point ones pruned.

## 5. Recurse until saturated

Phases 2–4 are loops, not one-shots. Keep going until: new expansions return cases already read (saturation); the anchor is identified and branches converge on it; each main proposition has a recent application located; every case you'll rely on has been validity-checked; the major exceptions/qualifications are mapped. Don't stop while the anchor is unidentified, a meaningful citing branch is unread, a foundational case is unverified, or a hint of a circuit split is unrun.

## Output format (case-law deliverable)

1. **Answer** — the rule and its current status, in 2–4 sentences.
2. **Doctrinal genealogy** — a short narrative from the anchor forward to the modern formulation.
3. **Anchor / source authority** — the 1–3 cases that established the rule (name, cite, what it decided, key pinpoint quote).
4. **Primary authority (current law)** — the 3–7 cases stating the current rule (cite, holding, pinpoint quote, validity status).
5. **Supporting authority** — cases that reinforce, extend, or apply the rule informatively.
6. **Contrary / limiting authority** — adverse, distinguishable, narrowing, or critical cases. Engage honestly; this is what makes research trustworthy.
7. **Trends and open questions** — splits, recent shifts, unresolved issues.
8. **Validity confirmations** — brief notes on the overturn checks performed (show the work).

**Citation network diagram** (Mermaid): anchors at top, descendants flowing down, focus case marked (★/bold), adverse edges labeled (`-->|abrogated by|`), short cite + year on each node. Split by sub-doctrine if too large.

**Comprehensive case table** — every case for which you retrieved text (not just those cited):

| Case Name & Citation | Cluster ID | Role | Validity | Key Quote(s) | Local File |
|---|---|---|---|---|---|
| *Brown v. Board of Educ.*, 347 U.S. 483 (1954) | 107252 | Anchor | Good law | "Separate educational facilities are inherently unequal." *Id.* at 495. | `107252_brown_v_board_347_US_483.md` |

Role = Anchor / Primary / Supporting / Contrary / Pruned-but-considered. Sort by role, then date.

## Tool quick reference

- `opinion_search` / `courtlistener_full_search` — discovery.
- `opinion_store` — bulk retrieval (1–25 cluster IDs); markdown URLs valid ~1 hr; save to `saved cases/`.
- `opinion_view` — single-case inline retrieval (or from a reporter cite); good for a quick spot check.
- `show_citing_opinions` — forward tracing and the workhorse of the overturn check.
- `show_related_opinions` — topical sweep for cases the citation chains miss.
