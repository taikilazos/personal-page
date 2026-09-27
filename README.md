# Hi there, I'm Taiki Papandreou 👋

## 🚀 About Me
- 🎓 Currently pursuing my MSc in AI at University of Amsterdam
- 🤖 AI Engineer & Machine Learning Specialist
- 🌍 Based in Netherlands, available for opportunities worldwide
- 🗣️ Fluent in English, Japanese, and Dutch
- 🔍 Actively seeking exciting opportunities starting September 2025

## 💻 Tech Stack
**AI & Machine Learning:**
- Python, Machine Learning, NLP
- OpenAI/LLMs, BERT/RoBERTa, RAG Systems
- TensorFlow, PyTorch

**Development:**
- FastAPI, Streamlit, HTML/CSS
- R, SQL, Git

## 🌟 What I Do
I specialize in building AI-powered solutions that solve real-world problems. My experience spans from chatbots to content generation platforms, with a passion for creating technology that's accessible and impactful.

## 📫 Let's Connect
- 📧 Email: [taiki.papandreou@gmail.com](mailto:taiki.papandreou@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/taiki-papandreou-lazos](https://linkedin.com/in/taiki-papandreou-lazos-a341981b5/)
- 🌐 Portfolio: [taikilazos.github.io/personal-page](https://taikilazos.github.io/personal-page)

## 📊 GitHub Stats
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
