#!/usr/bin/env bash
# Henter endringene som er gjort i follobjorkeved.no (repoet ved-folle-eiendom) siden sist,
# og fletter dem inn her. Kjøres rett før lanseringen, så ingenting fra vedsiden går tapt.
# README.md og ANALYSE.md tas ikke med (de er forskjellige i de to repoene).
#
#   ./hent-ved.sh
#
# Commiten det sist ble hentet fra står i .ved-synk. Ved konflikter: rett filene, kjør
# «git add», og oppdater .ved-synk med commiten skriptet skriver ut.
set -euo pipefail
cd "$(dirname "$0")"

VED="https://github.com/andersmathisen7-design/ved-folle-eiendom.git"
FRA=$(cat .ved-synk)
git fetch -q "$VED" main
TIL=$(git rev-parse FETCH_HEAD)

if [ "$FRA" = "$TIL" ]; then
  echo "Ingen nye endringer i ved-folle-eiendom (står på ${TIL:0:7})."
  exit 0
fi

echo "Nye endringer i ved-folle-eiendom:"
git log --oneline "$FRA..$TIL"
if git diff "$FRA" "$TIL" -- . ':!README.md' ':!ANALYSE.md' ':!.github/**' | git apply -3 --allow-empty; then
  echo "$TIL" > .ved-synk
  python3 build.py >/dev/null && python3 sjekk.py | tail -1
  echo "Ferdig. Se over endringene med «git status», og commit dem."
else
  echo "Konflikter. Rett filene, kjør «git add», og skriv $TIL i .ved-synk." >&2
  exit 1
fi
