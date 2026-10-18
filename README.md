# Taiki Papandreou

## About Me
- AI Developer at CribConnects
- Founder of TPL Company (tplcompany.org) — freelance AI consultancy
- MSc AI graduate from University of Amsterdam
- Based in Netherlands
- Fluent in English, Japanese, and Dutch

## Tech Stack
**AI & Machine Learning:**
- Python, Machine Learning, NLP
- OpenAI/LLMs, BERT/RoBERTa, RAG Systems
- TensorFlow, PyTorch

**Development:**
- FastAPI, Streamlit, HTML/CSS
- R, SQL, Git

## What I Do
I build AI-powered solutions that solve real-world problems — from chatbots to content generation platforms.

## Connect
- Email: [taiki.papandreou@gmail.com](mailto:taiki.papandreou@gmail.com)
- LinkedIn: [linkedin.com/in/taiki-papandreou](https://www.linkedin.com/in/taiki-papandreou/)
- Portfolio: [taikilazos.github.io/personal-page](https://taikilazos.github.io/personal-page)

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=TaikiLazos&show_icons=true&theme=default&hide_border=true)

![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=TaikiLazos&layout=compact&theme=default&hide_border=true)
---
*"Creating AI solutions that make technology more accessible"* ✨
## 🛠 Building the site

The site is assembled by a zero-dependency build script — no framework, no node_modules:

```
python3 build.py      # build every page from _pages/ into the repo root
python3 serve.py      # preview at http://127.0.0.1:8000/
```

- Page content lives in `_pages/` (front matter + body HTML per page)
- Shared markup lives in `_templates/` (`head.html`, `footer.html`); new pages start from
  `_templates/new-project.html` or `_templates/new-post.html`, copied into `_pages/projects/` or `_pages/blog/`
- The nav is defined once in `build.py` — change it there, rebuild, all pages update
- Outputs are written to the repo root and committed, so GitHub Pages serves them as-is
- Fonts are self-hosted (`assets/fonts/`): Shippori Mincho for headings, Zen Kaku Gothic New for text
- Preview with `serve.py`, not `python3 -m http.server`: the homepage film is scrubbed by the scroll,
  which needs HTTP Range requests (GitHub Pages supports them, the built-in server does not)

## 🎨 The homepage artwork

The homepage is one journey west along the Silk Road, from Japan through China to Greece:
a kitsune shrine, a dragon over ink mountains, and Pegasus. `myth.js` plays each scene as a loop
while you read and scrubs the journeys between them with the scroll.

- Site files: `assets/myth-film/` (scene loops, the journeys film, posters)
- How they were made: `art/` — `gen.py` runs a job file from `art/jobs/` on fal.ai and logs its
  cost in `art/ledger.csv`; `review.py` checks a video's loop seam and motion; `picks.md` records
  which drafts were chosen. Drafts and reference images stay local (`art/out/`, `art/refs/` are ignored).
