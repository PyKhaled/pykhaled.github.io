#!/usr/bin/env python3
"""Validate Hugo Markdown content before publishing."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ("title", "date", "description")
FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
LOCAL_URL_RE = re.compile(r"https?://(?:localhost|127\.0\.0\.1)(?::\d+)?", re.I)
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b", re.I)


def parse_front_matter(text: str) -> dict[str, str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"\'')
    return data


def body_without_front_matter(text: str) -> str:
    match = FRONT_MATTER_RE.match(text)
    return text[match.end():] if match else text


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    fm = parse_front_matter(text)

    if not fm:
        errors.append("missing YAML front matter (--- ... ---)")
        return errors

    for field in REQUIRED_FIELDS:
        if not fm.get(field):
            errors.append(f"missing required front matter field: {field}")

    description = fm.get("description", "")
    if len(description) > 160:
        errors.append(f"description is {len(description)} characters; keep it <= 160")

    if fm.get("draft", "").lower() == "true":
        errors.append("draft is true")

    tags = fm.get("tags", "")
    if "posts" in path.parts and not tags:
        errors.append("published post has no tags")

    body = body_without_front_matter(text)

    headings = [(len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(body)]
    h1_count = sum(1 for level, _ in headings if level == 1)
    if h1_count > 1:
        errors.append(f"contains {h1_count} H1 headings; use at most one H1")

    previous_level = None
    for level, title in headings:
        if previous_level is not None and level > previous_level + 1:
            errors.append(f"heading level jumps from H{previous_level} to H{level}: {title}")
        previous_level = level

    for match in IMAGE_RE.finditer(body):
        if not match.group(1).strip():
            errors.append("image has empty alt text")

    if LOCAL_URL_RE.search(body):
        errors.append("contains localhost/127.0.0.1 URL")

    if PLACEHOLDER_RE.search(body):
        errors.append("contains TODO/FIXME/TBD placeholder")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "content")
    if not root.exists():
        print(f"Content directory '{root}' does not exist; nothing to validate.")
        return 0

    failures = 0
    for path in sorted(root.rglob("*.md")):
        file_errors = validate_file(path)
        if file_errors:
            failures += 1
            print(f"\n{path}:")
            for error in file_errors:
                print(f"  - {error}")

    if failures:
        print(f"\nValidation failed for {failures} file(s).")
        return 1

    print("Content validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
