#!/usr/bin/env python3
"""
Sjekker den bygde siden i public/: døde interne lenker, manglende bilder og filer,
lenker til ankre som ikke finnes, og at hver side har én <h1>, <title> og description.

    python3 build.py && python3 sjekk.py

Exit-kode 0 = alt i orden, 1 = feil (listet ut).
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

OUT = Path(__file__).parent / "public"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.h1, self.title, self.desc = [], set(), 0, False, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.title = True
        if tag == "meta" and a.get("name") == "description" and (a.get("content") or "").strip():
            self.desc = True
        for k in ("href", "src"):
            if a.get(k):
                self.links.append(a[k])
        for k in ("srcset", "imagesrcset"):
            if a.get(k):
                self.links += [x.strip().split(" ")[0] for x in a[k].split(",")]


def target(path):
    p = OUT / unquote(path).lstrip("/")
    if p.is_dir():
        p = p / "index.html"
    return p


def main():
    pages = {}
    for f in OUT.rglob("*.html"):
        pg = Page()
        pg.feed(f.read_text(encoding="utf-8"))
        rel = "/" + str(f.relative_to(OUT)).replace("index.html", "")
        pages[rel] = pg
    errors = []
    for rel, pg in sorted(pages.items()):
        is_tool = rel.startswith(("/widget/", "/admin/")) or "refresh" in (OUT / rel.lstrip("/")).as_posix()
        if not rel.startswith("/widget/") and not rel.startswith("/personvern/"):
            if pg.h1 != 1 and not rel.startswith("/admin/"):
                errors.append(f"{rel}: {pg.h1} stk <h1>")
            if not pg.title:
                errors.append(f"{rel}: mangler <title>")
            if not pg.desc and not is_tool:
                errors.append(f"{rel}: mangler description")
        for link in pg.links:
            u = urlsplit(link)
            if u.scheme or link.startswith(("//", "mailto:", "tel:", "data:", "javascript:")):
                continue
            path = u.path or rel
            if not path.startswith("/"):
                continue
            t = target(path)
            if not t.exists():
                errors.append(f"{rel}: død lenke {link}")
                continue
            if u.fragment and t.suffix == ".html":
                key = "/" + str(t.relative_to(OUT)).replace("index.html", "")
                ids = pages[key].ids if key in pages else set()
                if u.fragment not in ids:
                    errors.append(f"{rel}: ankeret #{u.fragment} finnes ikke på {key}")
    for e in errors:
        print(e)
    print(f"{len(pages)} sider sjekket, {len(errors)} feil")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
