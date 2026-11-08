# Tester

Kjøres lokalt på PC-en, aldri i GitHub Actions.

```bash
python3 build.py                      # tests/bestilling.test.js tester det ferdige nettstedet i public/
node tests/kalender.test.js           # e-posten det gamle kalenderskriptet lager (Node, uten Google; nettsiden bruker det ikke lenger)
node tests/bestilling.test.js         # vedbestillingen, kontaktskjemaet og garasjevask i Chromium, med appen og GoatCounter mocket
```

`bestilling.test.js` trenger Playwright. Installer den utenfor repoet og pek NODE_PATH dit, f.eks.:

```bash
mkdir -p ~/pwtest && cd ~/pwtest && npm init -y && npm i playwright && npx playwright install chromium
cd - && NODE_PATH=~/pwtest/node_modules node tests/bestilling.test.js
```

Ingen ekte bestilling eller henvendelse sendes: alle kall til appen Nettsideferdig (`folloes.app.nettsideferdig.no`) fanges opp i testen,
og testen feiler hvis skjemaet kontakter FormSubmit eller Google.
