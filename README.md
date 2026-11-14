# Follo Eiendomsservice AS – ny nettside (folloes.no)

Ny, rask og statisk versjon av **folloes.no** (i dag WordPress med Elementor), med bjørkeved-siden fra **follobjorkeved.no** flettet inn. Hele nettstedet har samme stil som folloes.no: svart, grått og grønt (`#63C302`), Oswald i overskrifter og Nunito i brødtekst. Skriftene ligger på egen server.

## Innhold

| Side | Hva |
|---|---|
| `/` | Forsiden for firmaet: tjenester, årstider, referanser, bjørkeved og kontaktskjema |
| `/tjenester/` og `/vaktmestertjenester/`, `/vintertjenester/`, `/feiing-og-spyling/`, `/gartner-og-grontareal/`, `/renhold/`, `/hms-brannsikring-kontroll-av-lekeplasser/`, `/matteutleie/`, `/trefelling/` | Tjenestesidene, samme adresser som på dagens folloes.no |
| `/garasjevask/` | Egen del av nettstedet, som bjørkeved (eget menypunkt, egen underlinje og egen blokk på forsiden, ikke blant tjenestene). Kopiert fra garasjevasken.no: priser per parkeringsplass, priskalkulator, risiko og forberedelser. Kalkulatoren fyller ut kontaktskjemaet. Teksten står i `GARASJEVASK_SIDE` og prisene i `GARASJEVASK` i `firma_innhold.py` |
| `/om-oss/`, `/referanser/`, `/kontakt-oss/`, `/personvernerklaering/`, `/takk-for-din-henvendelse/` | Som på folloes.no. Personvernerklæringen dekker nå både kontaktskjemaet og vedbestillinger |
| `/salg-av-bjorkeved/` | Forsiden for bjørkeved (var forsiden på follobjorkeved.no). Erstatter den gamle siden med samme adresse på folloes.no |
| `/ved-as/` … `/ved-enebakk/`, `/vedabonnement/`, `/artikler/`, `/vedpris/`, `/fyre-i-dag/`, `/verktoy/`, `/data/`, `/presse/`, `/takk/` | Resten av bjørkeved-sidene, uendret adresse fra follobjorkeved.no |
| `/admin/` | Sender videre til eiersiden i appen: https://folloes.app.nettsideferdig.no/admin/ |

Tekst og bilder til firmasidene ligger i `firma_innhold.py` (hentet fra folloes.no i oktober 2026, med skrivefeil rettet). Sidene lages i `firma_build.py`. Bjørkeved-sidene lages som før i `build.py`, og toppen, menyen og bunnen er felles for alle sider (`head()` og `footer()` i `build.py`).

## Bygg og sjekk

```bash
python3 build.py     # lager nettsiden i public/
python3 sjekk.py     # døde lenker, manglende bilder og ankre, én <h1> per side (exit 1 ved feil)
cd public && python3 -m http.server 8000   # se siden på http://localhost:8000
```

## Testside

`./publiser-test.sh` bygger en testversjon og legger den på `gh-pages`-grenen: **https://andersmathisen7-design.github.io/folloes-nettside/**.
Testversjonen har en gul stripe øverst og blir ikke indeksert av Google. Skjemaene går til samme app som den ekte siden (se under), som er i testmodus til prislisten er bekreftet. Det brukes ikke GitHub Actions.

## Endringer fra folloes.no (UX)

- Overskriften på forsiden sier hva firmaet gjør, ikke bare navnet. Knappene «Få et uforpliktende tilbud» og «Ring» står øverst.
- Hele tjenestekortet er klikkbart, og bildene vises (på folloes.no var de ofte tomme på grunn av lat lasting).
- Kontaktskjemaet står nederst på alle firmasider, med tjenesten valgt på forhånd. Telefon *eller* e-post holder. Svar går til takkesiden.
- Mobil: egen meny, «Få et tilbud»-knapp nederst på skjermen, telefonnummer som kan trykkes.
- Ingen cookie-vegg: siden setter ingen cookies, og skriftene hentes ikke fra Google.
- Bedre kontrast: knappene har mørk tekst på grønt (hvit tekst på `#63C302` var vanskelig å lese), og brødteksten er mørkere grå.
- Den gamle siden «Salg av bjørkeved» viste vintertjenester under «Vi kan hjelpe deg med», og trefelling-siden viste feieoppgaver. Det er rettet.
- Bildene er WebP i to størrelser. Kortbildene er 12–170 kB, mot opptil 1 MB PNG før.

## Lansering

Se **[LANSERING.md](LANSERING.md)**: hva som er gjort, hva som skjer på lanseringsdagen og i hvilken rekkefølge, og DNS-oppsettet hos Domeneshop.

- `.github/workflows/pages.yml` publiserer folloes.no (foreløpig bare med knapp i Actions).
- `./hent-ved.sh` henter nye endringer fra follobjorkeved.no (repoet ved-folle-eiendom). Sist hentet: `.ved-synk`.
- `python3 lag-omdirigering.py` lager omdirigeringssiden for follobjorkeved.no i `public-omdirigering/`.
- **Skjemaene går til appen Nettsideferdig** (`APP_URL` i `config.py`, https://folloes.app.nettsideferdig.no), ikke til FormSubmit eller Google-regnearket:
  - Vedbestillingen (`src/assets/app.js`): dagene og «Fullt»/«Ledig» fra `GET /api/leveringsdager` når adressen er skrevet, bestillingen til `POST /api/bestill-levering` (ingen beløp; appen regner prisen og sender kunden bekreftelse på e-post). Varen heter «Bjørkeved 40 L» i appen, og bæringen er tillegg med samme navn som i `CARRY_OPTIONS`.
  - Kontaktskjemaet og garasjevask-kalkulatoren: `POST /api/henvendelse`.
  - Eiersiden (bestillinger, fulle dager, henvendelser) er appens admin. `/admin/` på nettstedet sender dit.
  - `APP_URL=http://127.0.0.1:8790 python3 build.py` bygger mot en lokal (falsk) app.
- `kalender/` (Google-regnearket) brukes ikke lenger av nettsiden. Bestillinger og henvendelser går til appen Nettsideferdig (`APP_URL`).
- Tester: se `tests/README.md` og `cd server && npm test`.
