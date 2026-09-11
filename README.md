# Hugo Personal Website - GitHub CI/CD

This repository configuration turns a Hugo personal site into a small automated publishing pipeline. Pull requests are checked for writing quality, Markdown quality, broken links, generated HTML problems, secrets, dependency vulnerabilities, accessibility, SEO, and performance. Pushes to `main` deploy the production site to GitHub Pages.

## Pipeline

```text
Write / edit content
        |
        v
Pull request
        |
        +--> Content Quality
        |     - markdownlint
        |     - cspell
        |     - Vale
        |     - Hugo article validator
        |
        +--> Site Quality
        |     - Hugo production build
        |     - Lychee link checker
        |     - HTMLProofer
        |
        +--> Security
        |     - Gitleaks
        |     - npm audit
        |
        +--> Lighthouse
              - Performance
              - Accessibility
              - Best practices
              - SEO

Merge to main
        |
        v
GitHub Pages build + deployment
```

## Included files

```text
.github/
├── dependabot.yml
└── workflows/
    ├── content-quality.yml
    ├── deploy.yml
    ├── lighthouse.yml
    ├── security.yml
    └── site-quality.yml

scripts/
└── validate_content.py

.vale/
└── styles/PersonalSite/
    ├── Terms.yml
    └── Todo.yml

.markdownlint.json
.lychee.toml
.vale.ini
cspell.json
lighthouserc.json
README.md
```

## What each workflow does

### Content Quality

Runs on pull requests and pushes to `main`.

- `markdownlint-cli2` checks Markdown structure and formatting.
- `cspell` catches spelling mistakes while allowing common engineering vocabulary.
- Vale performs editorial/style checks. It is intentionally non-blocking by default because prose rules can be subjective.
- `scripts/validate_content.py` enforces publishing rules for Hugo Markdown content.

The custom validator currently checks:

- YAML front matter exists.
- `title`, `date`, and `description` exist.
- Description is no longer than 160 characters.
- Posts have tags.
- `draft: true` is not accidentally published.
- At most one H1 is present.
- Heading levels do not skip levels such as H2 -> H4.
- Markdown images have alt text.
- No localhost/127.0.0.1 URLs remain.
- No TODO/FIXME/TBD placeholders remain.

Edit `scripts/validate_content.py` to match your own content model.

### Site Quality

Builds the real Hugo output and then checks it.

- Builds Hugo with production settings.
- Checks links in both source Markdown and generated HTML using Lychee.
- Runs HTMLProofer against `public/`.
- Uploads `public/` as a short-lived workflow artifact for troubleshooting.

`https://example.invalid/` is intentionally used as the CI build base URL. Replace it if your theme needs your real domain during validation.

### Security

- Gitleaks scans the repository history for accidentally committed credentials and secrets.
- `npm audit --audit-level=high` runs when an npm lockfile exists.
- The workflow also runs weekly so new vulnerability data can catch an existing dependency later.

### Lighthouse

Runs Lighthouse CI against the built static site.

Default thresholds:

| Category | Threshold | Result |
| --- | ---: | --- |
| Performance | 85% | warning |
| Accessibility | 95% | failure |
| Best practices | 95% | warning |
| SEO | 95% | failure |

Change these in `lighthouserc.json`.

The example configuration checks `/` and `/posts/`. Remove or change `/posts/` if that route does not exist in your site.

### Deploy

Pushes to `main` build and deploy the site through GitHub Pages using the official Pages Actions flow.

The workflow preserves the same basic deployment architecture you were already using:

1. Checkout repository and submodules.
2. Install Hugo Extended and Dart Sass.
3. Configure GitHub Pages.
4. Install npm dependencies if a lockfile exists.
5. Build Hugo using the Pages base URL.
6. Upload `public/` as the Pages artifact.
7. Deploy to the `github-pages` environment.

## First-time GitHub configuration

In the repository settings:

1. Open **Settings -> Pages**.
2. Set **Source** to **GitHub Actions**.
3. Open **Settings -> Actions -> General** and ensure Actions are allowed.
4. Open **Settings -> Branches** (or Rulesets) and protect `main`.
5. Require the CI checks you want before merging.

Recommended required checks:

```text
Content Quality / Markdown, spelling, style, and article validation
Site Quality / Hugo build, links, generated HTML
Security / Secret scanning
Security / Dependency audit
Lighthouse / Performance, accessibility, best practices, SEO
```

You may initially leave Vale and Lighthouse performance/best-practice findings non-blocking while you tune the rules.

## Content front matter convention

A typical post should look like:

```yaml
---
title: "Building a Better Django Deployment Pipeline"
date: 2026-09-11
description: "A practical approach to improving Django CI/CD with automated quality and security checks."
tags:
  - Django
  - DevOps
  - CI/CD
draft: false
---
```

If your Hugo theme uses TOML front matter (`+++`) or JSON front matter, extend `scripts/validate_content.py` before enabling it as a required check.

## Custom spelling dictionary

Add personal names, products, and technical vocabulary to `cspell.json`:

```json
{
  "words": [
    "Django",
    "Kubernetes",
    "PostgreSQL",
    "YourProjectName"
  ]
}
```

Avoid simply disabling spelling checks for entire folders. A small curated dictionary gives much better results.

## Vale editorial rules

This bundle starts with intentionally small rules so the pipeline does not become noisy.

`PersonalSite/Terms.yml` standardizes common technology names such as `GitHub`, `JavaScript`, and `PostgreSQL`.

`PersonalSite/Todo.yml` warns when editorial placeholders are left in content.

You can later add rules for:

- sentence length;
- passive voice;
- preferred terminology;
- heading capitalization;
- inclusive language;
- first-person writing style;
- banned marketing phrases.

## Link checking

`.lychee.toml` contains common exclusions for mail links, telephone links, placeholder domains, and local development URLs.

If a legitimate site blocks automated requests or returns `429`, add a targeted exclusion instead of disabling external link checking completely.

## Dependabot

`.github/dependabot.yml` checks weekly for updates to:

- GitHub Actions;
- npm dependencies.

If your Hugo theme is a Git submodule, Dependabot will not upgrade that submodule automatically. Update the theme reference deliberately and review the result.

## Recommended branch strategy

For a personal site, a simple workflow is enough:

```text
main
  ^
  |
feature/article-* or feature/site-*
  |
Pull request + automated checks
```

After the pull request passes, merge to `main`; the deployment workflow publishes the result.

## Recommended repository rules

Protect `main` with:

- require a pull request before merging;
- require status checks;
- require branches to be up to date before merging;
- block force pushes;
- block deletion;
- optionally require signed commits.

For a one-person repository, approval requirements are optional. The automated checks are more useful than forcing yourself to approve your own PR.

## Local commands

Install the content-quality tools:

```bash
npm install --global markdownlint-cli2 cspell @lhci/cli
```

Run checks locally:

```bash
markdownlint-cli2 "**/*.md" "#public/**" "#themes/**"
cspell "content/**/*.md" README.md --no-progress
python3 scripts/validate_content.py content
hugo --minify
```

For Vale, install it with your preferred package manager and run:

```bash
vale content
```

## Important customizations before enabling every check

Review these values first:

1. `HUGO_VERSION` in the workflows.
2. URLs in `lighthouserc.json`.
3. Your content/front-matter fields in `scripts/validate_content.py`.
4. Your personal dictionary in `cspell.json`.
5. External-link exclusions in `.lychee.toml`.
6. Lighthouse thresholds.
7. Your Hugo theme's Node.js and Dart Sass requirements.

## Optional future improvements

Once this baseline is stable, useful additions include visual regression screenshots, image-size budgets, WebP/AVIF enforcement, Open Graph image validation, RSS/feed validation, structured-data validation, dead-code checks for CSS/JavaScript, scheduled external-link scans, and preview deployments for pull requests.
