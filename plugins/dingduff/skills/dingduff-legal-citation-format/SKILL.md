---
name: dingduff-legal-citation-format
description: >-
  Format legal citations in the style courts expect (briefs, motions,
  memoranda, pleadings). Use when drafting, inserting, or fixing a citation to
  a case, statute, constitution, regulation, rule, secondary source (treatise,
  law review, etc), or a same-matter filing — or when a draft needs signals
  (e.g. see, cf., but see), pincites, short forms (id./supra), string cites,
  explanatory parentheticals, or quotation formatting (block quotes,
  alterations, omissions). Trigger whenever the user is writing or revising a
  legal document that relies on authority and wants its citations to look
  right or when a citation looks malformed. Rules follow The Indigo Book.
  COVERS FORM ONLY: it does not
  verify that an authority exists, is good law, or is quoted accurately; pair
  it with primary-source verification (separate skill). NOTE: This skill and
  reference files are large, so run it in a subagent — delegate the formatting
  task rather than loading the full skill into the main context window. (v1.4)
---

# Legal Citation Format — Practitioner / Brief Style

This skill produces citations in the conventional **practitioner format** — the style used in **standard legal documents (SLDs)**: documents filed with a court (briefs, motions, memoranda, pleadings) and documents lawyers write to one another or the public (opinion letters, legal memoranda). That format is intentionally simpler than the **academic style** used in law review articles (ALDs), and it is close enough to uniform across U.S. jurisdictions that one generic standard works for almost everything an attorney files. The rules below state the SLD form; where a law-review (ALD) convention differs, that is flagged.

## Source and attribution

The rules and examples in this skill are based on, and written to be consistent with, **_The Indigo Book: A Manual of Legal Citation_** (Sprigman et al., Public Resource 2016) — a free, open-source implementation of the same Uniform System of Citation that *The Bluebook* implements. *The Indigo Book* is dedicated to the public domain under a CC0 dedication, and the citation system it restates ("a uniform system of citation") consists of facts and methods that no one owns. Where this skill addresses the consolidated "(cleaned up)" quotation parenthetical, it also follows the approach adopted in *The Indigo Book*'s second edition (Romig et al., 2021/2022).

This skill is an **original document**, not a copy or reproduction of *The Indigo Book*. It restates and adapts the citation rules in our own words and with our own (illustrative) examples, for use in practice. *The Indigo Book* is not affiliated with or authorized by *The Bluebook® A Uniform System of Citation®*, and neither is this skill. Citations produced under this guide are compatible with the Uniform System of Citation. For any rule this skill does not reach, consult *The Indigo Book* (https://law.resource.org/pub/us/code/blue/IndigoBook.html) or a full citation manual.

*Version 1.4 — reconciled with The Indigo Book.*

## Before anything else: defer to controlling local rules

A court's own rules, a standing order, or a jurisdiction-specific style manual always wins. Many courts modify citation form in small ways (preferred reporters, parallel-citation requirements, how record cites look, whether citations may sit in footnotes). When the user names a court or jurisdiction, follow its rules and treat the standard below only as the gap-filler. When nothing court-specific is in play, the generic format here is the safe default.

## How practitioner style differs from academic style

This is the single most common source of "wrong-looking" citations, so internalize it:

- **Two typefaces, not three.** Court documents use only ordinary roman type and *italics* (equivalently, <u>underlining</u>). The large-and-small-caps used in law review footnotes for author names and book/journal titles **do not appear** in a brief. An author's name and a journal name are set in ordinary roman.
- **Case names are italicized** in citations and in text (academic style leaves them roman in the main text). 
- **Citations live in the body text**, immediately after the proposition they support — not in footnotes — unless local rules say otherwise.

Pick *italics* or underlining and use it consistently throughout the document. Italics is the modern default; some judges and older local practice prefer underlining. They are exact equivalents — never mix them in one document.

## Workflow for any citation task

1. **Identify the authority type** (case, statute, constitution, regulation, rule, legislative material, secondary source, or a filing in the same matter). Each has its own pattern — see the quick reference below and the linked reference files.
2. **Build the full citation the first time** the authority appears.
3. **Switch to a short form** for every later reference (see `references/short-forms-and-quotations.md`).
4. **Place the citation** as a citation *sentence* or citation *clause*, add an introductory *signal* if the relationship isn't direct, and add an explanatory *parenthetical* if it helps (see `references/signals-and-structure.md`).
5. **Apply typeface rules** — italicize what should be italicized (below), nothing more.
6. **Verify the details** against the relevant reference file before finalizing — abbreviations, spacing, and punctuation are where citations most often go wrong.

When the task is to clean up an existing document, read the citations, diagnose each against these rules, and fix form without changing the substance (volume, page, court, year, quotation text).

## What to italicize (court-document typeface)

Italicize (or underline):

- Case names, including the *v.* and any procedural phrase that is part of the name (*In re*, *Ex parte*, *... ex rel. ...*). The comma **after** the case name is roman, not italic.
- Introductory signals (*See*, *Cf.*, *But see*, *e.g.*, etc.).
- *id.*, *supra*, *infra*, and similar cross-reference words.
- Phrases introducing case history (*aff'd*, *rev'd*, *cert. denied*, *sub nom.*, etc.).
- Words introducing related authority (*quoting*, *citing*, *quoted in*).
- Titles of books, articles, and other standalone works.
- In running text: titles of periodicals, words that were italicized in the original of a quotation, and non-English words not in common English usage.

Do **not** italicize: reporter abbreviations, anything in a statute or constitution citation (nothing in those is italicized), court/jurisdiction abbreviations, or the publisher/date parenthetical.

## Quick reference — the citations you build most often

These cover the large majority of brief cites. Full detail and edge cases are in the reference files.

### Cases (full citation)

Pattern: `<Case Name>, <Volume> <Reporter> <First Page>, <Pincite> (<Court> <Year>) (<parentheticals>)<, history>.`

- U.S. Supreme Court: *Alvarez v. United States*, 571 U.S. 320, 331 (2014).
- Federal court of appeals: *Vasquez v. Coastal Freight Co.*, 640 F.3d 200, 207 (9th Cir. 2011).
- Federal district court: *Okafor v. Summit Indus., Inc.*, 305 F. Supp. 3d 410, 418 (S.D. Tex. 2018).
- State high court (regional reporter): *Whitman v. Harbor Mut. Ins. Co.*, 431 P.3d 220, 224 (Cal. 2018).
- State intermediate court: *Marsh v. Cedar Valley Hosp.*, 215 S.W.3d 700, 705 (Tex. App. 2006).

(Party names, volumes, and pages in these examples are illustrative — they show form, not real cases.) Notes: the U.S. Supreme Court takes **no court abbreviation** — the year alone sits in the parenthetical. A state's highest court likewise takes no court name; include the state in the parenthetical when you cite a regional reporter, and give the year alone only when the official state reporter already names the state. A footnote pincite is `, 226 n.4` with no space inside `n.4`. If the pincite is the first page of the opinion, repeat the page: `488 F.3d 415, 415`. Where a state has adopted a **public-domain (media-neutral) citation**, *The Indigo Book* encourages using it, with a parallel cite to the regional reporter where possible (see `references/cases.md`).

### Statutes

Pattern: `<Title> <Code> § <Section> (<Year>).`

- Federal: 42 U.S.C. § 1983 (2018). Multiple sections: 29 U.S.C. §§ 201–219 (2018). Subsections: 17 U.S.C. § 106(1) (2018).
- With the act's name: Securities Exchange Act of 1934 § 10(b), 15 U.S.C. § 78j(b) (2018).
- State (unofficial code shows the publisher): Tex. Civ. Prac. & Rem. Code Ann. § 16.003 (West 2017); Cal. Civ. Code § 1542 (West 2019).
- Federal rules (no date): Fed. R. Civ. P. 12(b)(6); Fed. R. Evid. 401.

Nothing in a statute cite is italicized. The year is the **edition of the code**, not the year of enactment. The official U.S. Code is recodified every six years (2000, 2006, 2012, 2018, …); cite the most recent edition that contains the version of the statute you mean, adding a supplement parenthetical if the provision was amended after that edition (e.g., `(2018 & Supp. II 2020)`). *The Indigo Book* includes the edition year; some attorneys and courts omit it for the current official Code, but include it when in doubt or when local rules expect it.

### Constitutions

U.S. Const. art. I, § 8, cl. 3. U.S. Const. amend. XIV, § 1. U.S. Const. pmbl. State: Tex. Const. art. I, § 9. No date for a constitution still in force; nothing italicized.

### Short forms

- *id.* — points to the immediately preceding authority. Same page: *Id.* Different page: *Id.* at 100. Capitalize only when it begins a citation sentence; the period is part of it.
- Case short form — distinctive party name + reporter + `at` + pincite: *Whitman*, 431 P.3d at 224. Choose the memorable party (not "United States," "State," "City of ___," or another common litigant).

That is enough for cases, statutes, and constitutions in most filings. For everything else, and for the rules behind the patterns above, use the reference files.

## Reference files — read the one you need

- `references/cases.md` — full case form in depth: case names (citation vs. textual sentences), reporters and which to cite, pincites and page ranges, court/jurisdiction, weight and explanatory parentheticals, prior/subsequent history, and unreported/electronic cases.
- `references/statutes-constitutions-regulations.md` — federal and state statutes, session laws, named acts, constitutions, the C.F.R. and Federal Register, agency adjudications, executive orders, legislative materials (bills, reports, hearings), procedural rules, restatements, uniform acts, and tax materials.
- `references/secondary-sources.md` — treatises and books, law review and journal articles, magazines and newspapers, encyclopedias, dictionaries, and documents filed in the same matter (record cites, briefs, motions, transcripts).
- `references/signals-and-structure.md` — citation sentences vs. clauses, the full set of signals and what each means, the order of signals, the order of authorities within a citation, string citations, and explanatory parentheticals.
- `references/short-forms-and-quotations.md` — *id.*, *supra*, *hereinafter*, case short forms with parallel cites; inline vs. block quotations (50-word rule), alterations (brackets, *[sic]*, added emphasis), omissions (ellipses), and how to collapse a pile-up of cleanup parentheticals into a single *(cleaned up)* — the convention this guide uses, consistent with *The Indigo Book*'s second edition.
- `references/abbreviations.md` — common reporters, federal and state court abbreviations and the spacing rules, case-name word abbreviations (including the few allowed in textual sentences), history/explanatory phrases, geographic terms, and months.

## Mistakes to watch for

- Using large-and-small-caps or leaving case names un-italicized (that's academic style, not brief style).
- Italicizing the comma after a case name, or italicizing parts of a statute cite.
- Adding a court abbreviation for a U.S. Supreme Court cite (the year stands alone).
- Wrong reporter series for the court (e.g., a district-court opinion cited to the Federal Reporter instead of the Federal Supplement).
- Spacing in court/reporter abbreviations: close up adjacent single capitals (S.D.N.Y.), but space a single capital from a longer abbreviation (D. Mass., S.D. Cal.).
- Dropping the pincite — a brief should point the reader to the exact page, not just the opinion's first page.
- Beginning a quotation with an ellipsis, or forgetting that a sentence-ending omission keeps the sentence's final period (four dots total).
- Forgetting to switch to a short form after the first full citation, or using *id.* when the immediately preceding citation was to a different authority.
