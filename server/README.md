# Serveren: database for bestillinger og henvendelser

Erstatter leveringskalenderen i Google-regnearket (`kalender/`). Den er en **Cloudflare Worker** med en **D1-database** (SQLite hos Cloudflare). Den svarer på de samme forespørslene som kalenderskriptet, så bestillingsskjemaet og eiersiden virker som før. I tillegg gjør den dette:

- **Kontaktskjemaet** på firmasidene, også forespørsler om garasjevask, lagres i databasen og vises under **Henvendelser** på eiersiden. Der kan de merkes som besvart eller arkiveres.
- **Flytt dag:** en bestilling kan flyttes til en annen leveringsdag fra eiersiden. Før måtte datoen endres i regnearket.
- **E-post** sendes med [Resend](https://resend.com): bestillingen og henvendelsen går til eieren, og kunden får en bekreftelse. Mangler Resend, eller feiler sendingen, sender nettsiden skjemaet gjennom FormSubmit som før. Bestillingen er da lagret uansett.

Pris: 0 kr på gratisnivået til Cloudflare og Resend. Det holder til titusenvis av bestillinger, og Resend sender opptil 3 000 e-poster i måneden.

## Filer

| Fil | Hva |
|---|---|
| `src/logikk.js` | All logikk: kapasitet per dag, ruteberegning (Kartverket og OSRM), innlogging, e-post |
| `src/index.js` | Inngangen Cloudflare kaller |
| `migrations/` | Tabellene i databasen |
| `wrangler.toml` | Innstillinger: mottakere av e-post, avsender, leveringsdager, tillatte nettsider |
| `passord.mjs` | `npm run passord`: nytt passord til eiersiden (vises én gang). `-- --logg-ut-alle` logger ut alle enheter |
| `importer.mjs` | `npm run importer -- Bestillinger.csv`: flytter bestillingene fra regnearket inn i databasen |
| `test/server.test.js` | `npm test`: 23 tester i Cloudflares lokale simulator. Kartverket, OSRM og e-post er simulert |

## Oppsett (én gang)

**Du gjør dette:**

1. **Cloudflare-konto:** https://dash.cloudflare.com/sign-up (gratis, ingen kort).
2. **API-nøkkel til Claude:** My Profile → API Tokens → Create Token → malen **Edit Cloudflare Workers**. Legg til **Account → D1 → Edit**, og trykk Create. Claude ber om nøkkelen i et sikkert skjema, så den aldri står i chatten.
3. **Resend** (e-post): https://resend.com/signup → Domains → Add domain `folloes.no` (region EU). Legg inn DNS-postene Resend viser hos **Domeneshop**. Dette er bare TXT- og MX-poster på underdomenet `send`, så de påvirker ikke nettsiden eller annen e-post. Lag så en API-nøkkel (Sending access).
4. **Resend-nøkkelen inn i Cloudflare:** Workers & Pages → folloes → Settings → Variables and Secrets → Add → Type **Secret**, navn `RESEND_API_KEY`, lim inn nøkkelen.

**Claude gjør resten:**

```bash
cd server && npm install
npx wrangler d1 create folloes          # database_id inn i wrangler.toml
npm run deploy                          # lager tabellene og publiserer serveren
npm run passord                         # passordet til eiersiden
npm run importer -- Bestillinger.csv    # bestillingene fra regnearket
```

Til slutt settes adressen serveren fikk (`https://folloes.<konto>.workers.dev`) som `SERVER_URL` i `config.py`, og nettsiden publiseres.

## Daglig bruk

Alt skjer på eiersiden, https://folloes.no/admin/: bestillinger, telefonbestillinger, flytt dag, endre sekker, levert og betalt, fulle dager og henvendelser.

Vil du se rådataene: Cloudflare → Storage & Databases → D1 → folloes → **Explore Data**. Der kan du også rette en bestilling direkte.

## Sikkerhetskopi

Cloudflare kan spole databasen tilbake til et hvilket som helst tidspunkt de siste 7 dagene (**Time Travel**). Ta i tillegg en egen kopi nå og da:

```bash
npx wrangler d1 export folloes --remote --output=folloes-$(date +%F).sql
```

Filen er vanlig SQL og kan åpnes i hvilket som helst SQLite-program.

## Sikkerhet

- **Passordet** lagres bare som salt + PBKDF2-sjekksum (100 000 runder). Innloggingen gir en tilfeldig billett som utløper etter 12 timer, eller etter 30 dager med «Husk meg». Bare sjekksummen av billetten lagres.
- **Gjetting:** etter 10 feil passord på 15 minutter stenges innloggingen i 15 minutter.
- **Uten innlogging** får man bare vite minutter per dag og om en adresse får plass, aldri kundedata.
- **Misbruk:** nettbestillinger godtas bare for leveringsdager fra i morgen og 6 uker fram, og maks 30 i timen. Henvendelser er også begrenset til 30 i timen.
- **E-post til kunden** er en fast tekst med tall og dato serveren har kontrollert, aldri fritekst fra skjemaet. Ingen kan altså bruke skjemaet til å sende egne e-poster fra dere.
- **Samtidige bestillinger:** sendes to bestillinger til den siste plassen samtidig, beholdes den som kom først, og den andre kunden blir bedt om å velge en annen dag.
- **Kartverket** får adressen, og **OSRM** får bare koordinater, aldri navn eller telefon.

## Leveringsdager

Dagene står to steder, og de må være like: `LEVERINGSDAGER` i `wrangler.toml` og `DELIVERY_DAYS["weekdays"]` i `config.py`. Endrer du dem, kjør `npm run deploy` og publiser nettsiden.
