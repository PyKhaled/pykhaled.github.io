# Ahmed Khaled — Personal Website

A minimal, theme-agnostic Hugo scaffold for a personal engineering website.

## Sections

- Home
- About
- Projects
- Blog
- Contact

## Local development

Install Hugo Extended, then run:

```bash
hugo server -D
```

Open the local URL printed by Hugo.

## Create a new post

```bash
hugo new content blog/my-post/index.md
```

## Create a new project

Create a page bundle under:

```text
content/projects/my-project/
├── index.md
└── images...
```

## Structure

```text
.
├── .github/
├── archetypes/
├── assets/
├── content/
├── data/
├── layouts/
├── scripts/
├── static/
├── hugo.toml
└── README.md
```

## GitHub Pages

Update `baseURL` in `hugo.toml` to your production URL.

The included workflow deploys `main` to GitHub Pages.

## Content quality

The CI configuration includes:

- Hugo build
- Markdown linting
- Spell checking
- Vale writing checks
- Broken-link checks
- Basic article/front-matter validation
- Secret scanning
- npm audit when a package lock exists

## Customize

Start with:

- `hugo.toml`
- `data/profile.yaml`
- `assets/css/main.css`
- `content/about/index.md`
- `content/projects/`
- `content/blog/`
