#!/usr/bin/env python3
"""Compile a workshop folder (numbered .md sections) into a single PDF.

Markdown and Mermaid diagrams are rendered in headless Chrome (marked + mermaid
from jsDelivr), then printed to PDF.

Usage: python3 tools/build_workshop_pdf.py Workshop-2
"""
import html
import json
import pathlib
import subprocess
import sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

COVER = {
    "Workshop-2": {
        "title": "Workshop No. 2 — Design Artifacts and System Modeling",
        "subtitle": "Public Module of the youth football tournament platform: public website, widgets and PWA",
        "date": "October 15, 2026",
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
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>
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
  mermaid.initialize({{ startOnLoad: false, theme: 'neutral', securityLevel: 'loose',
    flowchart: {{ useMaxWidth: true }}, class: {{ useMaxWidth: true }}, er: {{ useMaxWidth: true }} }});
  mermaid.run({{ querySelector: '.mermaid' }}).then(() => document.title += ' ✓');
</script>
</body></html>
"""


def main() -> None:
    folder = pathlib.Path(sys.argv[1]).resolve()
    meta = COVER[folder.name]
    sections = [p.read_text(encoding="utf-8") for p in sorted(folder.glob("[0-9][0-9]-*.md"))]
    page = TEMPLATE.format(
        title=html.escape(meta["title"]),
        subtitle=html.escape(meta["subtitle"]),
        date=meta["date"],
        team="<br>".join(html.escape(t) for t in TEAM),
        sections=json.dumps(sections),
    )
    html_path = folder / ".build.html"
    html_path.write_text(page, encoding="utf-8")
    pdf_path = folder / f"{folder.name}.pdf"
    subprocess.run(
        [
            CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--allow-file-access-from-files", "--virtual-time-budget=20000",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={pdf_path}", html_path.as_uri(),
        ],
        check=True, capture_output=True,
    )
    html_path.unlink()
    print(f"Wrote {pdf_path}")


if __name__ == "__main__":
    main()
