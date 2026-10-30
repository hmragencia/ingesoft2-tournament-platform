#!/usr/bin/env python3
"""Build BPMN 2.0 files (with diagram layout) from small JSON specs and render them to SVG.

Each spec in <folder>/*.json describes pools, lanes, nodes on a column grid, sequence flows
and message flows. The script writes <name>.bpmn (opens in bpmn.io or Camunda Modeler) and
<name>.svg, rendered with bpmn-js in headless Chrome.

Usage: python3 tools/build_bpmn.py Workshop-2/bpmn
"""
import base64
import html
import json
import pathlib
import re
import subprocess
import sys
from xml.sax.saxutils import quoteattr

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BPMN_JS = "https://unpkg.com/bpmn-js@17.11.1/dist/bpmn-viewer.production.min.js"

POOL_LABEL = 30          # band with the pool name
LANE_LABEL = 30          # band with the lane name
X0 = POOL_LABEL + LANE_LABEL + 10
COL_W = 145
POOL_GAP = 40
COLLAPSED_H = 60
SIZES = {"task": (120, 80), "event": (36, 36), "gateway": (50, 50)}

TAGS = {
    "startEvent": "startEvent", "endEvent": "endEvent", "catchEvent": "intermediateCatchEvent",
    "boundaryEvent": "boundaryEvent", "gateway": "exclusiveGateway",
    "userTask": "userTask", "serviceTask": "serviceTask", "sendTask": "sendTask", "task": "task",
}


def kind(node):
    t = node["type"]
    if t.endswith("Task") or t == "task":
        return "task"
    if t == "gateway":
        return "gateway"
    return "event"


def layout(spec):
    ncols = 1 + max(n.get("col", 0) for n in spec["nodes"])
    width = X0 + ncols * COL_W + 20
    y = 0
    pools, lanes = {}, {}
    for pool in spec["pools"]:
        if pool.get("collapsed"):
            pools[pool["id"]] = (0, y, width, COLLAPSED_H)
            y += COLLAPSED_H + POOL_GAP
            continue
        top = y
        for lane in pool["lanes"]:
            h = lane.get("height", 120)
            lanes[lane["id"]] = (POOL_LABEL, y, width - POOL_LABEL, h, pool["id"])
            y += h
        pools[pool["id"]] = (0, top, width, y - top)
        y += POOL_GAP
    bounds = {}
    for n in spec["nodes"]:
        if n["type"] == "boundaryEvent":
            continue
        _, ly, _, lh, _ = lanes[n["lane"]]
        w, h = SIZES[kind(n)]
        cx = X0 + n["col"] * COL_W + COL_W / 2
        cy = ly + lh / 2 + n.get("dy", 0)
        bounds[n["id"]] = (cx - w / 2, cy - h / 2, w, h)
    for n in spec["nodes"]:
        if n["type"] == "boundaryEvent":
            tx, ty, tw, th = bounds[n["attachedTo"]]
            bounds[n["id"]] = (tx + 12, ty + th - 18, 36, 36)
    return pools, lanes, bounds


def center(b):
    x, y, w, h = b
    return x + w / 2, y + h / 2


def seq_waypoints(src, tgt, bounds):
    s, t = bounds[src["id"]], bounds[tgt["id"]]
    (scx, scy), (tcx, tcy) = center(s), center(t)
    s_right, t_left = s[0] + s[2], t[0]
    if src["type"] == "boundaryEvent":
        return [(scx, s[1] + s[3]), (scx, tcy), (t_left, tcy)]
    if abs(scy - tcy) < 1:
        return [(s_right, scy), (t_left, tcy)]
    if abs(scx - tcx) < 1:
        return [(scx, s[1] + s[3]), (tcx, t[1])] if tcy > scy else [(scx, s[1]), (tcx, t[1] + t[3])]
    if src["type"] == "gateway":
        sy = s[1] + s[3] if tcy > scy else s[1]
        return [(scx, sy), (scx, tcy), (t_left, tcy)]
    if tgt["type"] == "gateway":
        ty = t[1] if tcy > scy else t[1] + t[3]
        return [(s_right, scy), (tcx, scy), (tcx, ty)]
    xm = (s_right + t_left) / 2
    return [(s_right, scy), (xm, scy), (xm, tcy), (t_left, tcy)]


def msg_waypoints(m, pools, bounds, col_x):
    def ref(r):
        if r.startswith("pool:"):
            return "pool", pools[r[5:]]
        return "node", bounds[r]
    (sk, sb), (tk, tb) = ref(m["from"]), ref(m["to"])
    sx = center(sb)[0] if sk == "node" else (center(tb)[0] if tk == "node" else col_x(m["col"]))
    tx = center(tb)[0] if tk == "node" else sx
    down = center(tb)[1] > center(sb)[1]
    sy = sb[1] + sb[3] if down else sb[1]
    ty = tb[1] if down else tb[1] + tb[3]
    if abs(sx - tx) < 1:
        return [(sx, sy), (tx, ty)]
    target_pool = next(p for p in pools.values() if p[1] <= center(tb)[1] <= p[1] + p[3])
    ym = target_pool[1] - POOL_GAP / 2 if down else target_pool[1] + target_pool[3] + POOL_GAP / 2
    return [(sx, sy), (sx, ym), (tx, ym), (tx, ty)]


def event_definition(n):
    ev = n.get("event")
    return {"message": "<bpmn:messageEventDefinition/>", "timer": "<bpmn:timerEventDefinition/>"}.get(ev, "")


def to_xml(spec):
    pid = spec["id"]
    pools, lanes, bounds = layout(spec)
    nodes = {n["id"]: n for n in spec["nodes"]}
    lane_pool = {l: v[4] for l, v in lanes.items()}

    def pool_of(nid):
        n = nodes[nid]
        if n["type"] == "boundaryEvent":
            return pool_of(n["attachedTo"])
        return lane_pool[n["lane"]]

    def col_x(col):
        return X0 + col * COL_W + COL_W / 2

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
           'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
           'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" '
           'xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
           f'id="Definitions_{pid}" targetNamespace="https://github.com/hmragencia/ingesoft2-tournament-platform">',
           f'  <bpmn:collaboration id="Collaboration_{pid}">']
    for pool in spec["pools"]:
        proc = "" if pool.get("collapsed") else f' processRef="Process_{pid}_{pool["id"]}"'
        out.append(f'    <bpmn:participant id="Pool_{pid}_{pool["id"]}" name={quoteattr(pool["name"])}{proc}/>')
    for i, m in enumerate(spec.get("messages", [])):
        def mref(r):
            return f"Pool_{pid}_{r[5:]}" if r.startswith("pool:") else f"{pid}_{r}"
        out.append(f'    <bpmn:messageFlow id="Msg_{pid}_{i}" name={quoteattr(m.get("name", ""))} '
                   f'sourceRef="{mref(m["from"])}" targetRef="{mref(m["to"])}"/>')
    out.append('  </bpmn:collaboration>')

    for pool in spec["pools"]:
        if pool.get("collapsed"):
            continue
        out.append(f'  <bpmn:process id="Process_{pid}_{pool["id"]}" isExecutable="false">')
        out.append(f'    <bpmn:laneSet id="LaneSet_{pid}_{pool["id"]}">')
        for lane in pool["lanes"]:
            out.append(f'      <bpmn:lane id="Lane_{pid}_{lane["id"]}" name={quoteattr(lane["name"])}>')
            for n in spec["nodes"]:
                if n.get("lane") == lane["id"] or (n["type"] == "boundaryEvent" and nodes[n["attachedTo"]]["lane"] == lane["id"]):
                    out.append(f'        <bpmn:flowNodeRef>{pid}_{n["id"]}</bpmn:flowNodeRef>')
            out.append('      </bpmn:lane>')
        out.append('    </bpmn:laneSet>')
        for n in spec["nodes"]:
            if pool_of(n["id"]) != pool["id"]:
                continue
            tag = TAGS[n["type"]]
            extra = f' attachedToRef="{pid}_{n["attachedTo"]}"' if n["type"] == "boundaryEvent" else ""
            body = event_definition(n)
            out.append(f'    <bpmn:{tag} id="{pid}_{n["id"]}" name={quoteattr(n["name"])}{extra}>{body}</bpmn:{tag}>')
        for i, f in enumerate(spec["flows"]):
            if pool_of(f[0]) != pool["id"]:
                continue
            name = f' name={quoteattr(f[2])}' if len(f) > 2 else ""
            out.append(f'    <bpmn:sequenceFlow id="Flow_{pid}_{i}"{name} sourceRef="{pid}_{f[0]}" targetRef="{pid}_{f[1]}"/>')
        out.append('  </bpmn:process>')

    out.append(f'  <bpmndi:BPMNDiagram id="Diagram_{pid}">')
    out.append(f'    <bpmndi:BPMNPlane id="Plane_{pid}" bpmnElement="Collaboration_{pid}">')

    def label(lb):
        if not lb:
            return ""
        x, y, w, h = lb
        return f'<bpmndi:BPMNLabel><dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}"/></bpmndi:BPMNLabel>'

    def shape(eid, b, extra="", lb=None):
        x, y, w, h = b
        return (f'      <bpmndi:BPMNShape id="{eid}_di" bpmnElement="{eid}"{extra}>'
                f'<dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}"/>{label(lb)}</bpmndi:BPMNShape>')

    def edge(eid, pts, lb=None):
        wps = "".join(f'<di:waypoint x="{x:.0f}" y="{y:.0f}"/>' for x, y in pts)
        return f'      <bpmndi:BPMNEdge id="{eid}_di" bpmnElement="{eid}">{wps}{label(lb)}</bpmndi:BPMNEdge>'

    def node_label(n):
        x, y, w, h = bounds[n["id"]]
        pos = n.get("labelPos")
        if pos == "above":
            return (x + w / 2 - 60, y - 32, 120, 28)
        if pos == "aboveleft":
            return (x - 88, y - 26, 84, 28)
        if pos == "left":
            return (x - 92, y + 2, 88, 30)
        return None

    def msg_label(pts):
        if len(pts) == 2:
            (x1, y1), (_, y2) = pts
            return (x1 + 6, (y1 + y2) / 2 - 10, 110, 20)
        (_, _), (x1, ym), (x2, _), _ = pts
        return ((x1 + x2) / 2 - 50, ym - 18, 100, 14)

    for pool in spec["pools"]:
        out.append(shape(f'Pool_{pid}_{pool["id"]}', pools[pool["id"]], ' isHorizontal="true"'))
        for lane in pool.get("lanes", []):
            x, y, w, h, _ = lanes[lane["id"]]
            out.append(shape(f'Lane_{pid}_{lane["id"]}', (x, y, w, h), ' isHorizontal="true"'))
    for n in spec["nodes"]:
        extra = ' isMarkerVisible="true"' if n["type"] == "gateway" else ""
        out.append(shape(f'{pid}_{n["id"]}', bounds[n["id"]], extra, node_label(n)))
    for i, f in enumerate(spec["flows"]):
        out.append(edge(f'Flow_{pid}_{i}', seq_waypoints(nodes[f[0]], nodes[f[1]], bounds)))
    for i, m in enumerate(spec.get("messages", [])):
        pts = msg_waypoints(m, pools, bounds, col_x)
        out.append(edge(f'Msg_{pid}_{i}', pts, msg_label(pts)))
    out += ['    </bpmndi:BPMNPlane>', '  </bpmndi:BPMNDiagram>', '</bpmn:definitions>', '']
    return "\n".join(out)


RENDER_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script src="{bpmn_js}"></script></head><body><div id="canvas" style="width:2400px;height:1400px"></div>
<pre id="out"></pre><script>
const diagrams = {diagrams};
(async () => {{
  const results = [];
  for (const xml of diagrams) {{
    const viewer = new BpmnJS({{ container: '#canvas' }});
    try {{
      await viewer.importXML(xml);
      const {{ svg }} = await viewer.saveSVG();
      results.push(btoa(unescape(encodeURIComponent(svg))));
    }} catch (e) {{ results.push('ERROR:' + e.message); }}
    viewer.destroy();
  }}
  document.getElementById('out').textContent = 'BEGIN' + results.join('|') + 'END';
}})();
</script></body></html>"""


def render(xmls, workdir):
    page = workdir / ".render-bpmn.html"
    page.write_text(RENDER_PAGE.format(bpmn_js=BPMN_JS, diagrams=json.dumps(xmls)), encoding="utf-8")
    dom = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=20000",
         "--dump-dom", page.as_uri()],
        check=True, capture_output=True, text=True,
    ).stdout
    page.unlink()
    match = re.search(r"BEGIN(.*?)END", html.unescape(dom), re.S)
    if not match:
        sys.exit("bpmn-js did not finish rendering")
    out = []
    for item in match.group(1).split("|"):
        if item.startswith("ERROR:"):
            sys.exit(f"bpmn-js import failed: {item}")
        out.append(base64.b64decode(item).decode("utf-8"))
    return out


def main():
    folder = pathlib.Path(sys.argv[1]).resolve()
    specs = sorted(folder.glob("*.json"))
    xmls = []
    for path in specs:
        xml = to_xml(json.loads(path.read_text(encoding="utf-8")))
        path.with_suffix(".bpmn").write_text(xml, encoding="utf-8")
        xmls.append(xml)
    for path, svg in zip(specs, render(xmls, folder)):
        path.with_suffix(".svg").write_text(svg, encoding="utf-8")
        print(f"Wrote {path.with_suffix('.bpmn').name} and {path.with_suffix('.svg').name}")


if __name__ == "__main__":
    main()
