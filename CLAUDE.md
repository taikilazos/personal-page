# CLAUDE.md — Personal Page

## Project Overview
This is Taiki Papandreou's personal portfolio website, hosted on GitHub Pages.
URL: https://taikilazos.github.io/personal-page

## Stack
- Plain HTML/CSS/JS, no framework; a zero-dependency `build.py` assembles pages from `_pages/` + `_templates/`
- Static files served directly via GitHub Pages (built pages are committed)
- One page per project in `/projects/`, one per blog post in `/blog/`

## Owner Info
- Name: Taiki Papandreou
- Role: AI Developer at CribConnects
- Freelance company: TPL Company (tplcompany.org)
- Email: taiki.papandreou@gmail.com
- LinkedIn: https://www.linkedin.com/in/taiki-papandreou/
- X: https://x.com/LazosTaiki
- Languages: English, Japanese, Dutch

## Key Files
- `index.html` — homepage/about section
- `projects.html` — projects listing page
- `blog.html` — blog listing page
- `projects/` — individual project detail pages
- `blog/` — individual blog post pages
- `styles.css` — global styles
- `script.js` — global JS
- `myth.js` — homepage artwork (scene loops + scroll-scrubbed journeys film)
- `assets/` — PDFs, images, fonts, `myth-film/` videos
- `art/` — how the artwork was generated (fal.ai jobs, cost ledger, picks)

## Conventions
- Keep it simple — no frameworks; edit `_pages/`, then run `python3 build.py`
- New projects: copy `_templates/new-project.html` to `_pages/projects/projectN.html`
- New blog posts: copy `_templates/new-post.html` to `_pages/blog/<slug>.html`
- Preview with `python3 serve.py` (Range support, needed for the homepage film)
- Footer copyright year should stay current
