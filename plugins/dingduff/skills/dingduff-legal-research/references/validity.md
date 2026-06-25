# Validity and Currency

The verification discipline — confirming that every authority you rely on is *still good law*. The databases do **not** flag overturned/abrogated cases or guarantee real-time tracking of statutory amendments, so you do this yourself, every time, before any authority becomes part of an answer. This is the difference between research and a snippet dump.

## The overturn problem (cases)

For every case you intend to rely on:

1. Run `show_citing_opinions` against it, ordered by `-dateFiled`, and read the snippets of recent citing cases:
   ```json
   {"identifier": "<reporter cite or cluster_id>", "order_by": "-dateFiled", "limit_results": 20}
   ```
2. Scan for **treatment signals**: "abrogated," "overruled," "is no longer good law," "rejected," "declined to follow," "limited to its facts," "called into doubt," "superseded by statute." Treat any as a red flag.
3. Cross-check with a direct search: `opinion_search` for `"<case name>" AND (overruled OR abrogated OR "no longer good law")`.
4. If you find adverse treatment, retrieve the treating case via `opinion_store`, read it, and determine the **scope** — full overruling, partial abrogation, narrowing, or mere distinguishing.
5. For foundational SCOTUS or controlling appellate cases, check at least the ~20 most recent citing cases.

If a case has been overruled or substantially abrogated, **do not present it as good law** — note the treatment, explain the current rule, and cite the case that did the overruling. A non-controlling or overruled case presented as authority is the worst failure mode in legal research.

Also confirm, for each main proposition, a **recent application** exists (within ~5 years, or the most recent available if the doctrine is dormant) — this shows the rule is alive, and surfaces recent narrowing.

## Currency and amendments (statutes and regulations)

Code databases store statutory and regulatory text as imported and may lag amendments or repeals:

- When `codes_view` returns a section, note any effective-date / version annotation it carries (or retrieve section metadata via `metadata_view`).
- Where the statutory text drives the answer, run a recency check: `opinion_search` for recent cases citing the section — if a case discusses an amended version different from the text you have, flag it.
- For federal statutes especially, surface the text you found and flag possible amendments for the user to confirm against an authoritative `.gov` source.
- Watch for **"superseded by statute"** treatment of cases that construed a prior version of the text — the old gloss may no longer apply.
- **Regulations** (agency/administrative codes, the C.F.R.) are amended and repealed too — check their effective dates and any superseding amendments the same way, and confirm the agency hasn't revised the rule since the database's import.

Never silently rely on a stale version of a statute.

## The verification pass (before drafting any answer)

Run through every authority you plan to cite in a primary/anchor/controlling role:

- [ ] Each case run through `show_citing_opinions` (`-dateFiled`) and screened for treatment signals.
- [ ] Any adverse-treatment signal chased down — treating case retrieved, read, and its scope determined.
- [ ] A recent application located for each main proposition (or dormancy noted).
- [ ] No more-recent controlling case from the same court (or higher) supersedes a case you rely on.
- [ ] Statutory sections checked for effective-date/amendment annotations; stale text flagged.
- [ ] Interpreting cases (from statutory research) validity-checked the same way.

Record the checks briefly in the output (a "validity confirmations" note for cases; "currency and validity notes" for statutes) so the reader can see the work was done — not just trust that it was.
