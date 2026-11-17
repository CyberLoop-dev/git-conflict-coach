from html import escape
from pathlib import Path

SKIP={".git","node_modules",".venv","venv","dist","build","__pycache__"}

def parse_conflicts(text,path="<text>"):
    lines=text.splitlines()
    results=[]; start=None; separator=None
    for index,line in enumerate(lines,1):
        if line.startswith("<<<<<<<"):
            start=index; separator=None
        elif start is not None and line.startswith("======="):
            separator=index
        elif start is not None and line.startswith(">>>>>>>"):
            results.append({"file":str(path),"start_line":start,"end_line":index,
                            "kind":"unresolved conflict block",
                            "ours":lines[start:separator-1] if separator else [],
                            "theirs":lines[separator:index-1] if separator else []})
            start=None; separator=None
    if start is not None:
        results.append({"file":str(path),"start_line":start,"end_line":len(lines),
                        "kind":"incomplete conflict block","ours":[],"theirs":[]})
    return results

def scan_paths(paths):
    findings=[]
    for item in paths:
        candidates=[item] if item.is_file() else (p for p in item.rglob("*") if p.is_file() and not any(part in SKIP for part in p.parts))
        for path in candidates:
            try: text=path.read_text(encoding="utf-8")
            except (OSError,UnicodeError): continue
            findings.extend(parse_conflicts(text,path))
    return findings

def render_html(findings):
    cards=[]
    for item in findings:
        cards.append("<article><h2>"+escape(item["file"])+"</h2><p>Lines "+str(item["start_line"])+"–"+str(item["end_line"])+" · "+escape(item["kind"])+"</p></article>")
    body="".join(cards) or "<p>No conflict markers found.</p>"
    return "<!doctype html><meta charset='utf-8'><title>Conflict report</title><style>body{font:16px system-ui;background:#101827;color:#e5edf5;max-width:850px;margin:4rem auto;padding:1rem}article{background:#1d2b3d;border:1px solid #34465d;border-radius:12px;padding:1rem;margin:1rem 0}h2{font-size:1.1rem;color:#fbbf24}</style><h1>Git Conflict Coach</h1>"+body
