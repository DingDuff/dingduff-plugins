#!/usr/bin/env python3
"""Standalone review-bundle generator for DingDuff cite-check.

Reads cites.json (schema v1) plus the memo and source files it references,
verifies every file's checksum, pre-segments all documents (so the viewer's
JavaScript never performs offset arithmetic), and injects the payload into
the shared viewer template to produce a single self-contained review.html.

Checksum policy: any mismatch between cites.json and the bytes on disk is
fatal (exit 2) — wrong highlights are worse than no highlights. --force
proceeds, but suppresses highlights for mismatched documents and renders a
prominent warning banner.

Exit codes: 0 success; 2 fatal (missing/mismatched/unreadable files,
malformed cites.json, missing template placeholder).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCRIPT_VERSION = "cite-check/build_review.py 1.0"
PAYLOAD_PLACEHOLDER = "/*__CITECHECK_PAYLOAD__*/"
SIZE_WARNING_CHARS = 15_000_000

DEFAULT_TEMPLATE = Path(__file__).resolve().parent.parent / "viewer" / "review_viewer.html"


class FatalError(Exception):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_document(path: Path) -> str:
    # Decode failures become FatalError so the CLI honors its exit-2 contract
    # (a file can turn non-UTF-8 between verification and bundle time).
    try:
        return path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as exc:
        raise FatalError(f"{path} is not valid UTF-8: {exc}") from exc


def binds_hash(cite_text: str, proposition: str) -> str:
    return hashlib.sha256(
        (cite_text + "\x00" + proposition).encode("utf-8")).hexdigest()


def segment_document(raw: str, spans: List[Tuple[int, int, str]]) -> List[Dict[str, Any]]:
    """Flatten (start, end, mark_id) spans into ordered segments whose text
    concatenation equals raw exactly. Overlapping spans compose: a segment
    carries every mark covering it."""
    clipped = [(max(0, s), min(len(raw), e), m) for s, e, m in spans if s < e]
    bounds = {0, len(raw)}
    for s, e, _ in clipped:
        bounds.add(s)
        bounds.add(e)
    ordered = sorted(bounds)
    segments: List[Dict[str, Any]] = []
    for a, b in zip(ordered, ordered[1:]):
        marks = [m for s, e, m in clipped if s <= a and b <= e]
        segments.append({"text": raw[a:b], "marks": marks})
    return segments


def escape_payload(payload: Dict[str, Any]) -> str:
    """JSON-encode the payload so it can never break out of its script tag:
    '<' becomes \\u003c (a legal JSON escape), so '</script>' and '<!--'
    cannot appear in the emitted HTML even if a source document contains
    them. U+2028/9 are escaped for safety in any inline-JS reuse."""
    text = json.dumps(payload, ensure_ascii=False)
    return (text.replace("<", "\\u003c")
                .replace("\u2028", "\\u2028")
                .replace("\u2029", "\\u2029"))


def load_cites(path: Path) -> Dict[str, Any]:
    try:
        cites = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FatalError(f"cannot read cites.json: {exc}") from exc
    if not isinstance(cites, dict) or cites.get("schema_version") != 1:
        raise FatalError("cites.json schema_version must be 1")
    for key in ("memo", "sources", "citations"):
        if key not in cites:
            raise FatalError(f"cites.json is missing '{key}'")
    return cites


def load_review(path: Path) -> Optional[Dict[str, Any]]:
    try:
        review = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FatalError(f"cannot read review file: {exc}") from exc
    if not isinstance(review, dict) or review.get("schema_version") != 1:
        raise FatalError("review.json schema_version must be 1")
    return review


def build_payload(cites: Dict[str, Any], workdir: Path, force: bool,
                  prior_review: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[str]]:
    mismatches: List[str] = []
    total_chars = 0

    # --- memo ---
    memo_rel = cites["memo"]["path"]
    memo_path = workdir / memo_rel
    if not memo_path.is_file():
        raise FatalError(f"memo file not found: {memo_rel}")
    memo_ok = sha256_file(memo_path) == cites["memo"]["sha256"]
    if not memo_ok:
        mismatches.append(memo_rel)
    memo_raw = read_document(memo_path)
    total_chars += len(memo_raw)
    if memo_ok:
        memo_spans = [
            (c["memo_anchor"]["start"], c["memo_anchor"]["end"], c["id"])
            for c in cites["citations"] if c.get("memo_anchor")
        ]
        memo_doc = {"segments": segment_document(memo_raw, memo_spans),
                    "checksum_ok": True}
    else:
        memo_doc = {"segments": [{"text": memo_raw, "marks": []}],
                    "checksum_ok": False}

    # --- sources ---
    anchors_by_source: Dict[str, List[Tuple[int, int, str]]] = {}
    for c in cites["citations"]:
        for i, a in enumerate(c.get("anchors", [])):
            anchors_by_source.setdefault(c["source"], []).append(
                (a["start"], a["end"], f"{c['id']}:{i}"))

    source_docs: Dict[str, Any] = {}
    for key, src in cites["sources"].items():
        if src.get("missing") or not src.get("path"):
            source_docs[key] = {"segments": None, "checksum_ok": None, "missing": True}
            continue
        src_path = workdir / src["path"]
        if not src_path.is_file():
            raise FatalError(f"source file not found: {src['path']}")
        ok = sha256_file(src_path) == src["sha256"]
        if not ok:
            mismatches.append(src["path"])
        raw = read_document(src_path)
        total_chars += len(raw)
        if ok:
            source_docs[key] = {
                "segments": segment_document(raw, anchors_by_source.get(key, [])),
                "checksum_ok": True,
            }
        else:
            source_docs[key] = {"segments": [{"text": raw, "marks": []}],
                                "checksum_ok": False}

    if mismatches and not force:
        listing = "\n  ".join(mismatches)
        raise FatalError(
            "checksum mismatch — these files changed since cites.json was "
            f"generated:\n  {listing}\nRe-run /cite-check (or pass --force to "
            "render without highlights for the changed files).")

    if total_chars > SIZE_WARNING_CHARS:
        print(f"warning: embedded documents total {total_chars:,} chars; "
              "review.html will be large", file=sys.stderr)

    binds = {c["id"]: c.get("binds_to") or binds_hash(c["cite_text"], c["proposition"])
             for c in cites["citations"]}

    payload = {
        "mode": "standalone",
        "generator": SCRIPT_VERSION,
        "cites": cites,
        "memo_doc": memo_doc,
        "source_docs": source_docs,
        "binds": binds,
        "prior_review": prior_review,
        "build": {"forced": bool(mismatches), "mismatches": mismatches},
    }
    return payload, mismatches


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cites", required=True, help="path to cites.json")
    parser.add_argument("--out", required=True, help="path to write review.html")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE),
                        help="viewer template (defaults to the skill's shared viewer)")
    parser.add_argument("--review", default=None,
                        help="existing review.json to embed as prior verdicts")
    parser.add_argument("--workdir", default=".",
                        help="directory against which relative paths resolve")
    parser.add_argument("--force", action="store_true",
                        help="render despite checksum mismatches (highlights "
                             "suppressed for changed files; warning banner shown)")
    args = parser.parse_args(argv)

    workdir = Path(args.workdir)
    try:
        template_path = Path(args.template)
        if not template_path.is_file():
            raise FatalError(f"viewer template not found: {args.template}")
        template = template_path.read_text(encoding="utf-8")
        if PAYLOAD_PLACEHOLDER not in template:
            raise FatalError("viewer template is missing the payload placeholder")

        cites = load_cites(workdir / args.cites)
        prior_review = load_review(workdir / args.review) if args.review else None
        payload, mismatches = build_payload(cites, workdir, args.force, prior_review)
    except FatalError as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 2

    html = template.replace(PAYLOAD_PLACEHOLDER, escape_payload(payload), 1)
    out_path = workdir / args.out
    out_path.write_text(html, encoding="utf-8")
    if mismatches:
        print(f"wrote {args.out} WITH CHECKSUM WARNINGS: {', '.join(mismatches)}",
              file=sys.stderr)
    print(json.dumps({"ok": True, "out": args.out,
                      "citations": len(cites["citations"]),
                      "forced": bool(mismatches)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
