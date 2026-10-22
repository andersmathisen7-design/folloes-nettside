# Synlighet i Google og KI-søk: folloes.no

*Laget 22. oktober 2026. Hvert tiltak har en kilde eller en egen måling. Der vi har måttet anta noe, står det* **(antakelse)**.

Gjelder den nye folloes.no: firmasidene til Follo Eiendomsservice AS og bjørkeved-sidene som flyttes over fra follobjorkeved.no. For selve vedmarkedet, se [ANALYSE.md](ANALYSE.md). For lenker, se [LENKEBYGGING.md](LENKEBYGGING.md).

---

## 1. Kort svar: gjør dette, i denne rekkefølgen

| # | Tiltak | Hvorfor (data) |
|---|---|---|
| 1 | **Send mineiendomsservice.no videre til folloes.no (301).** | Den er en full kopi av folloes.no: samme tittel og samme telefonnummer, og begge oppgir seg selv som originalen. For «vaktmester Follo» ligger kopien på plass 5 og folloes.no på plass 9 (kap. 2). Google viser vanligvis bare én av to like sider. |
| 2 | **Gjør flyttingen riktig.** Sett opp Search Console og Bing Webmaster Tools for alle tre domenene *før* lansering. Send hver gammel adresse videre med 301 til sin nye. | Google: «Expect temporary fluctuation in site ranking during the move». Videresendingene bør stå «generally at least 1 year». I dag finnes ingen Search Console for folloes.no (`GOOGLE_SITE_VERIFICATION` er tom). Uten den kan vi ikke se hva vi mister. |
| 3 | **Google-bedriftsprofil og anmeldelser.** | Profilen og anmeldelsene er de to tyngste faktorene for kartet (Whitespark 2026). 47 % bruker ikke et firma med under 20 anmeldelser, og 74 % ser etter anmeldelser fra de siste tre månedene (BrightLocal 2026). |
| 4 | **Egne sider per tjeneste og sted, med mer innhold.** For eksempel «Brøyting i Ås» og «Vaktmester i Ski». | Nr. 1 og 2 av faktorene for vanlige lokale treff er «Dedicated Page for Each Service» og stedsord i teksten (Whitespark 2026). Vår egen måling viser det samme: vedsidene per sted får mest trafikk fra Google, og begge bestillingene 05.–12.10 kom fra /ved-as. Firmasidene har i dag bare ca. 150 ord hver. |
| 5 | **KI-søk:** bli nevnt på andre nettsider, ikke bare på egen side. | 69 % av nordmenn brukte generativ KI i 2026 (SSB). Blant faktorene for KI-synlighet ligger «best of»-lister, bransjesider og omtaler i aviser og offentlige sider øverst (Whitespark 2026). |

---

## 2. Slik står det til i dag (egne målinger 22.10.2026)

### Dagens folloes.no (WordPress)

| Funn | Tall | Hva det betyr |
|---|---|---|
| Adresser i sitemap | 18 | 16 av dem finnes i den nye siden med samme adresse. Bare `/hello-world/` (WordPress sitt eksempelinnlegg) og `/category/uncategorized/` mangler. De to skal ikke med. |
| Tittel på forsiden | «Vaktmester \| Follo Eiendomsservice AS \| Brøyting Ås» | **«Brøyting Ås» er borte i den nye tittelen.** Tittelen kan være grunnen til at siden dukker opp i søk etter brøyting i dag. Sjekk det i Search Console før den endres (tiltak 2). |
| Strukturerte data | Bare `Organization` (fra Yoast) | Den nye siden har `LocalBusiness` med adresse, telefon og org.nr., og `Service` på hver tjenesteside. Det er bedre. |
| Sidevekt | 128–162 kB HTML, ca. 40 skript og 20 CSS-filer per side | Den nye siden er statisk HTML uten tunge skript. |

### mineiendomsservice.no

- Den kjører en egen WordPress-installasjon med samme innhold som folloes.no. Forsiden har tittelen «Vaktmester | Follo Eiendomsservice AS | Brøyting Ås», og telefonnummeret er 48 99 39 00.
- Hver side oppgir seg selv som originalen (`canonical`), for eksempel `https://www.mineiendomsservice.no/vintertjenester/`. Den lenker ikke til folloes.no.
- Google slår slike like sider sammen og viser bare én av dem. Hvilken det blir, bestemmer Google selv. Et 301-signal er det sterkeste signalet vi kan gi ([Google: konsolidering av duplikater](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)).
- I dag ser det ut til at kopien vinner. Søk på «vaktmester Follo» (Bing, norsk region, 22.10):

| Plass | Treff |
|---|---|
| 1 | follovaktmestern.no (Follo Vaktmesterselskap AS) |
| 2 | follovs.no (samme firma) |
| 3 | vk.no/avdeling-follo |
| 4 | follovs.no/omoss |
| **5** | **mineiendomsservice.no** |
| 6 | gulesider.no |
| 7 | alt-mann.no |
| **9** | **folloes.no** |

*Merk: Bing og DuckDuckGo stengte for automatiske søk etter første spørsmål. De andre søkeordene ga ikke brukbare svar. Riktige plasseringer i Google får vi bare fra Search Console (tiltak 2).*

### Den nye siden (`public/`, bygget 22.10)

| Sidetype | Ord per side (med meny og bunn) | Egen tekst | Strukturerte data |
|---|---|---|---|
| Vedsider per sted (7 stk.) | ca. 1 250 | ca. 1 000 | LocalBusiness, Product, FAQPage, BreadcrumbList |
| Tjenestesider (8 stk.) | 390–490 | **ca. 150** | Service, BreadcrumbList |
| Om oss og referanser | 440–570 | lite | bare BreadcrumbList |

Titlene på tjenestesidene er bare tjenestenavnet: «Trefelling | Follo Eiendomsservice AS» og «Vintertjenester | …». Siden for matteutleie heter «Høykvalitets matter», så ordet «matteutleie» står ikke i tittelen.

### Trafikk som allerede kommer (follobjorkeved.no, GoatCounter)

05.–12.10 kom det 46 besøk. 30 av dem kom fra Google og 6 fra chatgpt.com. Begge bestillingene kom fra /ved-as. Google sendte mest trafikk til områdesidene (Ski 9, Ås 4, Drøbak 4). chatgpt.com sendte trafikk til /vedpris og til områdesidene. Kilde: [ukesrapporter/2026-10-12.md](ukesrapporter/2026-10-12.md).

**Konklusjon:** Oppskriften virker allerede for ved: én side per sted, med pris, FAQ og strukturerte data. Firmatjenestene har ikke fått den samme oppskriften ennå.

---

## 3. Hva avgjør plasseringen i Google

### Googles egne ord
Lokale resultater er «hovedsakelig basert på relevans, avstand og prominens». Om anmeldelser: «Med flere anmeldelser og positive vurderinger kan du få høyere lokal rangering.» Om informasjonen: «Bedrifter med fullstendig og nøyaktig informasjon har større sjanse for å vises i lokale søkeresultater.» ([Google Bedriftsprofil-hjelp](https://support.google.com/business/answer/7091?hl=no))

### Whitespark Local Search Ranking Factors 2026
Dette er en spørreundersøkelse blant 47 eksperter, som har vurdert 187 faktorer. Den ble publisert 6. november 2025 og viser hva fagfolk mener, ikke Googles egne vekter ([Whitespark](https://whitespark.ca/local-search-ranking-factors/)).

| Kartet (local pack) | Vanlige lokale treff | KI-søk |
|---|---|---|
| 1. Hovedkategori i bedriftsprofilen | 1. **Egen side for hver tjeneste** | 1. Med på «best of»-lister |
| 2. Avstand til den som søker | 2. **Stedsord i innholdet** | 2. Egen side for hver tjeneste |
| 3. Søkeord i firmanavnet i profilen | 3. Kvaliteten på lenker til domenet | 3. Synlig på viktige bransjesider |
| 4. Adresse i stedet det søkes fra | 4. Søkeord i tittelen på siden profilen lenker til | 4. Omtaler i aviser, blogger, offentlige sider og foreninger |
| 5. Åpen når det søkes | 5. Lenker fra sider i samme bransje | 5. Anmeldelser på sider med høy tillit |

Vekter per gruppe for kartet, slik [Advice Local](https://www.advicelocal.com/?p=20716) gjengir 2026-utgaven: bedriftsprofil 32 %, anmeldelser 20 %, innhold på siden 15 %, atferd 9 %, lenker 8 %, kataloger 6 %. For vanlige lokale treff er innhold på siden 33 % og lenker 24 %. *(Gjengitt av andre, ikke sjekket mot Whitesparks egen figur.)*

### Hva kundene gjør: BrightLocal Local Consumer Review Survey 2026
Undersøkelsen er gjort blant 1 002 voksne i USA i februar 2026, så norske tall kan avvike **(antakelse)** ([BrightLocal](https://www.brightlocal.com/research/local-consumer-review-survey/)).
- 97 % leser anmeldelser av lokale firma, og 41 % gjør det alltid (29 % i 2025).
- 31 % bruker bare firma med 4,5 stjerner eller mer (17 % i 2025). 68 % krever minst 4.
- 47 % bruker ikke et firma med under 20 anmeldelser.
- 74 % ser etter anmeldelser fra de siste tre månedene.
- 80 % velger heller et firma som svarer på alle anmeldelser. 50 % mislikker ferdigskrevne standardsvar.
- 45 % brukte ChatGPT eller andre KI-verktøy for å finne lokale firma (6 % året før).

---

## 4. KI-søk (ChatGPT, Google AI Overviews og AI Mode, Copilot, Perplexity)

| Fakta | Kilde |
|---|---|
| **69 %** av nordmenn mellom 16 og 79 år brukte generativ KI i 2026. Det var 54 % i 2025 og 36 % i 2024. Etter alder: 72 % (45–54 år), 58 % (55–64 år) og 34 % (65–74 år). Styremedlemmer i borettslag og huseiere er altså også med. | SSB, tabell [14365](https://www.ssb.no/statbank/table/14365) |
| Google AI Mode og AI Overviews finnes i Norge og på norsk. | [Google-hjelp, AI Mode](https://support.google.com/websearch/answer/16011537), [Tek.no](https://www.tek.no/nyheter/nyhet/i/5EPbO1/googles-soek-faar-ai-mode-i-norge) |
| Når Google viser en KI-oppsummering, falt klikkraten på vanlige treff fra 1,76 % til 0,61 % (−61 %). Merkevarer som er sitert i oppsummeringen, får flere klikk enn de som ikke er det. Målingen gjelder informasjonssøk, ikke søk som «brøyting Ås». | [Seer Interactive, sept. 2025](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update) |
| OpenAI: OAI-SearchBot «is used to surface websites in search results in ChatGPT's search features». OpenAI anbefaler å slippe den inn i robots.txt. | [OpenAI](https://developers.openai.com/api/docs/bots) |
| Google bruker ikke llms.txt i søk. Fila verken skader eller hjelper. | [Search Engine Journal](https://www.searchenginejournal.com/googles-llms-txt-guidance-depends-on-which-product-you-ask) |

**Hva dette betyr for oss:**
- `robots.txt` slipper inn alle roboter. Det er riktig, så det skal ikke endres.
- `llms.txt` kan bli liggende. Den koster ingenting, men den alene gir ikke plass i KI-svarene.
- Det som teller, er det samme som for Google: én side per tjeneste, svar i klartekst (pris, område, hvordan det foregår), anmeldelser, og at andre nettsider nevner firmaet.
- Data som andre kan sitere, virker allerede. Det viser trafikken fra chatgpt.com til /vedpris.

---

## 5. Tiltakene i detalj

### Tiltak 1: mineiendomsservice.no → folloes.no
- Hver adresse sendes videre med 301 til samme adresse på folloes.no. Forsiden går til forsiden, og `/vintertjenester/` går til `/vintertjenester/`. Gjør det samme dag som den nye siden går live.
- I Search Console bekrefter du begge domenene og bruker «Adresseendring» fra mineiendomsservice.no til folloes.no ([Google: flytte nettsted](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)).
- **Avklar først:** Hvem eier mineiendomsservice.no, og hvor ligger den? Den kjører på samme type server (nginx og WordPress) som folloes.no. Bruker dere fortsatt e-postadressen @min-eiendom.no? Den ligger på et annet domene og påvirkes ikke.

### Tiltak 2: flyttingen
1. **Nå, mens den gamle siden lever:** Bekreft folloes.no i Search Console med en DNS-post. Legg inn koden i `GOOGLE_SITE_VERIFICATION`. Les av hvilke søk som gir klikk i dag, for eksempel om «brøyting ås» står der. Gjør det samme i Bing Webmaster Tools, som kan importere fra Search Console.
2. **Adressekart:**
   - follobjorkeved.no har 31 adresser. Forsiden går til `/salg-av-bjorkeved/`, og resten går til samme adresse (som README sier).
   - folloes.no har 16 av 18 adresser uendret.
   - Alle de ca. 24 interne adressene på mineiendomsservice.no går til samme adresse på folloes.no.
3. **Viktig teknisk forbehold:** GitHub Pages kan ikke sende 301 fra serveren. Videresendingen fra follobjorkeved.no og mineiendomsservice.no må derfor gjøres hos domeneleverandøren (videresending i Domeneshop eller Plesk) eller med en liten server. Sjekk at stien blir med, slik at `follobjorkeved.no/ved-as/` havner på `folloes.no/ved-as/` og ikke på forsiden. Test med `curl -I` på 5–10 adresser etter lansering.
4. La videresendingene stå i minst ett år (Google).
5. Regn med svingninger i noen uker. Følg med i den ukentlige rapporten.

### Tiltak 3: Google-bedriftsprofil og anmeldelser
- **Én profil** for Follo Eiendomsservice AS.
  - Hovedkategorien er den viktigste enkeltfaktoren (Whitespark). Velg den kategorien som passer best for vaktmester- og eiendomsservice, og legg brøyting, trefelling og ved som tilleggskategorier.
  - Lenk profilen til `https://folloes.no/`.
  - Legg inn tjenesteområdet: de seks Follo-kommunene.
- **Samme navn, adresse og telefon overalt:** Proff, Gule Sider, 1881, Brønnøysund, Facebook, Mittanbud og bedriftsprofilen. Det gamle navnet Min Eiendomsservice AS må ut der det fortsatt står. Google sier at feil informasjon kan gjøre at profilen ikke vises.
- **Anmeldelser:**
  - Mål: 20 innen 1. februar 2027 (BrightLocal: 47 % godtar ikke færre).
  - Spør jevnt, fordi 74 % ser på de siste tre månedene.
  - Svar på alle med et eget svar, ikke en ferdig mal.
  - Spør styreleder i hvert borettslag dere har avtale med. De er gode referanser og skriver gode anmeldelser **(antakelse)**.
- Ikke legg inn egne stjerner i de strukturerte dataene (`aggregateRating`) på egen side. Google viser ikke stjerner som firmaet har samlet om seg selv for `LocalBusiness` ([Google: anmeldelsesutdrag](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)).

### Tiltak 4: tjenestesider etter samme oppskrift som vedsidene
1. **Bedre titler.** Tittelen er blant de fem viktigste faktorene for vanlige lokale treff. Forslag:
   - Forsiden: behold «Brøyting Ås» til Search Console viser hva som gir klikk. For eksempel «Vaktmester og brøyting i Ås og Follo | Follo Eiendomsservice».
   - `/vintertjenester/`: «Brøyting og snømåking i Ås og Follo | Follo Eiendomsservice». Folk søker på hva de trenger, og «vintertjenester» er et bransjeord **(antakelse, sjekk søkevolum i Google Ads Søkeordplanlegger, som er gratis)**.
   - `/matteutleie/`: «Matteutleie og vask av inngangsmatter i Follo».
   - `/trefelling/`: «Trefelling i Ås, Ski og Follo – også på trange tomter».
2. **Mer innhold per tjenesteside.** Gå fra ca. 150 til 600–1 000 ord egen tekst, som på vedsidene:
   - hva som er med
   - hvem det passer for (borettslag, private, næring)
   - prisnivå eller hvordan prisen regnes ut
   - hvordan en avtale foregår
   - område (kommunene)
   - 4–6 vanlige spørsmål med svar (FAQ)
   - bilder fra ekte jobber
3. **Egne sider per sted**, men bare der dere faktisk har oppdrag. Begynn med de to tjenestene som gir mest penger, i de to kommunene der dere har flest kunder. For eksempel `/broyting-as/` og `/vaktmester-ski/`.
   - Hver side må ha egne opplysninger: referanser fra stedet, typiske oppdrag og kjøretid.
   - Like sider der bare stedsnavnet er byttet ut, regner Google som spam ([Google: «doorway»-sider](https://developers.google.com/search/docs/essentials/spam-policies#doorways)).
4. **Referansesiden:** Legg inn navngitte borettslag eller bedrifter (med samtykke), hva dere gjør for dem, et sitat og et bilde. Det gir både tillit og stedsord.
5. **Små rettelser:**
   - Beskrivelsen på forsiden er 184 tegn, og Google kutter rundt 155. Forkort den.
   - 14 titler er over 65 tegn (mest vedsidene og artiklene), så «Follo Bjørkeved» kuttes. Det har lite å si fordi prisen og emnet står først.
   - Legg `areaServed` med de seks kommunene og `sameAs` (bedriftsprofil, Facebook, Proff) inn i `LocalBusiness`.

### Tiltak 5: bli nevnt andre steder (Google og KI)
Dette er faktor 1, 3 og 4 for KI-synlighet hos Whitespark:
- **Follo Næringsforening**, Proff og Mittanbud med anmeldelser.
- **Lokalaviser:** Pressesaken om vedpriser er klar i [LENKEBYGGING.md](LENKEBYGGING.md). Lag en tilsvarende sak om vinterdrift for borettslag før første snøfall, for eksempel «Hva koster brøyting for et borettslag i Follo?» med ekte tall.
- **Lister:** Be om å bli med på lister som «vaktmester i Follo» hos Gule Sider, Mittanbud og lokale nettsteder.
- **Data som andre kan sitere:** Det fungerer allerede for /vedpris. En tilsvarende side for vinterdrift kan gi lenker og KI-sitater **(antakelse)**.

---

## Status 22.10.2026 (grenen `synlighet`)

**Gjort i koden:**
- Nye titler med sted på forsiden og alle tjenestesidene. «Brøyting» og «Ås» er tilbake i tittelen på forsiden.
- FAQ med 5 spørsmål og FAQPage-data på hver av de 8 tjenestesidene. Svarene bygger bare på det som står om tjenesten.
- `areaServed` på tjenestene er de seks kommunene, ikke bare «Follo».
- Ny del **/rad/**: hjelpeartikler for firmatjenestene, i Markdown i `rad/`. Hver tjenesteside lenker til sine råd, og rådene står i llms.txt og sitemap. De første seks:
  - snømåking på fortau
  - snø på taket
  - strøgrus om våren
  - trær mot naboen
  - lekeplass i borettslaget
  - brannsikkerhet i borettslag

  Lovhenvisningene er kontrollert mot Lovdata 22.10.2026, blant annet politivedtektene for alle seks kommunene.

**Krever deg eller broren din (kan ikke gjøres i koden):** tiltak 1–3 og 5, Search Console, GoatCounter-kode, Google-bedriftsprofil og anmeldelser.

**Neste artikler, forslag:** brøyteavtale for borettslag, vaktmester for borettslag (hva avtalen bør inneholde), beskjæring av hekk og trær (når på året), vårens vedlikeholdsliste for styret.

---

## 6. Hva vi ikke vet ennå, og hvordan vi finner det ut

| Ukjent | Hvordan |
|---|---|
| Riktig plass i Google for hvert søkeord | Search Console for folloes.no (tiltak 2). Kom i gang før lansering, så vi har tall fra før flyttingen å sammenligne med. |
| Hvor mange som søker på «brøyting Ås», «vaktmester Ski» osv. | Google Ads Søkeordplanlegger (gratis med en Ads-konto). Ikke målt her. |
| Hvor mange som kommer fra KI | GoatCounter for folloes.no. `GOATCOUNTER` i `config.py` er tom. Henvisninger fra chatgpt.com, perplexity.ai og copilot vises som egne kilder. |
| Hva ChatGPT svarer om «vaktmester i Follo» | Spør ChatGPT, Gemini og Copilot med de samme 5 spørsmålene hver måned, og noter om folloes.no blir nevnt. Svarene varierer fra gang til gang (BrightLocal), så ta hvert spørsmål 3 ganger. |

---

## Kilder
- Google: [Lokal rangering](https://support.google.com/business/answer/7091?hl=no) · [Flytte nettsted](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes) · [Duplikater](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) · [Spam-regler](https://developers.google.com/search/docs/essentials/spam-policies) · [AI Mode](https://support.google.com/websearch/answer/16011537)
- [Whitespark Local Search Ranking Factors 2026](https://whitespark.ca/local-search-ranking-factors/) · [Advice Local om vektene](https://www.advicelocal.com/?p=20716)
- [BrightLocal Local Consumer Review Survey 2026](https://www.brightlocal.com/research/local-consumer-review-survey/)
- [SSB tabell 14365: bruk av KI](https://www.ssb.no/statbank/table/14365)
- [Seer Interactive: AI Overviews og klikkrate](https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update)
- [OpenAI: robotene](https://developers.openai.com/api/docs/bots) · [Search Engine Journal om llms.txt](https://www.searchenginejournal.com/googles-llms-txt-guidance-depends-on-which-product-you-ask) · [Tek.no om AI Mode i Norge](https://www.tek.no/nyheter/nyhet/i/5EPbO1/googles-soek-faar-ai-mode-i-norge)
- Egne målinger 22.10.2026: sitemap og HTML for folloes.no, mineiendomsservice.no og follobjorkeved.no, `public/` i dette repoet, Bing med norsk region, og GoatCounter (ukesrapporten 12.10).
