# Ahmed Khaled — Personal Website

A Hugo-based personal website designed around a simple principle:

> The website is the canonical home of your professional identity; GitHub, Medium, and LinkedIn are distribution and evidence channels.

## Content model

The site has three primary content types:

### Projects

Case studies for things you build.

Use these to explain:

- the problem
- architecture
- engineering decisions
- outcomes
- lessons learned

### Blog

Polished long-form technical writing.

The website version should normally be the canonical source. Selected articles may be republished to Medium.

### Notes

Short technical observations, snippets, experiments, references, and lessons that do not need to become full articles.

## Local development

Install Hugo Extended, Node.js, and npm.

```bash
npm install
hugo server -D
```

## Create content

### Blog article

```bash
hugo new content blog/my-article/index.md
```

### Note

```bash
mkdir -p content/notes/my-note
cp archetypes/default.md content/notes/my-note/index.md
```

### Project

Create:

```text
content/projects/my-project/
├── index.md
└── images...
```

## Medium workflow

Write and publish on your website first.

Example front matter:

```yaml
---
title: "My Article"
date: 2026-09-11
description: "A useful description."
draft: false
tags:
  - django
  - architecture

medium_url: ""
canonicalURL: ""
---
```

After publishing to your site:

1. Import or republish the selected article on Medium.
2. Configure the Medium copy to point its canonical URL to the website article.
3. Add the resulting Medium URL to `medium_url`.
4. Keep your website as the source of truth.

Your Medium profile is configured in:

```text
data/social.yaml
```

Current value:

```text
https://medium.com/@pykhaled
```

## Homepage

The homepage is portfolio-oriented and includes:

- professional positioning
- featured projects
- latest long-form writing
- latest engineering notes
- expertise groups
- GitHub / Medium / LinkedIn / email links

## Related content

Hugo's related-content engine connects pages using shared metadata such as tags.

This lets a project page surface relevant articles and notes, and lets articles lead readers into related projects.

## SEO

The scaffold includes:

- canonical URLs
- sitemap generation
- robots.txt
- RSS
- meta descriptions
- OpenGraph metadata
- Twitter card metadata
- JSON-LD Person schema on the homepage
- JSON-LD BlogPosting schema for articles

Update `baseURL` before production.

Also update:

```text
static/robots.txt
```

with the final sitemap URL.

## Social profiles

Edit:

```text
data/social.yaml
```

and:

```text
hugo.toml
```

Replace the placeholder LinkedIn URL and email address.

## Quality pipeline

Pull requests and pushes run:

- Markdown linting
- spell checking
- custom content validation
- Hugo build
- Gitleaks secret scanning
- npm dependency audit

Pull requests also run broken-link checks.

## Deployment

`main` is deployed to GitHub Pages using:

```text
.github/workflows/deploy.yml
```

The flow is:

```text
Write content
    ↓
Pull request
    ↓
Content quality
Security
Links
Hugo build
    ↓
Merge to main
    ↓
Build production site
    ↓
Upload Pages artifact
    ↓
Deploy GitHub Pages
```

## Important placeholders

Before launch, update:

- `hugo.toml` → `baseURL`
- `hugo.toml` → LinkedIn and email
- `data/social.yaml`
- `static/robots.txt`
- GitHub project URLs
- sample content

## Recommended next steps

Once the content structure is stable, add:

- custom visual identity
- project screenshots
- article cover images
- analytics
- Lighthouse CI
- accessibility auditing
- HTML validation
- Medium article migration

## Asset pipeline

CSS and JavaScript live under:

```text
assets/
├── css/main.css
└── js/main.js
```

They are processed with Hugo Pipes using `resources.Get`, `minify`, and `fingerprint`.

This means the generated production files use cache-busting URLs similar to:

```text
/css/main.min.<hash>.css
/js/main.min.<hash>.js
```

Do not reference files under `assets/` directly with `/css/main.css` or `/js/main.js`; files under `assets/` are not copied to `public/` unless they are processed by Hugo Pipes.

If assets return 404 after a template change, clean generated output and rebuild:

```bash
rm -rf public resources/_gen
hugo server -D
```

For a production-style local check:

```bash
rm -rf public
hugo --minify --baseURL "https://pykhaled.github.io/"
find public -type f | grep -E '\.(css|js)$'
```

## Node tooling and lock file

`package-lock.json` is committed intentionally so GitHub Actions can use npm caching and `npm ci` without failing on a missing lock file.

This scaffold keeps the local dependency tree minimal. The content tools are pinned directly in `package.json` scripts:

```json
{
  "scripts": {
    "lint:markdown": "npx --yes markdownlint-cli2@0.17.2 \"**/*.md\"",
    "spellcheck": "npx --yes cspell@8.17.5 \"content/**/*.md\" \"README.md\""
  }
}
```

The CI setup can therefore safely run:

```bash
npm ci
npm run lint:markdown
npm run spellcheck
```

`npm ci` validates the committed lock file, while `npx` downloads the explicitly pinned tool versions when the checks run.

If you later add permanent Node dependencies, use:

```bash
npm install <package>
```

and commit both `package.json` and the regenerated `package-lock.json`.
