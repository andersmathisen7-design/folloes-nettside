# Follo Eiendomsservice AS – ny nettside (folloes.no)

Ny, rask og statisk versjon av **folloes.no** (i dag WordPress med Elementor), med bjørkeved-siden fra **follobjorkeved.no** flettet inn. Hele nettstedet har samme stil som folloes.no: svart, grått og grønt (`#63C302`), Oswald i overskrifter og Nunito i brødtekst. Skriftene ligger på egen server.

## Innhold

| Side | Hva |
|---|---|
| `/` | Forsiden for firmaet: tjenester, årstider, referanser, bjørkeved og kontaktskjema |
| `/tjenester/` og `/vaktmestertjenester/`, `/vintertjenester/`, `/feiing-og-spyling/`, `/gartner-og-grontareal/`, `/renhold/`, `/hms-brannsikring-kontroll-av-lekeplasser/`, `/matteutleie/`, `/trefelling/` | Tjenestesidene, samme adresser som på dagens folloes.no |
| `/om-oss/`, `/referanser/`, `/kontakt-oss/`, `/personvernerklaering/`, `/takk-for-din-henvendelse/` | Som på folloes.no. Personvernerklæringen dekker nå både kontaktskjemaet og vedbestillinger |
| `/salg-av-bjorkeved/` | Forsiden for bjørkeved (var forsiden på follobjorkeved.no). Erstatter den gamle siden med samme adresse på folloes.no |
| `/ved-as/` … `/ved-enebakk/`, `/vedabonnement/`, `/artikler/`, `/vedpris/`, `/fyre-i-dag/`, `/verktoy/`, `/data/`, `/presse/`, `/admin/`, `/takk/` | Resten av bjørkeved-sidene, uendret adresse fra follobjorkeved.no |

Tekst og bilder til firmasidene ligger i `firma_innhold.py` (hentet fra folloes.no i oktober 2026, med skrivefeil rettet). Sidene lages i `firma_build.py`. Bjørkeved-sidene lages som før i `build.py`, og toppen, menyen og bunnen er felles for alle sider (`head()` og `footer()` i `build.py`).

## Bygg og sjekk

```bash
python3 build.py     # lager nettsiden i public/
python3 sjekk.py     # døde lenker, manglende bilder og ankre, én <h1> per side (exit 1 ved feil)
cd public && python3 -m http.server 8000   # se siden på http://localhost:8000
```

## Testside

`./publiser-test.sh` bygger en testversjon og legger den på `gh-pages`-grenen: **https://andersmathisen7-design.github.io/folloes-nettside/**.
Testversjonen har en gul stripe øverst og blir ikke indeksert av Google. Den bruker ikke den ekte leveringskalenderen, og skjemaene går bare til `ORDER_EMAIL` (ikke kopi til firmaet). Det brukes ikke GitHub Actions.

## Endringer fra folloes.no (UX)

- Overskriften på forsiden sier hva firmaet gjør, ikke bare navnet. Knappene «Få et uforpliktende tilbud» og «Ring» står øverst.
- Hele tjenestekortet er klikkbart, og bildene vises (på folloes.no var de ofte tomme på grunn av lat lasting).
- Kontaktskjemaet står nederst på alle firmasider, med tjenesten valgt på forhånd. Telefon *eller* e-post holder. Svar går til takkesiden.
- Mobil: egen meny, «Få et tilbud»-knapp nederst på skjermen, telefonnummer som kan trykkes.
- Ingen cookie-vegg: siden setter ingen cookies, og skriftene hentes ikke fra Google.
- Bedre kontrast: knappene har mørk tekst på grønt (hvit tekst på `#63C302` var vanskelig å lese), og brødteksten er mørkere grå.
- Den gamle siden «Salg av bjørkeved» viste vintertjenester under «Vi kan hjelpe deg med», og trefelling-siden viste feieoppgaver. Det er rettet.
- Bildene er WebP i to størrelser. Kortbildene er 12–170 kB, mot opptil 1 MB PNG før.

## Før lansering

1. **Domenet (bestemt 22. okt. 2026):** follobjorkeved.no skal sende videre (301) til folloes.no: forsiden til /salg-av-bjorkeved/ og undersidene til samme adresse på folloes.no. Gjøres samme dag som den nye siden går live på folloes.no, ikke før, ellers forsvinner vedsiden i mellomtiden.
2. **Publisering:** Det er ikke satt opp noen workflow ennå. Oppsettet fra follobjorkeved (GitHub Pages, `.github/workflows/pages.yml` i det repoet) kan kopieres med `SITE_URL=https://folloes.no` og `cname: folloes.no`.
3. **Statistikk:** `GOATCOUNTER` i `config.py` er tom. Lag en ny kode for folloes.no.
4. **Kontaktskjemaet** bruker samme FormSubmit-adresse som vedbestillingene (`ORDER_EMAIL`, kopi til `ORDER_CC`).
5. **Search Console:** `GOOGLE_SITE_VERIFICATION` er tom. Koden for follobjorkeved.no gjelder ikke folloes.no.
6. **Sjekk teksten:** «Gratis befaring» står øverst på forsiden og i kontaktblokken. På folloes.no står det bare på siden for vintertjenester. Stemmer det for alle tjenestene?
7. **Kjent svakhet i kalenderen (arvet fra follobjorkeved):** `app.js` sender selv `minutes` og `capacity` når en leveringsdag reserveres, og `kalender/kalender.gs` stoler på tallene. Noen som vil, kan fylle opp eller overbooke en dag. Bør regnes ut i `kalender.gs`.

## Endre priser eller tekst

Alt ligger i **`config.py`**, blant annet pris, bæringstillegg, leveringsgebyr, områder, FAQ og e-postadresse. Bygg siden på nytt etter endringer:

```bash
python3 build.py          # lager nettsiden i public/
```

Hver push til `main` publiseres automatisk med GitHub Actions.

## Bestillinger på e-post

Skjemaet sender til `ORDER_EMAIL` i `config.py` gjennom [FormSubmit](https://formsubmit.co). Tjenesten er gratis og trenger ingen server.

1. Når siden er ute, sender du én testbestilling.
2. FormSubmit sender da en aktiverings-e-post til adressen. Klikk **Activate**.
3. Etter det kommer alle bestillinger som e-post med en tabell over hva kunden har bestilt. Kunden får også en automatisk bekreftelse.
4. Anbefalt: I aktiverings-e-posten får du en tilfeldig kode. Sett den inn som `ORDER_EMAIL` i stedet for e-postadressen. Da vises ikke adressen i kildekoden, og du får mindre spam.

Adressene i `ORDER_CC` i `config.py` (nå post@min-eiendom.no) får en kopi av hver bestilling.

Hvis sending feiler, ser kunden telefonnummeret og kan ringe i stedet.

## Leveringsdager

Kunden velger leveringsdag i skjemaet. Dere kjører bare mandag og tirsdag, med 5 timer per dag. Hver bestilling får en beregnet tid ut fra kjøretid til området, antall sekker og bæring. Når tiden er brukt opp, vises dagen som «Fullt». Ås har kortest kjøretid, så der får flere plass på samme dag. Innstillingene ligger i `DELIVERY_DAYS` i `config.py`.

For at fulle dager skal oppdateres automatisk, må dere sette opp leveringskalenderen (et gratis Google-regneark). Se **[kalender/README.md](kalender/README.md)**.

**Eiersiden** `/admin/` viser alle bestillinger per leveringsdag, med antall sekker per dag, status (ny, bekreftet, levert, avbestilt), telefonbestillinger og kjøreliste til utskrift. Den bruker samme kalender. Se kalender/README.md.

## Besøksstatistikk

Dashbord: **https://follobjorkeved.goatcounter.com**. Du logger inn med amkleven@gmail.com.
Det viser besøk per side, hvor folk kommer fra (Google, Facebook osv.) og disse hendelsene:
«Sjekket pris i skjemaet» (endret antall eller bæring), «Begynte på bestilling» (begynte på adresse eller kontaktinfo), «Trykket Send, men et felt manglet: …» (ett per felt, f.eks. Telefon), «Endret antall sekker til: …» (gruppe, f.eks. 20-29 eller 100+, når kunden endrer fra standard 50), «Valgte leveringsdag», «Bestilling sendt», «Bestilte antall sekker: …», «Valgte hvor ofte: …» (en-gang, 2-uker, 4-uker eller 6-uker i skjemaet), «Bestilte med hyppighet: …» (vedabonnement eller én gang i sendt bestilling), «Trykket på telefonnummer» og «Feil ved sending av bestilling».
For hendelsene viser «kilde» (referrer) siden hendelsen skjedde på, for eksempel `follobjorkeved.no/ved-as`. Da ser du hvilke sider som gir bestillinger. Hvor besøkende kom fra, ser du på sidene selv.
GoatCounter bruker ingen cookies, så siden trenger ikke samtykkebanner.

## Google Analytics / Ads / Meta (valgfritt)

Fyll inn `GA4_ID`, `GADS_ID`/`GADS_CONVERSION` og `META_PIXEL_ID` i `config.py`. Siden sender da disse hendelsene:
- `generate_lead`: en bestilling er sendt. Verdien er i NOK.
- `click_tel`: noen har trykket på telefonnummeret.
- `begin_checkout`: noen har begynt å fylle ut skjemaet.

**Merk:** Slår du på Google Analytics eller Meta Pixel, krever norsk lov at besøkende samtykker til cookies. Da må du legge inn et samtykkebanner. Uten slike ID-er setter siden ingen cookies.
