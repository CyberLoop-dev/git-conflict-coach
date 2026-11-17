import argparse
from pathlib import Path
from conflict_coach import scan_paths, render_html

def main():
    parser=argparse.ArgumentParser(description="Find unresolved Git conflict markers without editing files.")
    parser.add_argument("paths",nargs="+",type=Path)
    parser.add_argument("--html",type=Path,help="Write a self-contained HTML report.")
    args=parser.parse_args()
    findings=scan_paths(args.paths)
    for item in findings:
        print(f"{item['file']}:{item['start_line']}-{item['end_line']}: {item['kind']}")
    print(f"{len(findings)} conflict block(s) found.")
    if args.html:
        args.html.write_text(render_html(findings),encoding="utf-8")
        print(f"Report written to {args.html}")
    return 1 if findings else 0

if __name__=="__main__": raise SystemExit(main())
