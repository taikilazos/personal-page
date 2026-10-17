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
python3 build.py
```

- Page content lives in `_pages/` (front matter + body HTML per page)
- Shared markup lives in `_templates/` (`head.html`, `footer.html`)
- The nav is defined once in `build.py` — change it there, rebuild, all pages update
- Outputs are written to the repo root and committed, so GitHub Pages serves them as-is
- Fonts are self-hosted (`assets/fonts/`, latin subset of Inter), images are resized JPEGs
