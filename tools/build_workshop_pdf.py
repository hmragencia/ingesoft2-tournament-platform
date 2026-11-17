#!/usr/bin/env python3
"""Compile a workshop folder (numbered .md sections) into a single PDF.

Markdown and Mermaid diagrams are rendered in headless Chrome (marked + mermaid
from jsDelivr), then printed to PDF. A diagram opts into orthogonal routing with
`layout: elk` in its Mermaid front matter (the class and table diagrams do).

Usage:
  python3 tools/build_workshop_pdf.py Workshop-2                      # every section -> Workshop-2.pdf
  python3 tools/build_workshop_pdf.py Workshop-2 --sections 06 07 08 --out Workshop-2-part-2.pdf
"""
import argparse
import html
import json
import pathlib
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
REPO_URL = "https://github.com/hmragencia/ingesoft2-tournament-platform"

COVER = {
    "Workshop-2": {
        "title": "Workshop No. 2 — Design Artifacts and System Modeling",
        "subtitle": "Public Module of the youth football tournament platform: public website, widgets and PWA. Complete document: parts 1 and 2, revised after the lecturer's feedback",
        "date": "November 17, 2026",
    },
    "Workshop-2-part-2": {
        "title": "Workshop No. 2 — Design Artifacts and System Modeling",
        "subtitle": "Part 2: business process models and architecture diagram",
        "date": "October 30, 2026",
    },
}

TEAM = [
    "Nicolás Molano Barón — Product Owner",
    "Luis Gabriel Peraza Muñoz — Scrum Master",
    "Rafael Otero Erazo — Developer",
    "Sebastián Clavijo Tocasuchyl — Developer",
    "Nicolás Gómez Lozano — Developer",
]

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>
  @page {{ size: Letter; margin: 18mm 16mm; }}
  body {{ font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #111; }}
  h1 {{ font-size: 19pt; border-bottom: 2px solid #0B6E4F; padding-bottom: 4px; break-before: page; }}
  h2 {{ font-size: 14pt; color: #0B6E4F; margin-top: 18px; }}
  h3 {{ font-size: 11.5pt; margin: 14px 0 4px; }}
  h2, h3, p:has(+ table), p:has(+ .mermaid) {{ break-after: avoid-page; }}
  table {{ border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9pt; break-inside: auto; }}
  tr {{ break-inside: avoid; }}
  th, td {{ border: 1px solid #bbb; padding: 4px 6px; vertical-align: top; text-align: left; }}
  th {{ background: #e8f3ee; }}
  code {{ font-family: Menlo, monospace; font-size: 8.5pt; background: #f3f3f3; padding: 0 2px; }}
  pre code {{ display: block; white-space: pre-wrap; padding: 8px; }}
  img {{ max-width: 100%; max-height: 225mm; display: block; margin: 8px auto; border: 1px solid #ddd; }}
  .mermaid {{ text-align: center; margin: 10px 0; break-inside: avoid; }}
  .mermaid svg {{ max-width: 100%; height: auto; max-height: 230mm; }}
  .cover {{ text-align: center; padding-top: 70mm; }}
  .cover h1 {{ border: 0; break-before: auto; font-size: 24pt; }}
  .cover p {{ margin: 4px 0; }}
  .toc {{ break-before: page; }}
  @page landscape {{ size: Letter landscape; margin: 12mm; }}
  .landscape {{ page: landscape; break-before: page; }}
  .landscape img {{ max-height: 182mm; border: 0; }}
  .landscape .mermaid svg {{ max-height: 175mm; }}
</style></head>
<body>
<section class="cover">
  <p>Software Engineering II — 2026-II<br>Computer Engineering Program, School of Engineering<br>Universidad Nacional de Colombia</p>
  <h1>{title}</h1>
  <p><em>{subtitle}</em></p>
  <p style="margin-top:20mm"><strong>Team</strong><br>{team}</p>
  <p style="margin-top:8mm"><strong>Lecturer</strong><br>Eng. Liliana Marcela Olarte Mesa, M.Sc.</p>
  <p style="margin-top:8mm">{date}</p>
</section>
<main id="doc"></main>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@12.3.0/dist/mermaid.esm.min.mjs';
  import elkLayouts from 'https://cdn.jsdelivr.net/npm/@mermaid-js/layout-elk@1.0.2/dist/mermaid-layout-elk.esm.min.mjs';
  mermaid.registerLayoutLoaders(elkLayouts);
  const sections = {sections};
  const doc = document.getElementById('doc');
  const renderer = new marked.Renderer();
  const baseCode = renderer.code.bind(renderer);
  renderer.code = (code, lang) => lang === 'mermaid'
    ? '<div class="mermaid">' + code.replace(/</g, '&lt;') + '</div>'
    : baseCode(code, lang);
  for (const md of sections) {{
    const s = document.createElement('section');
    s.innerHTML = marked.parse(md, {{ renderer }});
    doc.appendChild(s);
  }}
  // Links to other files of the workshop point to the public repository, so they work from the PDF.
  const repoBase = {repo_base};
  if (repoBase) for (const a of doc.querySelectorAll('a[href]')) {{
    const href = a.getAttribute('href');
    if (!/^([a-z]+:|#)/i.test(href)) a.setAttribute('href', repoBase + href);
  }}
  mermaid.initialize({{ startOnLoad: false, theme: 'neutral', securityLevel: 'loose',
    flowchart: {{ useMaxWidth: true, wrappingWidth: 420 }}, class: {{ useMaxWidth: true, hideEmptyMembersBox: true }}, er: {{ useMaxWidth: true }} }});
  // Render one at a time and insert the results at the end: diagrams repeat
  // class names, and ELK looks nodes up in the live DOM.
  const blocks = [...document.querySelectorAll('.mermaid')];
  const rendered = [];
  for (const [i, block] of blocks.entries()) {{
    rendered.push((await mermaid.render('diagram-' + i, block.textContent)).svg);
  }}
  blocks.forEach((block, i) => {{ block.innerHTML = rendered[i]; }});
  document.title += ' ✓';
</script>
</body></html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--sections", nargs="*", help="two-digit section prefixes to include (default: all)")
    parser.add_argument("--out", help="PDF file name inside the folder (default: <folder>.pdf)")
    args = parser.parse_args(sys.argv[1:])
    folder = pathlib.Path(args.folder).resolve()
    out_name = args.out or f"{folder.name}.pdf"
    meta = COVER[pathlib.Path(out_name).stem]
    files = sorted(folder.glob("[0-9][0-9]-*.md"))
    if args.sections:
        files = [f for f in files if f.name[:2] in args.sections]
    sections = [p.read_text(encoding="utf-8") for p in files]
    page = TEMPLATE.format(
        title=html.escape(meta["title"]),
        subtitle=html.escape(meta["subtitle"]),
        date=meta["date"],
        team="<br>".join(html.escape(t) for t in TEAM),
        sections=json.dumps(sections),
        repo_base=json.dumps(f"{REPO_URL}/blob/main/{folder.name}/" if folder.name.startswith("Workshop-") else ""),
    )
    html_path = folder / ".build.html"
    html_path.write_text(page, encoding="utf-8")
    pdf_path = folder / out_name
    subprocess.run(
        [
            CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--allow-file-access-from-files", "--virtual-time-budget=90000",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={pdf_path}", html_path.as_uri(),
        ],
        check=True, capture_output=True,
    )
    html_path.unlink()
    print(f"Wrote {pdf_path}")


if __name__ == "__main__":
    main()
