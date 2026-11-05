#!/usr/bin/env python3
"""Build the annex with the complete class diagram of a workshop.

Merges every Mermaid class diagram of <folder>/03-class-diagram.md into one model,
lays it out with Mermaid + ELK in headless Chrome and writes, inside <folder>/annex:
  - class-diagram-full.drawio.xml: editable XML, opens in diagrams.net
  - Workshop-2-class-diagram-annex.pdf: the same diagram on one large page

Both files use the same layout, so they show the same drawing.

Usage: python3 tools/build_class_annex.py Workshop-2
"""
import argparse
import json
import pathlib
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@12.3.0/dist/mermaid.esm.min.mjs"
ELK = "https://cdn.jsdelivr.net/npm/@mermaid-js/layout-elk@1.0.2/dist/mermaid-layout-elk.esm.min.mjs"
TITLE = "Workshop No. 2 — Annex: complete class diagram of the Public Module"
XML_NAME = "class-diagram-full.drawio.xml"
PDF_NAME = "Workshop-2-class-diagram-annex.pdf"

RELATION = re.compile(
    r'^\s*(\w+)\s+(?:"([^"]+)"\s+)?(<\|--|\*--|o--|\.\.>|-->|--)\s+(?:"([^"]+)"\s+)?(\w+)(?:\s*:\s*(.+?))?\s*$'
)

EDGE_STYLES = {
    "*--": "startArrow=diamondThin;startFill=1;startSize=16;endArrow=none;",
    "o--": "startArrow=diamondThin;startFill=0;startSize=16;endArrow=none;",
    "-->": "endArrow=open;endFill=0;endSize=10;",
    "--": "endArrow=none;",
    "..>": "dashed=1;endArrow=open;endFill=0;endSize=10;",
    "<|--": "startArrow=block;startFill=0;startSize=12;endArrow=none;",
}


def parse(markdown: str):
    """Return the merged classes and the relations of all the views, without repeats."""
    classes: dict = {}
    relations: list = []
    for block in re.findall(r"```mermaid\n(.*?)```", markdown, re.S):
        lines = block.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            head = re.match(r"^class (\w+)(:::\w+)?( \{)?$", line)
            if head:
                name, is_reference, opens = head.groups()
                body = []
                if opens:
                    i += 1
                    while lines[i].strip() != "}":
                        body.append(lines[i].strip())
                        i += 1
                # A reference only repeats a class defined elsewhere: the definition wins.
                if not is_reference or name not in classes:
                    if not is_reference:
                        classes[name] = body
                    else:
                        classes.setdefault(name, [])
            else:
                match = RELATION.match(lines[i])
                if match and match.groups() not in relations:
                    relations.append(match.groups())
            i += 1
    return classes, relations


def mermaid_source(classes: dict, relations: list) -> str:
    out = ["---", "config:", "  layout: elk", "---", "classDiagram", "  direction LR"]
    for name, body in classes.items():
        if body:
            out += [f"  class {name} {{"] + [f"    {line}" for line in body] + ["  }"]
        else:
            out.append(f"  class {name}")
    for left, m1, rel, m2, right, label in relations:
        text = f"  {left}"
        text += f' "{m1}"' if m1 else ""
        text += f" {rel}"
        text += f' "{m2}"' if m2 else ""
        text += f" {right}"
        text += f" : {label}" if label else ""
        out.append(text)
    return "\n".join(out) + "\n"


def html_page(source: str, for_print: bool) -> str:
    # The layout pass keeps the natural size; the print pass scales the drawing to the page.
    sizing = "width: 100%; height: auto; max-height: 530mm;" if for_print else "width: auto; height: auto;"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{TITLE}</title>
<style>
  @page {{ size: 841mm 594mm; margin: 12mm; }}
  body {{ margin: 0; font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; background: #fff; }}
  h1 {{ font-size: 26pt; margin: 0; color: #0B6E4F; }}
  p {{ font-size: 13pt; margin: 4px 0 8mm; }}
  #out svg {{ {sizing} display: block; margin: 0 auto; }}
</style></head><body>
<h1>{TITLE}</h1>
<p>Classes with the «read-only» stereotype are projections of the tournament-management platform; the rest are owned by the module.
«PK» marks a primary key and «FK» a foreign key. Same model as sections 3.1 to 3.3 of the workshop, shown together.</p>
<div id="out"></div><pre id="layout" style="display:none"></pre>
<script type="module">
  import mermaid from '{MERMAID}';
  import elk from '{ELK}';
  mermaid.registerLayoutLoaders(elk);
  mermaid.initialize({{ startOnLoad: false, theme: 'neutral', securityLevel: 'loose',
    class: {{ useMaxWidth: {'true' if for_print else 'false'}, hideEmptyMembersBox: true }} }});
  const {{ svg }} = await mermaid.render('annex', {json.dumps(source)});
  const out = document.getElementById('out');
  out.innerHTML = svg;
  const root = out.querySelector('svg');
  const origin = root.getBoundingClientRect();
  const nodes = [...root.querySelectorAll('g.node')].map(n => {{
    const r = n.getBoundingClientRect();
    return {{ id: n.id, x: r.x - origin.x, y: r.y - origin.y, w: r.width, h: r.height }};
  }});
  const edges = [...root.querySelectorAll('path[id*="-id_"]')].map(p => {{
    const m = p.getCTM();
    return {{ id: p.id, d: p.getAttribute('d'), m: [m.a, m.b, m.c, m.d, m.e, m.f] }};
  }});
  document.getElementById('layout').textContent = JSON.stringify({{ nodes, edges, w: origin.width, h: origin.height }});
</script></body></html>
"""


def chrome(page: pathlib.Path, *flags: str) -> str:
    result = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--allow-file-access-from-files", "--virtual-time-budget=90000",
         "--window-size=9000,6000", *flags, page.as_uri()],
        check=True, capture_output=True, text=True,
    )
    return result.stdout


def corners(edge: dict) -> list:
    """Points of a routed edge: its ends and the corner of each bend."""
    a, b, c, d, e, f = edge["m"]
    numbers = re.findall(r"([MLQCTHVZA])|(-?\d+(?:\.\d+)?(?:e-?\d+)?)", edge["d"], re.I)
    points: list = []
    command, buffer = None, []
    for letter, number in numbers:
        if letter:
            command, buffer = letter.upper(), []
            continue
        buffer.append(float(number))
        if command in ("M", "L", "T") and len(buffer) == 2:
            points.append(tuple(buffer))
            buffer = []
        elif command == "Q" and len(buffer) == 4:
            points.append((buffer[0], buffer[1]))  # control point: the corner of the rounded bend
            buffer = []
        elif command == "C" and len(buffer) == 6:
            points.append((buffer[4], buffer[5]))
            buffer = []
        elif command == "A" and len(buffer) == 7:  # line jump over another edge: only its end matters
            points.append((buffer[5], buffer[6]))
            buffer = []
    placed = [(a * x + c * y + e, b * x + d * y + f) for x, y in points]
    clean: list = []
    for point in placed:
        if not clean or abs(point[0] - clean[-1][0]) > 0.5 or abs(point[1] - clean[-1][1]) > 0.5:
            clean.append(point)
    # Keep only real bends: drop points that sit on a straight run.
    bends = clean[:1]
    for i in range(1, len(clean) - 1):
        (x0, y0), (x1, y1), (x2, y2) = bends[-1], clean[i], clean[i + 1]
        if abs((x1 - x0) * (y2 - y1) - (y1 - y0) * (x2 - x1)) > 1:
            bends.append(clean[i])
    if len(clean) > 1:
        bends.append(clean[-1])
    return bends


def uml_member(line: str) -> str:
    text = line.replace("~", "<", 1).replace("~", ">", 1)
    return re.sub(r"\)\s+(?=\S)", "): ", text)


def add_cell(root, cell_id, value="", style="", parent="1", geometry=None, **attrs):
    cell = ET.SubElement(root, "mxCell", id=cell_id, value=value, style=style, parent=parent, **attrs)
    if geometry is not None:
        ET.SubElement(cell, "mxGeometry", **{k: str(v) for k, v in geometry.items()}, **{"as": "geometry"})
    return cell


def build_xml(classes: dict, relations: list, layout: dict) -> ET.ElementTree:
    mx = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(mx, "diagram", id="class-diagram-full", name="Complete class diagram")
    model = ET.SubElement(
        diagram, "mxGraphModel", dx="1400", dy="900", grid="1", gridSize="10", guides="1", tooltips="1",
        connect="1", arrows="1", fold="1", page="1", pageScale="1",
        pageWidth=str(round(layout["w"]) + 80), pageHeight=str(round(layout["h"]) + 80), math="0", shadow="0",
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    boxes = {}
    for node in layout["nodes"]:
        found = re.search(r"classId-(\w+?)-\d+$", node["id"])
        if found:
            boxes[found.group(1)] = node
    missing = set(classes) - set(boxes)
    if missing:
        raise SystemExit(f"Classes without a layout box: {sorted(missing)}")

    margin = 40
    for name, body in classes.items():
        box = boxes[name]
        stereotype = next((re.sub(r"[<>]", "", line) for line in body if line.startswith("<<")), None)
        members = [line for line in body if not line.startswith("<<")]
        attributes = [line for line in members if "(" not in line]
        methods = [line for line in members if "(" in line]
        start = 44 if stereotype else 28
        title = f"<b>{name}</b>" if stereotype != "abstract" else f"<b><i>{name}</i></b>"
        value = f"«{stereotype}»<br>{title}" if stereotype else title
        fill = "#F2F2F2" if stereotype and "read-only" in stereotype else "#FFFFFF"
        height = max(box["h"], start + 18 * len(members) + (8 if attributes and methods else 0) + 4)
        add_cell(
            root, f"c_{name}", value,
            "swimlane;html=1;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;"
            f"startSize={start};horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;"
            f"marginBottom=0;whiteSpace=wrap;fontSize=12;fillColor={fill};strokeColor=#666666;",
            vertex="1",
            geometry={"x": round(box["x"] + margin), "y": round(box["y"] + margin),
                      "width": round(box["w"]), "height": round(height)},
        )
        row = 18
        y = start
        rows = [(line, False) for line in attributes]
        if attributes and methods:
            rows.append((None, True))
        rows += [(line, False) for line in methods]
        for k, (line, separator) in enumerate(rows):
            geometry = {"y": round(y), "width": round(box["w"]), "height": 8 if separator else row}
            if separator:
                add_cell(
                    root, f"c_{name}_r{k}", "",
                    "line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;"
                    "spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;strokeColor=#666666;",
                    parent=f"c_{name}", vertex="1", geometry=geometry,
                )
                y += 8
            else:
                add_cell(
                    root, f"c_{name}_r{k}", uml_member(line),
                    "text;html=0;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=6;"
                    "spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;"
                    "whiteSpace=nowrap;fontSize=12;",
                    parent=f"c_{name}", vertex="1", geometry=geometry,
                )
                y += row

    routed = layout["edges"]
    used = set()
    for k, (left, m1, rel, m2, right, label) in enumerate(relations):
        # Mermaid names each edge id_<first>_<second>_<n>, in either order.
        candidates = [e for e in routed if e["id"] not in used and
                      re.search(rf"id_({left}_{right}|{right}_{left})_\d+$", e["id"])]
        style = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;fontSize=11;" + EDGE_STYLES[rel]
        edge = add_cell(root, f"e_{k}", label or "", "", source=f"c_{left}", target=f"c_{right}", edge="1")
        geometry = ET.SubElement(edge, "mxGeometry", relative="1", **{"as": "geometry"})
        if candidates:
            chosen = candidates[0]
            used.add(chosen["id"])
            path = [(x + margin, y + margin) for x, y in corners(chosen)]
            start_box, end_box = boxes[left], boxes[right]
            # Orient the route from the source class to the target class.
            cx, cy = start_box["x"] + margin + start_box["w"] / 2, start_box["y"] + margin + start_box["h"] / 2
            ex, ey = end_box["x"] + margin + end_box["w"] / 2, end_box["y"] + margin + end_box["h"] / 2
            if (path[0][0] - cx) ** 2 + (path[0][1] - cy) ** 2 > (path[-1][0] - cx) ** 2 + (path[-1][1] - cy) ** 2:
                path.reverse()
            if len(path) >= 2:
                def anchor(point, box):
                    fx = min(max((point[0] - box["x"] - margin) / box["w"], 0), 1)
                    fy = min(max((point[1] - box["y"] - margin) / box["h"], 0), 1)
                    return round(fx, 3), round(fy, 3)
                exit_x, exit_y = anchor(path[0], start_box)
                entry_x, entry_y = anchor(path[-1], end_box)
                style += (f"exitX={exit_x};exitY={exit_y};exitDx=0;exitDy=0;exitPerimeter=0;"
                          f"entryX={entry_x};entryY={entry_y};entryDx=0;entryDy=0;entryPerimeter=0;")
            if len(path) > 2:
                points = ET.SubElement(geometry, "Array", **{"as": "points"})
                for x, y in path[1:-1]:
                    ET.SubElement(points, "mxPoint", x=str(round(x)), y=str(round(y)))
        edge.set("style", style)
        label_style = "edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=11;labelBackgroundColor=#FFFFFF;"
        if m1:
            add_cell(root, f"e_{k}_m1", m1, label_style, parent=f"e_{k}", vertex="1", connectable="0",
                     geometry={"x": "-0.85", "relative": "1"})
        if m2:
            add_cell(root, f"e_{k}_m2", m2, label_style, parent=f"e_{k}", vertex="1", connectable="0",
                     geometry={"x": "0.85", "relative": "1"})
    ET.indent(mx) if hasattr(ET, "indent") else None
    return ET.ElementTree(mx)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()
    folder = pathlib.Path(args.folder).resolve()
    classes, relations = parse((folder / "03-class-diagram.md").read_text(encoding="utf-8"))
    source = mermaid_source(classes, relations)
    annex = folder / "annex"
    annex.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "annex.html"
        page.write_text(html_page(source, for_print=False), encoding="utf-8")
        dom = chrome(page, "--dump-dom")
        raw = re.search(r'<pre id="layout"[^>]*>(.*?)</pre>', dom, re.S)
        if not raw or not raw.group(1).strip():
            raise SystemExit("Chrome did not produce a layout")
        layout = json.loads(raw.group(1).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))
        tree = build_xml(classes, relations, layout)
        tree.write(annex / XML_NAME, encoding="utf-8", xml_declaration=True)
        page.write_text(html_page(source, for_print=True), encoding="utf-8")
        chrome(page, f"--print-to-pdf={annex / PDF_NAME}")
    print(f"{len(classes)} classes, {len(relations)} relations")
    print(f"Wrote {annex / XML_NAME}")
    print(f"Wrote {annex / PDF_NAME}")


if __name__ == "__main__":
    main()
