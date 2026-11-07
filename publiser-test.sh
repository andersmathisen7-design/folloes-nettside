#!/usr/bin/env bash
# Bygger testversjonen og legger den på gh-pages-grenen (GitHub Pages).
# Testversjonen blir ikke indeksert, bruker ikke den ekte leveringskalenderen,
# og skjemaene går bare til ORDER_EMAIL. Ingen GitHub Actions: alt kjøres lokalt.
#
#   ./publiser-test.sh
set -euo pipefail
cd "$(dirname "$0")"

REPO="folloes-nettside"
OWNER="andersmathisen7-design"

# Etter lanseringen ligger den ekte folloes.no på gh-pages. Da skal testsiden aldri overskrive den.
if git ls-remote --exit-code "$(git remote get-url origin)" gh-pages >/dev/null 2>&1; then
  git fetch -q origin gh-pages
  if git cat-file -e FETCH_HEAD:CNAME 2>/dev/null; then
    echo "Stopp: gh-pages har eget domene ($(git show FETCH_HEAD:CNAME)), altså den ekte siden. Testsiden publiseres ikke." >&2
    exit 1
  fi
fi

python3 build.py >/dev/null
python3 sjekk.py | tail -1

SITE_URL="https://$OWNER.github.io/$REPO" BASE_PATH="/$REPO" TESTSIDE=1 python3 build.py

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp -r public/. "$TMP/"
touch "$TMP/.nojekyll"
git -C "$TMP" init -q -b gh-pages
git -C "$TMP" add -A
git -C "$TMP" -c user.email="$(git config user.email || echo amkleven@gmail.com)" -c user.name="$(git config user.name || echo 'Anders Mathiesen')" \
  commit -q -m "Testside bygget fra $(git rev-parse --short HEAD)"
git -C "$TMP" push -q -f "$(git remote get-url origin)" gh-pages

# Bygg vanlig versjon igjen, så public/ ikke ligger igjen som testversjon.
python3 build.py >/dev/null
echo "Publisert: https://$OWNER.github.io/$REPO/"
