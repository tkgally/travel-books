#!/usr/bin/env python3
"""Publish a finished book: wip/<slug>/ -> books/<slug>/, after preflight says PASS.

  publish.py SLUG [--epubcheck JAR]

Runs tools/preflight.py on wip/<slug> (or on books/<slug> for a new version of a published book) and stops
unless it ends PASS. Then, for a first publication, moves book.json, source.json, log.md, pages/ and images/
to books/<slug>/ (model runs and everything else in wip/<slug>/ stay in git history only), writes the
preflight report to books/<slug>/preflight.txt, and sets the book's row in data/queue.json to "published".
The site is rebuilt and deployed by GitHub Actions when the change reaches main.
"""
import argparse, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import preflight  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--epubcheck")
    a = ap.parse_args()
    wip, pub = os.path.join(REPO, "wip", a.slug), os.path.join(REPO, "books", a.slug)
    src = wip if os.path.isdir(wip) else pub
    if not os.path.isdir(src):
        sys.exit(f"no wip/{a.slug} or books/{a.slug}")
    if src == wip and os.path.isdir(pub):
        sys.exit(f"books/{a.slug} already exists: new versions are made by editing books/{a.slug} directly")
    verdict, report, _ = preflight.run(src, a.epubcheck)
    print(report)
    if verdict != "PASS":
        sys.exit("not published: preflight did not PASS")
    if src == wip:
        os.makedirs(pub)
        for name in ("book.json", "source.json", "log.md", "pages", "images"):
            if os.path.exists(os.path.join(wip, name)):
                shutil.move(os.path.join(wip, name), os.path.join(pub, name))
        shutil.rmtree(wip)
    open(os.path.join(pub, "preflight.txt"), "w", encoding="utf-8").write(report + "\n")
    cfg = json.load(open(os.path.join(pub, "book.json"), encoding="utf-8"))
    qf = os.path.join(REPO, "data", "queue.json")
    q = json.load(open(qf, encoding="utf-8"))
    for b in q["books"]:
        if b.get("slug") == a.slug:
            b["status"] = "published"
            b["version"] = cfg["version"]
            b["published"] = cfg["date"]
    json.dump(q, open(qf, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(qf, "a").write("\n")
    print(f"published books/{a.slug} v{cfg['version']}: commit, push, PR, merge; then check the live page")


if __name__ == "__main__":
    main()
