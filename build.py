#!/usr/bin/env python3
"""Assemble the static site from _pages/ sources and _templates/ partials.

Zero dependencies. After editing anything under _pages/ or _templates/,
run `python3 build.py` — outputs land in the repo root (and subdirs),
ready for GitHub Pages.

Front matter (between --- lines) supports:
    title        <title> text
    nav          projects | blog  (which nav link is marked current)
    body_class   optional class on <body> (the homepage uses it to float the header over the film)
    description  optional per-page meta description
    extra_head   folded block (key: |) of extra <head> content
    footer_extra folded block of extra footer content
    extra_foot   folded block of scripts before </body>
"""

import pathlib
import re
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = ROOT / "_pages"
TEMPLATES = ROOT / "_templates"

DEFAULT_DESCRIPTION = (
    "Taiki Papandreou - AI engineer in the Netherlands building AI systems "
    "that ship into regulated businesses."
)

NAV_ITEMS = [
    ("projects", "Projects", "projects.html"),
    ("blog", "Blog", "blog.html"),
    ("cv", "CV", "assets/Taiki_CV.pdf"),
]


def parse_source(text):
    """Split front matter (between --- lines) from body content."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("page is missing front matter")
    meta, body = match.groups()
    fm = {}
    key = None
    for line in meta.splitlines():
        if line.startswith((" ", "\t")) and key is not None:
            fm[key] += "\n" + line
        elif ":" in line:
            key, value = line.split(":", 1)
            fm[key.strip()] = value.strip()
    # Unfold indented values (key: | blocks)
    for key, value in fm.items():
        if value == "|":
            fm[key] = ""
        elif value.startswith("|\n"):
            fm[key] = textwrap.dedent(value[2:]).strip("\n")
    return fm, body


def render_nav(active, base):
    items = []
    for key, label, href in NAV_ITEMS:
        current = ' aria-current="page"' if key == active else ""
        items.append(
            f'                <li><a href="{base}{href}" class="nav-link"{current}>{label}</a></li>'
        )
    return "\n".join(items)


def render(source):
    fm, body = parse_source(source.read_text())
    rel = source.relative_to(PAGES)
    base = "../" * (len(rel.parts) - 1)

    head = (TEMPLATES / "head.html").read_text()
    head = head.replace("{{title}}", fm.get("title", "Taiki Papandreou"))
    head = head.replace("{{base}}", base)
    head = head.replace(
        "{{description}}", fm.get("description", DEFAULT_DESCRIPTION)
    )
    head = head.replace("{{extra_head}}", fm.get("extra_head", ""))
    head = head.replace("{{nav}}", render_nav(fm.get("nav", ""), base))
    head = head.replace("{{body_class}}", fm.get("body_class", ""))

    foot = (TEMPLATES / "footer.html").read_text()
    foot = foot.replace("{{base}}", base)
    foot = foot.replace("{{footer_extra}}", fm.get("footer_extra", ""))
    foot = foot.replace("{{extra_foot}}", fm.get("extra_foot", ""))

    return head + body + foot


def main():
    rebuilt = []
    for source in sorted(PAGES.rglob("*.html")):
        out = ROOT / source.relative_to(PAGES)
        out.write_text(render(source))
        rebuilt.append(str(out.relative_to(ROOT)))
    for line in rebuilt:
        print(f"  built {line}")
    print(f"\n{len(rebuilt)} pages built.")


if __name__ == "__main__":
    main()
