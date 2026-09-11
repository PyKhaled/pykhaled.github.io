from pathlib import Path
import re
import sys

CONTENT = Path("content")
required = ["title", "description"]
errors = []

for path in CONTENT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        errors.append(f"{path}: missing YAML front matter")
        continue

    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{path}: malformed front matter")
        continue

    front = parts[1]
    body = parts[2]

    for key in required:
        if not re.search(rf"(?m)^{re.escape(key)}\s*:\s*.+$", front):
            errors.append(f"{path}: missing or empty '{key}'")

    desc = re.search(r'(?m)^description\s*:\s*["\']?(.*?)["\']?\s*$', front)
    if desc and len(desc.group(1).strip()) > 160:
        errors.append(f"{path}: description exceeds 160 characters")

    if re.search(r"(?i)\b(TODO|FIXME)\b", body):
        errors.append(f"{path}: contains TODO/FIXME")

    if re.search(r"https?://(localhost|127\.0\.0\.1)", body):
        errors.append(f"{path}: contains localhost URL")

    if re.search(r"!\[[ \t]*\]\(", body):
        errors.append(f"{path}: image with empty alt text")

    if "/blog/" in str(path) and re.search(r"(?m)^draft\s*:\s*false\s*$", front):
        if not re.search(r"(?m)^tags\s*:", front):
            errors.append(f"{path}: published blog post should include tags")

if errors:
    print("Content validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Content validation passed.")
