"""
Lager omdirigeringssiden for de gamle domenene (follobjorkeved.no) i public-omdirigering/.

GitHub Pages kan ikke sende ekte 301-svar, så hver gammel adresse får en liten side med
<link rel="canonical"> og <meta http-equiv="refresh" content="0">. Google behandler det som en
permanent flytting. Adresser som ikke finnes (bilder, CSV, widgeter på andre nettsider osv.)
fanges av 404.html, som sender videre med JavaScript til samme adresse på folloes.no.

    python3 build.py               # først, så listen over sider er oppdatert
    python3 lag-omdirigering.py    # lager public-omdirigering/

Innholdet i public-omdirigering/ legges på gh-pages i repoet ved-folle-eiendom på lanseringsdagen
(se LANSERING.md).
"""
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
OUT = ROOT / "public-omdirigering"
NY = "https://folloes.no"
GAMMELT_DOMENE = "follobjorkeved.no"

# Spesielle adresser. Alt annet sendes til samme adresse på folloes.no.
SPESIELLE = {
    "/": "/salg-av-bjorkeved/",
    "/personvern/": "/personvernerklaering/",
}


def side(til):
    url = html.escape(NY + til, quote=True)
    return (f'<!doctype html><html lang="nb"><head><meta charset="utf-8"><title>Flyttet til folloes.no</title>'
            f'<meta name="robots" content="noindex"><link rel="canonical" href="{url}">'
            f'<meta http-equiv="refresh" content="0; url={url}">'
            f'<script>location.replace("{url}"+location.search+location.hash)</script></head>'
            f'<body><p>Follo Bjørkeved har flyttet til <a href="{url}">{url}</a>.</p></body></html>')


def main():
    if not PUBLIC.exists():
        raise SystemExit("Kjør python3 build.py først.")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    stier = set()
    for p in PUBLIC.rglob("index.html"):
        rel = p.parent.relative_to(PUBLIC).as_posix()
        stier.add("/" if rel == "." else f"/{rel}/")
    n = 0
    for sti in sorted(stier | set(SPESIELLE)):
        til = SPESIELLE.get(sti, sti)
        mappe = OUT / sti.strip("/")
        mappe.mkdir(parents=True, exist_ok=True)
        (mappe / "index.html").write_text(side(til), encoding="utf-8")
        n += 1
    # Alt annet: samme adresse på folloes.no.
    (OUT / "404.html").write_text(
        '<!doctype html><html lang="nb"><head><meta charset="utf-8"><title>Flyttet til folloes.no</title>'
        '<meta name="robots" content="noindex">'
        f'<script>location.replace("{NY}"+location.pathname+location.search+location.hash)</script></head>'
        f'<body><p>Follo Bjørkeved har flyttet til <a href="{NY}/salg-av-bjorkeved/">{NY}/salg-av-bjorkeved/</a>.</p></body></html>',
        encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    (OUT / "CNAME").write_text(GAMMELT_DOMENE + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    # IndexNow-nøkkelen, så Bing kan få beskjed om at sidene har flyttet.
    for f in PUBLIC.glob("*.txt"):
        if len(f.stem) == 32:
            shutil.copy(f, OUT / f.name)
    print(f"Laget {n} omdirigeringer til {OUT}/")


if __name__ == "__main__":
    main()
