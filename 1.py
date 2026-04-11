import json
import time
from uuid import uuid4

NOW = int(time.time() * 1000)

def nid():
    return uuid4().hex[:20]

def rectangle(x, y, w, h, label, fill="#ffffff", font_size=18):
    rid = nid()
    tid = nid()
    r = {
        "id": rid,
        "type": "rectangle",
        "x": x, "y": y,
        "width": w, "height": h,
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": fill,
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 3},
        "seed": 1,
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": [],
        "updated": NOW,
        "link": None,
        "locked": False,
    }
    t = {
        "id": tid,
        "type": "text",
        "x": x + 12,
        "y": y + 12,
        "width": w - 24,
        "height": h - 24,
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 1,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": 1,
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": None,
        "updated": NOW,
        "link": None,
        "locked": False,
        "text": label,
        "fontSize": font_size,
        "fontFamily": 1,
        "textAlign": "left",
        "verticalAlign": "top",
        "baseline": font_size,
        "containerId": rid,
        "originalText": label,
        "lineHeight": 1.2,
    }
    return [r, t], rid

def arrow(x1, y1, x2, y2, label=None):
    aid = nid()
    a = {
        "id": aid,
        "type": "arrow",
        "x": x1,
        "y": y1,
        "width": x2 - x1,
        "height": y2 - y1,
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": 1,
        "version": 1,
        "versionNonce": 1,
        "isDeleted": False,
        "boundElements": [],
        "updated": NOW,
        "link": None,
        "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "lastCommittedPoint": [x2 - x1, y2 - y1],
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": "arrow",
    }
    els = [a]
    if label:
        tid = nid()
        tx = x1 + (x2 - x1) * 0.5 - 80
        ty = y1 + (y2 - y1) * 0.5 - 18
        els.append({
            "id": tid,
            "type": "text",
            "x": tx,
            "y": ty,
            "width": 160,
            "height": 24,
            "angle": 0,
            "strokeColor": "#1e1e1e",
            "backgroundColor": "#ffffff",
            "fillStyle": "solid",
            "strokeWidth": 1,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "roundness": None,
            "seed": 1,
            "version": 1,
            "versionNonce": 1,
            "isDeleted": False,
            "boundElements": None,
            "updated": NOW,
            "link": None,
            "locked": False,
            "text": label,
            "fontSize": 14,
            "fontFamily": 1,
            "textAlign": "center",
            "verticalAlign": "middle",
            "baseline": 12,
            "containerId": None,
            "originalText": label,
            "lineHeight": 1.2,
        })
    return els

def center_right_edge(x, y, w, h):
    return (x + w, y + h/2)

def center_left_edge(x, y, w, h):
    return (x, y + h/2)

def center_bottom_edge(x, y, w, h):
    return (x + w/2, y + h)

def center_top_edge(x, y, w, h):
    return (x + w/2, y)

def main():
    elements = []

    # Grid constants
    W = 320
    H = 110
    GAPY = 30

    # Columns
    x_user = 60
    x_app  = 430
    x_mod  = 800
    x_ext  = 1170

    # Rows (top aligned)
    y0 = 80

    # Boxes
    user, _ = rectangle(
        x_user, y0 + 1*(H+GAPY), W, H,
        "User / Browser\n• upload resume\n• paste JD\n• view results",
        fill="#f7f7ff"
    )
    elements += user

    flask, _ = rectangle(
        x_app, y0 + 1*(H+GAPY), W, H,
        "Flask App (app.py)\n• POST /analyze\n• /template\n• /export",
        fill="#fff7f0"
    )
    elements += flask

    uploads, _ = rectangle(
        x_app, y0 + 2*(H+GAPY), W, 90,
        "uploads/ (temp)\n• save file\n• delete after",
        fill="#f0fff7",
        font_size=18
    )
    elements += uploads

    validator, _ = rectangle(
        x_mod, y0 + 0*(H+GAPY), W, H,
        "validators.py\nvalidate_upload()\n• type + size",
        fill="#ffffff"
    )
    extractor, _ = rectangle(
        x_mod, y0 + 1*(H+GAPY), W, H,
        "extractor.py\n• extract text\n• Gemini JSON\n• feedback/skill gaps",
        fill="#ffffff"
    )
    matcher, _ = rectangle(
        x_mod, y0 + 2*(H+GAPY), W, H,
        "matcher.py\n• embeddings\n• cosine similarity\n= ATS %",
        fill="#ffffff"
    )
    grammar, _ = rectangle(
        x_mod, y0 + 3*(H+GAPY), W, H,
        "grammar_checker.py\n• TextBlob or fallback\n• quality scores",
        fill="#ffffff"
    )
    details, _ = rectangle(
        x_mod, y0 + 4*(H+GAPY), W, H,
        "analyzer_details.py\n• ATS compliance\n• keywords/action verbs\n• quant/length",
        fill="#ffffff"
    )
    export, _ = rectangle(
        x_mod, y0 + 5*(H+GAPY), W, H,
        "export.py\n• CSV/PDF/TXT\n• send_file()",
        fill="#ffffff"
    )
    elements += validator + extractor + matcher + grammar + details + export

    external, _ = rectangle(
        x_ext, y0 + 1*(H+GAPY), W + 40, 260,
        "External deps\n• Google Gemini API\n• SentenceTransformer\n• pdfplumber / python-docx\n• TextBlob + NLTK",
        fill="#f8f8f8"
    )
    elements += external

    # Arrows (simple left-to-right)
    ux, uy = center_right_edge(x_user, y0 + 1*(H+GAPY), W, H)
    fx, fy = center_left_edge(x_app, y0 + 1*(H+GAPY), W, H)
    elements += arrow(ux, uy, fx, fy, "POST /analyze")

    # Flask -> uploads (down)
    fbx, fby = center_bottom_edge(x_app, y0 + 1*(H+GAPY), W, H)
    utx, uty = center_top_edge(x_app, y0 + 2*(H+GAPY), W, 90)
    elements += arrow(fbx, fby, utx, uty, "save file")

    # Flask -> modules (fan-out vertically, all from Flask right edge)
    frx, fry = center_right_edge(x_app, y0 + 1*(H+GAPY), W, H)

    def mod_left(row):
        return center_left_edge(x_mod, y0 + row*(H+GAPY), W, H)

    elements += arrow(frx, fry, *mod_left(0), "validate")
    elements += arrow(frx, fry, *mod_left(1), "extract + LLM")
    elements += arrow(frx, fry, *mod_left(2), "ATS match")
    elements += arrow(frx, fry, *mod_left(3), "grammar")
    elements += arrow(frx, fry, *mod_left(4), "details")
    elements += arrow(frx, fry, *mod_left(5), "export")

    # Modules -> external deps (only key ones)
    ext_left_x, ext_left_y = center_left_edge(x_ext, y0 + 1*(H+GAPY), W + 40, 260)

    # extractor -> external
    exr, exy = center_right_edge(x_mod, y0 + 1*(H+GAPY), W, H)
    elements += arrow(exr, exy, ext_left_x, ext_left_y + 40, "Gemini")

    # matcher -> external
    mx, my = center_right_edge(x_mod, y0 + 2*(H+GAPY), W, H)
    elements += arrow(mx, my, ext_left_x, ext_left_y + 90, "model")

    # grammar -> external
    gx, gy = center_right_edge(x_mod, y0 + 3*(H+GAPY), W, H)
    elements += arrow(gx, gy, ext_left_x, ext_left_y + 140, "TextBlob")

    # details -> external (keywords Gemini)
    dx, dy = center_right_edge(x_mod, y0 + 4*(H+GAPY), W, H)
    elements += arrow(dx, dy, ext_left_x, ext_left_y + 190, "keywords")

    out = {
        "type": "excalidraw",
        "version": 2,
        "source": "generate_excalidraw_architecture_v2.py",
        "elements": elements,
        "appState": {
            "viewBackgroundColor": "#ffffff",
            "gridSize": None,
            "zoom": {"value": 1.0},
        },
        "files": {}
    }

    filename = "ai_resume_analyzer_architecture.excalidraw"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("Wrote:", filename)
    print("Open in Excalidraw: https://excalidraw.com (Open -> select file)")

if __name__ == "__main__":
    main()