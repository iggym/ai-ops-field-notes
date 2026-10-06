#!/usr/bin/env python3
"""Validate metadata.json against the article files.

Catches the failure modes found in the repo audit (see tasks/tasks.md):
duplicate or mismatched article files, missing fields, leftover template
placeholders and citation tokens, and inconsistent research windows.

Usage: python3 scripts/validate.py   (exit code 1 on any error)
"""
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["id", "slug", "title", "hook", "path", "date", "status", "format",
            "tags", "reading_time_minutes", "pinned", "research_window", "source_type"]
SOURCE_TYPES = {"composite", "single-source-anonymized", "public-postmortem"}
LEFTOVERS = [r"\[citation:\d+\]", r"\{\{[A-Z_]+\}\}", r"\bTODO\b", r"\bLorem ipsum\b"]


def main():
    errors = []
    data = json.loads((ROOT / "metadata.json").read_text())
    articles = data.get("articles", [])
    seen_ids, seen_slugs, hashes = {}, {}, {}

    for a in articles:
        label = a.get("slug") or a.get("path") or a.get("title")
        missing = [k for k in REQUIRED if k not in a]
        if missing:
            errors.append(f"{label}: missing fields {missing}")

        for key, seen in (("id", seen_ids), ("slug", seen_slugs)):
            v = a.get(key)
            if v in seen:
                errors.append(f"{label}: duplicate {key} {v!r} (also {seen[v]})")
            seen[v] = label

        if not re.fullmatch(r"\d{4}", str(a.get("id", ""))):
            errors.append(f"{label}: id must be a 4-digit string")
        if a.get("path") != f"articles/{a.get('slug')}.html":
            errors.append(f"{label}: path {a.get('path')!r} does not match slug")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(a.get("date", ""))):
            errors.append(f"{label}: date must be YYYY-MM-DD")
        rw = a.get("research_window", "")
        if rw and not re.fullmatch(r"\d{4}-\d{2}-\d{2} to \d{4}-\d{2}-\d{2}", rw):
            errors.append(f"{label}: research_window must be 'YYYY-MM-DD to YYYY-MM-DD'")
        if a.get("source_type") and a["source_type"] not in SOURCE_TYPES:
            errors.append(f"{label}: unknown source_type {a['source_type']!r}")
        tags = a.get("tags", [])
        if not tags or any(not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", t) for t in tags):
            errors.append(f"{label}: tags must be non-empty lowercase-kebab")

        path = ROOT / a.get("path", "")
        if not path.is_file():
            errors.append(f"{label}: file {a.get('path')} not found")
            continue
        page = path.read_text()

        digest = hashlib.sha256(page.encode()).hexdigest()
        if digest in hashes:
            errors.append(f"{label}: file is identical to {hashes[digest]}")
        hashes[digest] = label

        m = re.search(r"<title>(.*?)</title>", page, re.S)
        page_title = html.unescape(m.group(1)).split(" — ")[0].split(" | ")[0].split(" - ")[0].strip() if m else ""
        if page_title.casefold() != a.get("title", "").casefold():
            errors.append(f"{label}: <title> is {page_title!r}, metadata says {a.get('title')!r}")

        for pat in LEFTOVERS:
            if re.search(pat, page):
                errors.append(f"{label}: leftover {pat!r} in page")

    on_disk = {f"articles/{p.name}" for p in (ROOT / "articles").glob("*.html")}
    for orphan in sorted(on_disk - {a.get("path") for a in articles}):
        errors.append(f"{orphan}: article file has no metadata entry")

    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(articles)} articles checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
