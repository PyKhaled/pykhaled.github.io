# Contributing

This repository is the source of truth for Ahmed Khaled's personal website.

The contribution flow is intentionally lightweight but disciplined: every content or site change should be made on a branch, validated locally, reviewed through a pull request, and merged into `main`.

## Branching model

Always branch from the latest `main`.

Use one branch per change.

Recommended branch prefixes:

```text
content/    New or updated articles, notes, and project pages
feature/    New site features
fix/        Bug fixes
chore/      Maintenance, dependency, CI, or configuration work
docs/       Documentation-only changes
```

Examples:

```text
content/django-rest-framework-files
content/django-saas-extensions
feature/project-related-content
fix/hugo-asset-pipeline
chore/update-cspell-dictionary
docs/contribution-workflow
```

Avoid working directly on `main`.

---

## Standard contribution flow

### 1. Switch to `main`

```bash
git switch main
```

If you use an older Git version:

```bash
git checkout main
```

### 2. Pull the latest changes

```bash
git pull --ff-only origin main
```

Using `--ff-only` prevents Git from silently creating a merge commit while updating your local `main`.

### 3. Create a branch

For the first Medium article:

```bash
git switch -c content/django-rest-framework-files
```

Equivalent older syntax:

```bash
git checkout -b content/django-rest-framework-files
```

Check the current branch:

```bash
git branch --show-current
```

Expected:

```text
content/django-rest-framework-files
```

---

## Renaming a branch

### Rename the current local branch before pushing

If the branch has not been pushed yet:

```bash
git branch -m content/django-file-handling
```

Verify:

```bash
git branch --show-current
```

### Rename a local branch by name

If you are not currently on the branch:

```bash
git branch -m old-name new-name
```

Example:

```bash
git branch -m content/django-files content/django-rest-framework-files
```

### Rename a branch after it has already been pushed

Rename locally:

```bash
git branch -m content/django-rest-framework-files
```

Push the new branch and set its upstream:

```bash
git push -u origin content/django-rest-framework-files
```

Delete the old remote branch:

```bash
git push origin --delete old-branch-name
```

If a pull request already exists, update or recreate it as needed before deleting the old remote branch.

Check tracking information with:

```bash
git branch -vv
```

---

## Creating a new Hugo article

Articles live under:

```text
content/blog/
```

Use a page bundle so article-specific images can live beside the Markdown file.

For the first article:

```bash
mkdir -p content/blog/django-rest-framework-files
touch content/blog/django-rest-framework-files/index.md
```

Or, if the archetype is suitable:

```bash
hugo new content blog/django-rest-framework-files/index.md
```

The resulting structure should look like:

```text
content/
└── blog/
    └── django-rest-framework-files/
        ├── index.md
        └── images/
```

Create the images directory only when needed:

```bash
mkdir -p content/blog/django-rest-framework-files/images
```

---

## Front matter for a migrated Medium article

For an article that was originally published on Medium, preserve the original publication date and keep the Medium URL as provenance.

Example:

```yaml
---
title: "How To Handle Files In Django Rest Framework"
date: 2023-11-01
description: "Handling file uploads and storage patterns in Django REST Framework."
draft: false

tags:
  - Django
  - Django REST Framework
  - Python
  - File Uploads

categories:
  - Backend Engineering

medium_url: "https://medium.com/@pykhaled/..."
related_projects: []
---
```

Guidelines:

- Preserve the original publication date.
- Keep `draft: true` while editing.
- Change it to `draft: false` only when the article is ready.
- Keep `medium_url` for the existing Medium copy.
- For new website-first articles, the Hugo page should remain the canonical source.
- Do not point the website canonical URL back to Medium unless there is a deliberate migration reason.
- Use meaningful alt text for images.
- Prefer fenced code blocks with a language identifier.

Example:

````markdown
```python
class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()
```
````

---

## Preview the site locally

Install dependencies if needed:

```bash
npm ci
```

Run Hugo including drafts:

```bash
hugo server -D
```

Open the local URL shown by Hugo, normally:

```text
http://localhost:1313/
```

Review:

- Article title and description
- Heading hierarchy
- Code blocks
- Links
- Images and alt text
- Tags and categories
- Related content
- Mobile layout
- Medium attribution

---

## Run all local checks

Before committing, run the same checks expected by CI.

### Markdown lint

```bash
npm run lint:markdown
```

### Spell check

```bash
npm run spellcheck
```

If CSpell reports a legitimate technical term, add it to `.cspell.json` rather than disabling spell checking for the whole file.

### Content validation

```bash
npm run check:content
```

### Hugo production build

```bash
hugo --minify
```

A clean local validation flow is:

```bash
npm ci
npm run lint:markdown
npm run spellcheck
npm run check:content
hugo --minify
```

Fix all errors before pushing.

---

## Review your changes

Check the working tree:

```bash
git status
```

Review the diff:

```bash
git diff
```

If you have already staged files:

```bash
git diff --staged
```

For the first article you might see:

```text
content/blog/django-rest-framework-files/index.md
```

and any article images you added.

---

## Stage the change

Stage only the relevant files when practical:

```bash
git add content/blog/django-rest-framework-files/
```

If you also changed supporting configuration:

```bash
git add .cspell.json CONTRIBUTING.md
```

Review staged changes:

```bash
git diff --staged
```

---

## Commit

Use a clear conventional commit message.

For a new article:

```bash
git commit -m "content: add Django REST Framework files article"
```

Other examples:

```bash
git commit -m "content: update Django SaaS extensions note"
git commit -m "fix: correct Hugo asset pipeline"
git commit -m "chore: update CSpell dictionary"
git commit -m "docs: document contribution workflow"
```

Prefer a commit that represents one coherent change.

---

## Push the branch

For the first push:

```bash
git push -u origin content/django-rest-framework-files
```

After the upstream is set:

```bash
git push
```

---

## Open a pull request

Open a pull request from:

```text
content/django-rest-framework-files
```

into:

```text
main
```

The pull request should explain:

```text
What changed
Why it changed
How it was validated
Any migration or Medium-specific notes
```

Example:

```markdown
## What changed

- Added "How To Handle Files In Django Rest Framework"
- Preserved its original Medium publication date
- Added Medium provenance metadata
- Converted code samples to fenced Markdown blocks

## Validation

- [x] Markdown lint
- [x] CSpell
- [x] Content validator
- [x] Hugo production build
- [x] Local visual review
```

Wait for all required GitHub Actions checks to pass before merging.

---

## Addressing review or CI feedback

Make the requested edits on the same branch.

Then:

```bash
git status
git add <changed-files>
git commit -m "content: address article review feedback"
git push
```

The existing pull request updates automatically.

For a very small correction, you may amend the last commit before pushing:

```bash
git commit --amend
```

Avoid rewriting shared branch history after other people have based work on it.

---

## Merge

Once review and CI are successful, merge the pull request into `main`.

Use the repository's configured merge strategy.

For this site, squash merge is a good default for focused article or maintenance branches because it keeps `main` concise.

Example final commit:

```text
content: add Django REST Framework files article (#12)
```

Do not push directly to `main` to bypass failing checks.

---

## Clean up after merge

Switch back to `main`:

```bash
git switch main
```

Update it:

```bash
git pull --ff-only origin main
```

Delete the local branch:

```bash
git branch -d content/django-rest-framework-files
```

If GitHub did not already delete the remote branch:

```bash
git push origin --delete content/django-rest-framework-files
```

Prune stale remote references:

```bash
git fetch --prune
```

---

## Complete example: first Medium article

```bash
# Start from a clean and current main
git switch main
git pull --ff-only origin main

# Create the content branch
git switch -c content/django-rest-framework-files

# Create the Hugo page bundle
mkdir -p content/blog/django-rest-framework-files
touch content/blog/django-rest-framework-files/index.md

# Edit the article
$EDITOR content/blog/django-rest-framework-files/index.md

# Preview
hugo server -D

# Validate
npm ci
npm run lint:markdown
npm run spellcheck
npm run check:content
hugo --minify

# Inspect changes
git status
git diff

# Stage and commit
git add content/blog/django-rest-framework-files/
git commit -m "content: add Django REST Framework files article"

# Publish branch
git push -u origin content/django-rest-framework-files

# Open a PR into main and wait for CI/review
```

After the PR is merged:

```bash
git switch main
git pull --ff-only origin main
git branch -d content/django-rest-framework-files
git fetch --prune
```

---

## Quick reference

```text
main
  │
  ├── update from origin
  │
  ▼
content/django-rest-framework-files
  │
  ├── create article
  ├── preview locally
  ├── lint
  ├── spell check
  ├── validate content
  ├── build Hugo
  ├── commit
  └── push
       │
       ▼
   Pull Request
       │
       ├── CI
       ├── review
       └── merge
            │
            ▼
           main
            │
            ▼
      GitHub Pages deploy
```

## Contribution checklist

Before opening or merging a pull request:

- [ ] Branch was created from the latest `main`
- [ ] Branch name clearly describes the change
- [ ] Article metadata is complete
- [ ] Original Medium date is preserved when migrating an article
- [ ] `medium_url` is set when applicable
- [ ] `draft` is correct
- [ ] Code blocks specify their language
- [ ] Images have meaningful alt text
- [ ] `npm run lint:markdown` passes
- [ ] `npm run spellcheck` passes
- [ ] `npm run check:content` passes
- [ ] `hugo --minify` succeeds
- [ ] Changes were reviewed with `git diff`
- [ ] Pull request targets `main`
- [ ] Required GitHub Actions checks pass
