#!/usr/bin/env python3
"""Deterministic .docx -> Markdown/text extractor for DingDuff cite-check.

Word and Google Docs are the real collaboration formats; cite-check verifies
plain UTF-8 text. This converts a .docx (a zip of XML) into a stable Markdown
working file so the existing pipeline can check it unchanged. It is stdlib
only — no python-docx, no pandoc — matching verify_anchors.py's zero-dependency
ethos, so it runs in any attorney session.

What it captures, and why it matters for cite-check:

  * Body paragraphs in document order, with a light heading map
    (Word "Heading N"/"Title" styles -> N leading '#').
  * Tables (cells joined with ' | ', rows on their own lines).
  * Footnotes AND endnotes — legal citations frequently live in footnotes,
    and dropping them would silently leave those cites unchecked. Each
    reference becomes an inline marker ([^N] / [^eN]); the note bodies are
    appended under "## Footnotes" / "## Endnotes" in id order.
  * The accepted/"Accept All" view of tracked changes: inserted text
    (<w:ins>) is kept, deleted text (<w:del>/<w:delText>) is dropped. If the
    document still carries unaccepted revisions, that is reported so the
    caller can warn the attorney that "what was checked" had pending edits.

Output is deterministic (document order throughout) so the same .docx yields
byte-identical Markdown and therefore a stable SHA-256 across re-runs.

stdout carries one machine-readable JSON report; diagnostics go to stderr.

Exit codes:
    0  extracted (report.ok = true)
    2  fatal: not a .docx / unreadable zip / missing word/document.xml
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from xml.etree import ElementTree as ET

SCRIPT_VERSION = "cite-check/extract_docx.py 1.0"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DOC_PART = "word/document.xml"
FOOTNOTES_PART = "word/footnotes.xml"
ENDNOTES_PART = "word/endnotes.xml"

# Word reserves these note ids for the separator / continuation glyphs; they
# are not real notes and must never be emitted as citation-bearing text.
SEPARATOR_TYPES = {"separator", "continuationSeparator"}


class FatalError(Exception):
    pass


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _collect_runs(elem: ET.Element, out: List[str], refs: Dict[str, Set[str]],
                  stats: Dict[str, int]) -> None:
    """In-order walk of a paragraph (or note) subtree, appending visible text.

    Deleted runs (<w:del>) are skipped entirely so the result is the
    accept-all view. Footnote/endnote references become inline markers.
    """
    for child in elem:
        tag = _local(child.tag)
        if tag == "del":
            stats["del"] += 1
            continue  # tracked deletion — excluded from the accepted text
        if tag == "delText":
            continue
        if tag == "ins":
            stats["ins"] += 1
            _collect_runs(child, out, refs, stats)
            continue
        if tag == "t":
            out.append(child.text or "")
            continue
        if tag == "tab":
            out.append("\t")
            continue
        if tag in ("br", "cr"):
            out.append("\n")
            continue
        if tag == "footnoteReference":
            fid = child.get(W + "id")
            if fid is not None:
                out.append(f"[^{fid}]")
                refs["foot"].add(fid)
            continue
        if tag == "endnoteReference":
            fid = child.get(W + "id")
            if fid is not None:
                out.append(f"[^e{fid}]")
                refs["end"].add(fid)
            continue
        # Anything else (runs, hyperlinks, smartTags, …): recurse so nested
        # <w:t> is captured in order.
        _collect_runs(child, out, refs, stats)


def _para_prefix(p: ET.Element) -> str:
    """Markdown heading prefix from the paragraph's style, or '' for body."""
    ppr = p.find(W + "pPr")
    if ppr is None:
        return ""
    style = ppr.find(W + "pStyle")
    if style is None:
        return ""
    val = (style.get(W + "val") or "").strip()
    low = val.lower()
    if low in ("title",):
        return "# "
    if low.startswith("heading"):
        digits = "".join(ch for ch in val if ch.isdigit())
        level = int(digits) if digits else 1
        return "#" * min(max(level, 1), 6) + " "
    return ""


def _paragraph_text(p: ET.Element, refs: Dict[str, Set[str]],
                    stats: Dict[str, int]) -> str:
    out: List[str] = []
    _collect_runs(p, out, refs, stats)
    return _para_prefix(p) + "".join(out)


def _table_text(tbl: ET.Element, refs: Dict[str, Set[str]],
                stats: Dict[str, int]) -> str:
    rows: List[str] = []
    for tr in tbl.findall(W + "tr"):
        cells: List[str] = []
        for tc in tr.findall(W + "tc"):
            cell_paras = [_paragraph_text(p, refs, stats)
                          for p in tc.findall(W + "p")]
            cells.append(" ".join(s for s in cell_paras if s).strip())
        rows.append(" | ".join(cells))
    return "\n".join(rows)


def _body_blocks(body: ET.Element, refs: Dict[str, Set[str]],
                 stats: Dict[str, int]) -> List[str]:
    blocks: List[str] = []
    for child in body:
        tag = _local(child.tag)
        if tag == "p":
            blocks.append(_paragraph_text(child, refs, stats))
        elif tag == "tbl":
            blocks.append(_table_text(child, refs, stats))
        # sectPr and others carry no body text.
    return blocks


def _notes(zf: zipfile.ZipFile, part: str, item_tag: str,
           referenced_ids: Set[str], refs: Dict[str, Set[str]],
           stats: Dict[str, int]) -> List[Tuple[int, str, str]]:
    """Return [(sort_key, id, text)] for real notes actually referenced in the
    body. Orphan definitions — including a note whose only reference sat in
    deleted (tracked-change) text — are skipped so they can't inject stray
    text or citations into the extracted memo."""
    if part not in zf.namelist():
        return []
    root = ET.fromstring(zf.read(part))
    notes: List[Tuple[int, str, str]] = []
    for note in root.findall(W + item_tag):
        nid = note.get(W + "id")
        if nid is None or note.get(W + "type") in SEPARATOR_TYPES:
            continue
        if nid not in referenced_ids:
            continue
        paras = [_paragraph_text(p, refs, stats) for p in note.findall(W + "p")]
        text = " ".join(s.strip() for s in paras if s.strip()).strip()
        if not text:
            continue
        try:
            key = int(nid)
        except ValueError:
            key = 1 << 30
        notes.append((key, nid, text))
    notes.sort(key=lambda n: (n[0], n[1]))
    return notes


def extract_docx(path: Path) -> Tuple[str, Dict[str, Any]]:
    """Extract a .docx into Markdown text; returns (markdown, report_fields)."""
    if not zipfile.is_zipfile(path):
        raise FatalError(f"{path} is not a .docx (not a zip archive)")
    try:
        with zipfile.ZipFile(path) as zf:
            if DOC_PART not in zf.namelist():
                raise FatalError(f"{path} is missing {DOC_PART}; not a Word document")
            doc_root = ET.fromstring(zf.read(DOC_PART))
            refs: Dict[str, Set[str]] = {"foot": set(), "end": set()}
            stats: Dict[str, int] = {"ins": 0, "del": 0}

            body = doc_root.find(W + "body")
            blocks = _body_blocks(body, refs, stats) if body is not None else []

            # Snapshot the ids the body actually references BEFORE reading the
            # note parts, so only referenced notes are emitted (see _notes).
            ref_foot, ref_end = set(refs["foot"]), set(refs["end"])
            footnotes = _notes(zf, FOOTNOTES_PART, "footnote", ref_foot, refs, stats)
            endnotes = _notes(zf, ENDNOTES_PART, "endnote", ref_end, refs, stats)
    except zipfile.BadZipFile as exc:
        raise FatalError(f"cannot read {path}: {exc}") from exc
    except ET.ParseError as exc:
        raise FatalError(f"malformed XML in {path}: {exc}") from exc

    sections: List[str] = ["\n\n".join(b for b in blocks if b.strip())]
    if footnotes:
        lines = ["## Footnotes", ""] + [f"[^{nid}]: {text}" for _, nid, text in footnotes]
        sections.append("\n".join(lines))
    if endnotes:
        lines = ["## Endnotes", ""] + [f"[^e{nid}]: {text}" for _, nid, text in endnotes]
        sections.append("\n".join(lines))

    markdown = "\n\n".join(s for s in sections if s.strip())
    if markdown:
        markdown += "\n"

    report = {
        "ok": True,
        "paragraphs": sum(1 for b in blocks if b.strip()),
        "footnotes": len(footnotes),
        "endnotes": len(endnotes),
        "has_tracked_changes": bool(stats["ins"] or stats["del"]),
        "tracked_insertions": stats["ins"],
        "tracked_deletions": stats["del"],
        "char_count": len(markdown),
    }
    return markdown, report


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--in", dest="inp", required=True, help="path to the .docx")
    parser.add_argument("--out", required=True, help="path to write extracted Markdown")
    args = parser.parse_args(argv)

    in_path = Path(args.inp)
    try:
        if not in_path.is_file():
            raise FatalError(f"input not found: {args.inp}")
        markdown, report = extract_docx(in_path)
    except FatalError as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2

    out_path = Path(args.out)
    out_path.write_text(markdown, encoding="utf-8")
    report["out"] = args.out
    report["generated_by"] = SCRIPT_VERSION
    if report["has_tracked_changes"]:
        print(
            f"warning: {args.inp} has unaccepted tracked changes "
            f"({report['tracked_insertions']} insertions, "
            f"{report['tracked_deletions']} deletions); extracted the "
            "accept-all view. Confirm this is the text you mean to cite-check.",
            file=sys.stderr,
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
