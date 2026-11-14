# Lansering av nye folloes.no

Alle domenene (folloes.no, follobjorkeved.no, garasjevasken.no, garasjevask.no) har DNS hos **Domeneshop**.
I dag går folloes.no til WordPress (217.170.205.89), og follobjorkeved.no ligger allerede på GitHub Pages.

**Hvem gjør hva:** 🤖 = Claude gjør det. 👤 = du må gjøre det (krever innlogging hos Domeneshop, Google eller GitHub-innstillingene).

## Allerede gjort (7. nov. 2026)

- 🤖 Endringene fra follobjorkeved.no siden 22. okt. er flettet inn: tre nye artikler (aske, vedovn som ryker inn, kuldeperiode), bestilling via leveringskalenderen med bekreftelse på e-post, eiersiden og testene. Kontaktskjemaet og bestillingsskjemaet er testet i nettleser.
- 🤖 Alle adressene fra gamle folloes.no, follobjorkeved.no og garasjevasken.no finnes på den nye siden. De tre WordPress-restene (`/hello-world/`, `/category/uncategorized/`, `/author/verdimedia/`) sender til forsiden.
- 🤖 Publisering: `.github/workflows/pages.yml` bygger og legger siden på `gh-pages` med domenet folloes.no, og varsler Bing (IndexNow). Den kjøres foreløpig bare med knapp, så testsiden ikke overskrives.
- 🤖 `publiser-test.sh` nekter å kjøre når den ekte siden ligger på `gh-pages`.
- 🤖 `lag-omdirigering.py` lager omdirigeringssiden for follobjorkeved.no: hver gammel adresse sender til samme adresse på folloes.no (forsiden til `/salg-av-bjorkeved/`).
- 🤖 `hent-ved.sh` henter nye endringer fra follobjorkeved.no fram til lanseringsdagen.
- 🤖 Statistikken bruker samme GoatCounter som før («follobjorkeved»), så historikken følger med. Testsiden teller ikke.

## Før lanseringsdagen

1. 👤 **Les gjennom testsiden** (https://andersmathisen7-design.github.io/folloes-nettside/) og godkjenn tekstene. Spesielt: står «Gratis befaring» riktig for alle tjenestene? Stemmer prisene for garasjevask med garasjevasken.no?
2. 👤 **Ta en sikkerhetskopi av WordPress-siden** hvis dere vil ha den (hos den som drifter folloes.no i dag). Den slutter å vises når DNS endres.
3. 👤 **Si opp WordPress-hostingen** først *etter* lanseringen.

## Bestillinger og henvendelser: appen Nettsideferdig (14. nov. 2026)

Vedbestillingen, kontaktskjemaet og garasjevask går til appen (`APP_URL` i `config.py`, `folloes.app.nettsideferdig.no`).
Alt styres i admin: https://folloes.app.nettsideferdig.no/admin. Varsler om bestillinger og henvendelser går til
`post@min-eiendom.no`. Den egne serveren (`server/`, Cloudflare D1) og FormSubmit er fjernet.

| # | Hvem | Hva |
|---|---|---|
| A1 | 👤 | Inviter andersmathisen7@gmail.com som eier i admin (Tilgang), så Claude kan sette opp resten. |
| A2 | 🤖 | Priser, bæring, leveringsdager (mandag og fredag, 7,5 timer), stengte dager og varsler i admin. |
| A3 | 🤖 | Importer bestillingene fra regnearket (Claude leser det fra Google Drive). Én gang før byttet og én gang rett etter. |
| A4 | 🤖 | Test en bestilling og en henvendelse mot appen i testmodus, så slå testmodus av. |

Regnearket blir stående som sikkerhetskopi. Kalenderskriptet trengs ikke lenger, så punkt 9 under (CLASPRC_JSON) faller bort.

## Lanseringsdagen (rekkefølgen er viktig)

| # | Hvem | Hva |
|---|---|---|
| 1 | 🤖 | `./hent-ved.sh`, sjekk og commit. Slå sammen til `main` (du godkjenner PR-en). |
| 2 | 🤖 | Kjør «Publiser folloes.no» i Actions. Testsiden på github.io erstattes da av den ekte siden. |
| 3 | 👤 | **Domeneshop → folloes.no → DNS** (se under). |
| 4 | 👤 | **GitHub → folloes-nettside → Settings → Pages:** sjekk at Custom domain er `folloes.no`. Når sertifikatet er klart (10 min–1 time), kryss av **Enforce HTTPS**. |
| 5 | 🤖 | Sjekk at alle sidene svarer på https://folloes.no, og at skjemaene kommer fram. |
| 6 | 🤖 | follobjorkeved.no: legg omdirigeringssiden på `gh-pages` i repoet ved-folle-eiendom, og skru av den gamle publiseringen der. DNS for follobjorkeved.no trenger ingen endring. |
| 7 | 👤 | **Domeneshop → garasjevasken.no og garasjevask.no → Videresending:** til `https://folloes.no/garasjevask/`, permanent (301). |
| 8 | 🤖 | Slå på automatisk publisering (push-linjene i `pages.yml`), og flytt den ukentlige jobben og kalenderskriptet hit. |
| 9 | 👤 | Bare hvis regnearket fortsatt brukes (databasen ikke er tatt i bruk): **GitHub → folloes-nettside → Settings → Secrets → Actions:** legg inn `CLASPRC_JSON` (samme verdi som i ved-folle-eiendom). |
| 10 | 👤 | **Google Search Console:** legg til domenet folloes.no (TXT-post hos Domeneshop), send inn `https://folloes.no/sitemap.xml`, og be om indeksering av forsiden og `/salg-av-bjorkeved/`. Gi meg koden, så legger jeg den inn (`GOOGLE_SITE_VERIFICATION`) hvis du heller vil bruke meta-tag. |
| 11 | 👤 | **Bing Webmaster Tools:** importer folloes.no fra Search Console. |
| 12 | 👤 | **Google-bedriftsprofilen og katalogene** (Gule Sider, 1881, Proff, Vednett osv.): bytt nettsiden til `https://folloes.no/salg-av-bjorkeved/` for veden og `https://folloes.no/` for firmaet. |

### DNS for folloes.no hos Domeneshop (punkt 3)

Domeneshop → Mine domener → folloes.no → **DNS-pekere**. Hvis domenet peker til et webhotell eller har videresending, slå det av først.

| Vert | Type | Data |
|---|---|---|
| (tom) / `@` | A | `185.199.108.153` |
| (tom) / `@` | A | `185.199.109.153` |
| (tom) / `@` | A | `185.199.110.153` |
| (tom) / `@` | A | `185.199.111.153` |
| `www` | CNAME | `andersmathisen7-design.github.io` |

Slett den gamle A-posten `217.170.205.89` og en eventuell gammel `www`-post. Ikke rør MX- eller TXT-poster.
Det kan ta fra noen minutter til et par timer før alle ser den nye siden.

**Obs:** garasjevask.no har e-post hos Domeneshop (MX `mx.domeneshop.no`). Ved videresending (punkt 7) skal MX-posten stå urørt.

## Om omdirigeringen fra follobjorkeved.no

GitHub Pages kan ikke sende ekte 301-svar. Omdirigeringssidene bruker derfor `canonical` og en umiddelbar `meta refresh`, som Google behandler som permanent flytting. Søkeresultatene flyttes over i løpet av noen uker. Verktøyet «Adresseendring» i Search Console krever ekte 301 og fungerer kanskje ikke. Det er ikke nødvendig.
