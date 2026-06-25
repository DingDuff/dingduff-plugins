#!/usr/bin/env python3
"""Audit-log generator for DingDuff cite-check.

Produces a single self-contained, PRINTABLE HTML audit log (letter landscape)
from cites.json (schema v1) and, when present, review.json — the firm-internal
and court-facing record that a human attorney checked the work product.

Columns: citation # · source cited · proposition · successfully anchored? ·
attorney review status (✅ ⚠️ ‼️ ❓) · review note · reviewed by.

Running without --review is valid (all rows ❓ — a "verified but not yet
attorney-reviewed" audit). Every cell is HTML-escaped: notes are free-form
attorney input. An integrity footer records the memo hash, verifier
provenance, and reviewer list for evidentiary value.

Exit codes: 0 success; 2 fatal (missing/malformed inputs).
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

SCRIPT_VERSION = "cite-check/build_audit.py 1.0"

# DingDuff brand mark (George) as inline SVG (NOT a data: <img> — CSP in MCP
# App iframes / print contexts blocks data: images). Lockstep with the viewer.
DOG_SVG = '<svg viewBox="0 0 32 32" shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg"><rect x="3" y="11" width="1" height="1" fill="#9b8a7c"/><rect x="3" y="13" width="1" height="1" fill="#9b8a7c"/><rect x="4" y="12" width="1" height="1" fill="#513219"/><rect x="4" y="14" width="1" height="1" fill="#7a5534"/><rect x="4" y="13" width="1" height="1" fill="#7c4e24"/><rect x="4" y="10" width="1" height="1" fill="#9b8a7c"/><rect x="4" y="11" width="2" height="1" fill="#513219"/><rect x="5" y="10" width="1" height="1" fill="#7a5534"/><rect x="5" y="15" width="1" height="1" fill="#7a5534"/><rect x="5" y="12" width="1" height="1" fill="#7c4e24"/><rect x="5" y="14" width="1" height="1" fill="#7c4e24"/><rect x="5" y="13" width="1" height="1" fill="#895729"/><rect x="6" y="10" width="1" height="1" fill="#513219"/><rect x="6" y="9" width="1" height="1" fill="#7a5534"/><rect x="6" y="11" width="1" height="1" fill="#7c4e24"/><rect x="6" y="13" width="1" height="1" fill="#7c4e24"/><rect x="6" y="15" width="1" height="1" fill="#7c4e24"/><rect x="6" y="12" width="1" height="1" fill="#895729"/><rect x="6" y="14" width="6" height="1" fill="#895729"/><rect x="7" y="9" width="1" height="1" fill="#513219"/><rect x="7" y="8" width="1" height="1" fill="#7a5534"/><rect x="7" y="10" width="1" height="1" fill="#7c4e24"/><rect x="7" y="12" width="1" height="1" fill="#7c4e24"/><rect x="7" y="15" width="2" height="1" fill="#513219"/><rect x="7" y="11" width="2" height="1" fill="#895729"/><rect x="7" y="13" width="6" height="1" fill="#895729"/><rect x="8" y="7" width="1" height="1" fill="#513219"/><rect x="8" y="20" width="1" height="3" fill="#513219"/><rect x="8" y="24" width="1" height="1" fill="#513219"/><rect x="8" y="6" width="1" height="1" fill="#7a5534"/><rect x="8" y="16" width="1" height="1" fill="#7a5534"/><rect x="8" y="8" width="1" height="1" fill="#7c4e24"/><rect x="8" y="9" width="1" height="2" fill="#895729"/><rect x="8" y="19" width="1" height="1" fill="#9b8a7c"/><rect x="8" y="23" width="2" height="1" fill="#513219"/><rect x="8" y="25" width="4" height="2" fill="#513219"/><rect x="8" y="12" width="4" height="1" fill="#895729"/><rect x="8" y="27" width="16" height="1" fill="#7a5534"/><rect x="9" y="16" width="1" height="1" fill="#513219"/><rect x="9" y="18" width="1" height="1" fill="#513219"/><rect x="9" y="6" width="1" height="1" fill="#7c4e24"/><rect x="9" y="15" width="1" height="1" fill="#7c4e24"/><rect x="9" y="19" width="1" height="1" fill="#7c4e24"/><rect x="9" y="24" width="1" height="1" fill="#7c4e24"/><rect x="9" y="21" width="1" height="1" fill="#895729"/><rect x="9" y="5" width="1" height="1" fill="#9b8a7c"/><rect x="9" y="10" width="2" height="1" fill="#513219"/><rect x="9" y="17" width="2" height="1" fill="#513219"/><rect x="9" y="9" width="2" height="1" fill="#7c4e24"/><rect x="9" y="11" width="2" height="1" fill="#7c4e24"/><rect x="9" y="22" width="2" height="1" fill="#7c4e24"/><rect x="9" y="7" width="3" height="1" fill="#895729"/><rect x="9" y="8" width="5" height="1" fill="#895729"/><rect x="9" y="20" width="12" height="1" fill="#895729"/><rect x="10" y="6" width="1" height="1" fill="#513219"/><rect x="10" y="5" width="1" height="1" fill="#7a5534"/><rect x="10" y="16" width="1" height="1" fill="#7c4e24"/><rect x="10" y="23" width="1" height="1" fill="#7c4e24"/><rect x="10" y="24" width="2" height="1" fill="#513219"/><rect x="10" y="21" width="2" height="1" fill="#7c4e24"/><rect x="10" y="15" width="2" height="1" fill="#895729"/><rect x="10" y="18" width="9" height="1" fill="#895729"/><rect x="10" y="19" width="10" height="1" fill="#895729"/><rect x="11" y="5" width="1" height="1" fill="#513219"/><rect x="11" y="22" width="1" height="2" fill="#513219"/><rect x="11" y="6" width="1" height="1" fill="#7c4e24"/><rect x="11" y="9" width="1" height="3" fill="#895729"/><rect x="11" y="17" width="2" height="1" fill="#895729"/><rect x="11" y="16" width="4" height="1" fill="#895729"/><rect x="12" y="5" width="1" height="1" fill="#7c4e24"/><rect x="12" y="7" width="1" height="1" fill="#7c4e24"/><rect x="12" y="10" width="1" height="3" fill="#7c4e24"/><rect x="12" y="14" width="1" height="2" fill="#7c4e24"/><rect x="12" y="9" width="2" height="1" fill="#7c4e24"/><rect x="12" y="6" width="2" height="1" fill="#895729"/><rect x="12" y="22" width="2" height="4" fill="#895729"/><rect x="12" y="26" width="3" height="1" fill="#7c4e24"/><rect x="12" y="21" width="10" height="1" fill="#895729"/><rect x="13" y="10" width="1" height="1" fill="#513219"/><rect x="13" y="13" width="1" height="1" fill="#7c4e24"/><rect x="13" y="17" width="1" height="1" fill="#7c4e24"/><rect x="13" y="5" width="2" height="1" fill="#513219"/><rect x="13" y="11" width="2" height="2" fill="#513219"/><rect x="13" y="14" width="3" height="1" fill="#513219"/><rect x="13" y="7" width="3" height="1" fill="#895729"/><rect x="13" y="15" width="6" height="1" fill="#513219"/><rect x="14" y="13" width="1" height="1" fill="#513219"/><rect x="14" y="8" width="1" height="1" fill="#7c4e24"/><rect x="14" y="23" width="1" height="3" fill="#7c4e24"/><rect x="14" y="6" width="3" height="1" fill="#513219"/><rect x="14" y="22" width="3" height="1" fill="#7c4e24"/><rect x="14" y="9" width="4" height="2" fill="#895729"/><rect x="14" y="17" width="4" height="1" fill="#895729"/><rect x="15" y="23" width="1" height="2" fill="#513219"/><rect x="15" y="5" width="1" height="1" fill="#9b8a7c"/><rect x="15" y="25" width="2" height="2" fill="#513219"/><rect x="15" y="8" width="2" height="1" fill="#895729"/><rect x="15" y="12" width="3" height="1" fill="#895729"/><rect x="15" y="16" width="4" height="1" fill="#513219"/><rect x="15" y="11" width="4" height="1" fill="#895729"/><rect x="15" y="13" width="4" height="1" fill="#895729"/><rect x="16" y="24" width="1" height="1" fill="#7c4e24"/><rect x="16" y="7" width="2" height="1" fill="#513219"/><rect x="16" y="14" width="2" height="1" fill="#895729"/><rect x="16" y="23" width="7" height="1" fill="#895729"/><rect x="17" y="6" width="1" height="1" fill="#9b8a7c"/><rect x="17" y="8" width="2" height="1" fill="#513219"/><rect x="17" y="26" width="6" height="1" fill="#7c4e24"/><rect x="17" y="24" width="6" height="2" fill="#895729"/><rect x="17" y="22" width="7" height="1" fill="#895729"/><rect x="18" y="9" width="1" height="1" fill="#513219"/><rect x="18" y="14" width="1" height="1" fill="#513219"/><rect x="18" y="12" width="1" height="1" fill="#7c4e24"/><rect x="18" y="7" width="1" height="1" fill="#9b8a7c"/><rect x="18" y="10" width="2" height="1" fill="#513219"/><rect x="18" y="17" width="2" height="1" fill="#513219"/><rect x="19" y="11" width="1" height="3" fill="#513219"/><rect x="19" y="16" width="1" height="1" fill="#9b8a7c"/><rect x="19" y="18" width="2" height="1" fill="#513219"/><rect x="20" y="19" width="2" height="1" fill="#513219"/><rect x="21" y="15" width="1" height="1" fill="#513219"/><rect x="21" y="13" width="1" height="1" fill="#9b8a7c"/><rect x="21" y="14" width="2" height="1" fill="#513219"/><rect x="21" y="20" width="3" height="1" fill="#513219"/><rect x="22" y="21" width="1" height="1" fill="#513219"/><rect x="22" y="15" width="1" height="1" fill="#895729"/><rect x="22" y="13" width="2" height="1" fill="#513219"/><rect x="22" y="17" width="2" height="1" fill="#9b8a7c"/><rect x="22" y="16" width="3" height="1" fill="#513219"/><rect x="23" y="24" width="1" height="3" fill="#513219"/><rect x="23" y="15" width="1" height="1" fill="#7c4e24"/><rect x="23" y="21" width="1" height="1" fill="#7c4e24"/><rect x="23" y="23" width="1" height="1" fill="#7c4e24"/><rect x="23" y="19" width="2" height="1" fill="#513219"/><rect x="23" y="14" width="2" height="1" fill="#895729"/><rect x="23" y="12" width="3" height="1" fill="#9b8a7c"/><rect x="24" y="15" width="1" height="1" fill="#513219"/><rect x="24" y="17" width="1" height="2" fill="#513219"/><rect x="24" y="23" width="1" height="1" fill="#7a5534"/><rect x="24" y="13" width="1" height="1" fill="#7c4e24"/><rect x="24" y="20" width="1" height="1" fill="#7c4e24"/><rect x="24" y="22" width="1" height="1" fill="#7c4e24"/><rect x="24" y="21" width="1" height="1" fill="#895729"/><rect x="25" y="13" width="1" height="1" fill="#513219"/><rect x="25" y="22" width="1" height="1" fill="#7a5534"/><rect x="25" y="14" width="1" height="1" fill="#7c4e24"/><rect x="25" y="16" width="1" height="3" fill="#7c4e24"/><rect x="25" y="21" width="1" height="1" fill="#7c4e24"/><rect x="25" y="20" width="1" height="1" fill="#895729"/><rect x="25" y="15" width="2" height="1" fill="#7c4e24"/><rect x="25" y="19" width="2" height="1" fill="#7c4e24"/><rect x="26" y="14" width="1" height="1" fill="#513219"/><rect x="26" y="20" width="1" height="1" fill="#513219"/><rect x="26" y="13" width="1" height="1" fill="#7a5534"/><rect x="26" y="21" width="1" height="1" fill="#7a5534"/><rect x="26" y="16" width="1" height="3" fill="#895729"/><rect x="27" y="15" width="1" height="4" fill="#513219"/><rect x="27" y="14" width="1" height="1" fill="#7a5534"/><rect x="27" y="19" width="1" height="1" fill="#7a5534"/></svg>'

# Keep in lockstep with the viewer's verdict model (review_viewer.html) and
# review.schema.json. Legacy values come from pre-round-2 review.json files.
VERDICT_EMOJI = {
    "verified": "✅",
    "needs_attention": "⚠️",
    "rejected": "‼️",
}
LEGACY_VERDICTS = {"misquoted": "rejected", "wrong_pin": "needs_attention"}
UNREVIEWED = "❓"


class FatalError(Exception):
    pass


def _load_json(path: Path, what: str) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FatalError(f"cannot read {what}: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise FatalError(f"{what} schema_version must be 1")
    return data


def source_label(src: Dict[str, Any]) -> str:
    """Human label for a source row: case name + reporter cite for opinions,
    official citation (or code § section) for statutes, title (kind) for
    attorney-supplied documents. Kept in lockstep with the viewer's sourceLabel."""
    if src.get("type") == "opinion":
        name = src.get("case_name") or f"cluster {src.get('cluster_id', '?')}"
        cite = src.get("citation")
        return f"{name}, {cite}" if cite else name
    if src.get("type") == "document":
        label = src.get("title") or "supplied document"
        return f"{label} ({src['kind']})" if src.get("kind") else label
    cite = src.get("citation")
    if cite:
        return cite
    code, section = src.get("code"), src.get("section")
    if code and section:
        return f"{code} § {section}"
    return src.get("statute_id") or "unknown statute"


def anchored_label(citation: Dict[str, Any]) -> str:
    status = citation.get("status")
    if status == "anchored":
        # Both are verified word-for-word quotes; "formatting differs" flags
        # only cosmetic differences (punctuation/spacing/line breaks/quote
        # marks). Keep these strings in lockstep with the viewer's anchoredLabel.
        matches = {a.get("match") for a in citation.get("anchors", [])}
        return "✓ Verbatim" if matches == {"exact"} else "✓ Verbatim (formatting differs)"
    if status == "no_quote_claimed":
        return "— no quote claimed"
    reason = citation.get("failure_reason") or "failed"
    if reason == "source_missing":
        return "— source missing"
    return f"✗ {reason.replace('_', ' ')}"


def review_for(citation: Dict[str, Any],
               reviews: Dict[str, Any]) -> Dict[str, str]:
    """Resolve the attorney-review cell set {emoji, note, reviewer} for one
    citation, applying legacy-verdict mapping and binds_to staleness."""
    entry = reviews.get(citation["id"])
    if not isinstance(entry, dict):
        return {"emoji": UNREVIEWED, "note": "", "reviewer": ""}

    verdict = entry.get("verdict", "")
    note = entry.get("note") or ""
    if verdict in LEGACY_VERDICTS:
        note = (note + " " if note else "") + f"[recorded as {verdict}]"
        verdict = LEGACY_VERDICTS[verdict]

    binds = citation.get("binds_to")
    if binds and entry.get("binds_to") and entry["binds_to"] != binds:
        # Stale review: the cite or its proposition changed since the verdict.
        # An audit log must not present it as a live verdict.
        return {
            "emoji": UNREVIEWED,
            "note": "[a prior review of an earlier version of this citation "
                    "was not applied]",
            "reviewer": "",
        }

    emoji = VERDICT_EMOJI.get(verdict)
    if emoji is None:
        return {"emoji": UNREVIEWED, "note": note, "reviewer": ""}
    return {"emoji": emoji, "note": note,
            "reviewer": entry.get("reviewer") or ""}


_PAGE_CSS = """
  @page { size: letter landscape; margin: 0.5in; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
         font-size: 9.5pt; color: #1a1a1a; background: #fff; margin: 0;
         padding: 12px; }
  @media print { body { padding: 0; } }
  h1 { font-size: 13pt; margin: 0 0 2pt; }
  h1 .ddog { display: inline-block; width: 22px; height: 22px; vertical-align: -4px; margin-right: 7px; }
  h1 .ddog svg { width: 100%; height: 100%; display: block; }
  .meta { color: #555; font-size: 8.5pt; margin-bottom: 8pt; }
  table { width: 100%; border-collapse: collapse; table-layout: fixed; }
  thead { display: table-header-group; }
  th { background: #f0efec; text-align: left; font-size: 8.5pt;
       text-transform: uppercase; letter-spacing: 0.04em; }
  th, td { border: 0.5pt solid #999; padding: 3pt 5pt; vertical-align: top;
           overflow-wrap: break-word; }
  tr { page-break-inside: avoid; }
  td.status { text-align: center; font-size: 12pt; }
  td.anchored { font-size: 8.5pt; }
  .col-id { width: 4%; } .col-src { width: 17%; } .col-prop { width: 28%; }
  .col-anch { width: 10%; } .col-status { width: 6%; } .col-note { width: 25%; }
  .col-by { width: 10%; }
  .integrity { margin-top: 10pt; font-size: 7.5pt; color: #555;
               border-top: 0.5pt solid #999; padding-top: 4pt; }
  .integrity code { font-family: ui-monospace, Menlo, monospace; }
  .legend { font-size: 8pt; color: #555; margin: 4pt 0 8pt; }
"""


def build_audit_html(cites: Dict[str, Any], review: Optional[Dict[str, Any]],
                     title: str) -> str:
    e = html.escape
    reviews = (review or {}).get("reviews", {})
    rows: List[str] = []
    counts = {"✅": 0, "⚠️": 0, "‼️": 0, UNREVIEWED: 0}
    reviewers: List[str] = []

    for c in cites["citations"]:
        src = cites["sources"].get(c["source"], {})
        r = review_for(c, reviews)
        counts[r["emoji"]] += 1
        if r["reviewer"] and r["reviewer"] not in reviewers:
            reviewers.append(r["reviewer"])
        rows.append(
            "<tr>"
            f"<td>{e(c['id'])}</td>"
            f"<td>{e(source_label(src))}</td>"
            f"<td>{e(c.get('proposition', ''))}</td>"
            f"<td class=\"anchored\">{e(anchored_label(c))}</td>"
            f"<td class=\"status\">{e(r['emoji'])}</td>"
            f"<td>{e(r['note'])}</td>"
            f"<td>{e(r['reviewer'])}</td>"
            "</tr>"
        )

    memo = cites["memo"]
    built_at = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    total = len(cites["citations"])
    reviewed = total - counts[UNREVIEWED]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{e(title)}</title>
<style>{_PAGE_CSS}</style>
</head>
<body>
<h1><span class="ddog">{DOG_SVG}</span>{e(title)}</h1>
<div class="meta">Memo: <strong>{e(memo['path'])}</strong> ·
  {reviewed}/{total} citations attorney-reviewed ·
  ✅ {counts['✅']} · ⚠️ {counts['⚠️']} · ‼️ {counts['‼️']} · ❓ {counts[UNREVIEWED]}</div>
<div class="legend">✅ verified · ⚠️ needs attention · ‼️ rejected · ❓ not reviewed.
  "Anchored" = the quoted passage was mechanically located, verbatim, in the
  stored source file by the cite-check verifier.</div>
<table>
<thead><tr>
  <th class="col-id">#</th>
  <th class="col-src">Source cited</th>
  <th class="col-prop">Proposition cited for</th>
  <th class="col-anch">Anchored?</th>
  <th class="col-status">Review</th>
  <th class="col-note">Review note</th>
  <th class="col-by">Reviewed by</th>
</tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
<div class="integrity">
  Integrity record — memo SHA-256: <code>{e(memo['sha256'])}</code> ·
  verification run: {e(memo.get('generated_at', '?'))} by {e(memo.get('generated_by', '?'))} ·
  reviewers: {e(', '.join(reviewers) or '(none)')} ·
  audit generated: {built_at} by {e(SCRIPT_VERSION)}.
  Verdicts bind to each citation's text+proposition hash; a changed citation
  invalidates its prior verdict (shown as ❓).
</div>
</body>
</html>
"""


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cites", required=True, help="path to cites.json")
    parser.add_argument("--review", default=None,
                        help="path to review.json (omit for an unreviewed audit)")
    parser.add_argument("--out", required=True,
                        help="path to write the audit HTML")
    parser.add_argument("--workdir", default=".",
                        help="directory against which relative paths resolve")
    parser.add_argument("--title", default="DingDuff Citation Verification Audit Log")
    args = parser.parse_args(argv)

    workdir = Path(args.workdir)
    try:
        cites = _load_json(workdir / args.cites, "cites.json")
        for key in ("memo", "sources", "citations"):
            if key not in cites:
                raise FatalError(f"cites.json is missing '{key}'")
        review = _load_json(workdir / args.review, "review.json") if args.review else None
    except FatalError as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2

    out_path = workdir / args.out
    out_path.write_text(build_audit_html(cites, review, args.title),
                        encoding="utf-8")
    # Same semantics as the table: stale (binds_to mismatch) and
    # invalid-verdict entries do NOT count as attorney-reviewed.
    reviews = (review or {}).get("reviews", {})
    reviewed = sum(1 for c in cites["citations"]
                   if review_for(c, reviews)["emoji"] != UNREVIEWED)
    print(json.dumps({"ok": True, "out": args.out,
                      "citations": len(cites["citations"]),
                      "reviewed": reviewed}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
