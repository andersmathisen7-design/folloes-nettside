# -*- coding: utf-8 -*-
# Alt innhold fra de gamle folloes.no-sidene, som rene Python-data.
# Kilde: _kilde/*.txt og _kilde/bilder.json (nøkler i fra_original).

SEASONS = [
    {
        "name": "Vår",
        "text": "Når snøen smelter er det tid for å rydde opp etter vinteren. Vi klargjør uteområder for en ny sesong.",
    },
    {
        "name": "Sommer",
        "text": "Sommeren er tiden for å holde eiendommen ryddig og velstelt. Vi tar oss av små og store oppgaver underveis.",
    },
    {
        "name": "Høst",
        "text": "Når bladene faller gjør vi eiendommen klar for vinteren. Opprydding og vedlikehold før kulden setter inn.",
    },
    {
        "name": "Vinter",
        "text": "Når snøen kommer sørger vi for trygge og fremkommelige uteområder med brøyting og strøing.",
    },
]

INTRO = {
    "h2": "Vaktmester- og vedlikeholdstjenester i Follo",
    "text": [
        "Tidligere Min Eiendomsservice AS har nå byttet navn til Follo Eiendomsservice AS! Vårt mål er å levere vaktmester- og vedlikeholdstjenester til privatpersoner, borettslag og bedrifter, med hovedfokus på Follo og nærliggende områder. Dette er vårt satsingsområde.",
        "Vi legger vår stolthet i å levere kvalitetsarbeid hver gang!",
    ],
    "list_h3": "Vaktmester- og vedlikeholdstjenester vi tilbyr:",
    "list": [
        "Vaktmestertjenester – gressklipping, vedlikehold av uteareal og bortkjøring av avfall.",
        "Vintertjenester – som strøing og måking.",
        "Feiing og spyling.",
        "Renhold – kontorvask, vask av kantine/kjøkken, trappevask, vindusvask, fasadevask.",
        "HMS – brannsikring og kontroll av lekeplasser.",
        "Matteutleie – for renere lokaler og et godt førsteinntrykk.",
        "Salg av bjørkeved – Vi leverer og bærer veden dit du ønsker.",
    ],
}

SERVICES = [
    {
        "slug": "vaktmestertjenester",
        "name": "Vaktmestertjenester",
        "title": "Vaktmestertjenester i Follo | Follo Eiendomsservice AS",
        "desc": "Vi tilbyr vaktmestertjenester for private boliger, borettslag og næringsbygg. Vi er raskt på plass for å utføre jobben når det trengs!",
        "h1": "Vi gjør vedlikeholdet enklere",
        "lead": "Follo Eiendomsservice AS utfører vaktmestertjenester for private boliger, fritidsboliger, borettslag og næringsbygg. Trenger inngangspartiet feiing, takrennene rens eller plenen klipp? Ring oss så gjør vi vedlikeholdet enklere!",
        "card": "Våre vaktmestre har variert og god fagkompetanse og dekker et stort spekter av tjenester. Vi avdekker avvik, utbedrer feil og mangler løpende, har god kontakt med beboerne, styret, forretningsfører og eiere. Kontakt oss i dag, så setter vi opp en avtale!",
        "card_img": "plen",
        "hero_img": "feiemaskin-5",
        "sections": [
            {
                "h2": "Med lidenskap for jobben",
                "text": [
                    "Vi liker jobben vi gjør, og det merkes i arbeidet vi leverer. Enten det gjelder små repetitive oppdrag eller større enkeltjobber, gjør vi en grundig jobb hver gang.",
                ],
                "img": "feiemaskin-1",
            },
            {
                "h2": "Vi har utstyret som trengs",
                "text": [
                    "Oppdrag stoppes ikke av sesong eller størrelse. Våre maskiner og verktøy står klare når snøen faller, når gresset vokser eller når annet vedlikehold må tas. Det gjør at arbeidet kan gjennomføres uten unødvendige forsinkelser.",
                ],
                "img": None,
            },
            {
                "h2": "Fast eller ved engangstilfeller",
                "text": [
                    "Noen eiendommer trenger fast oppfølging gjennom året. Andre har behov som oppstår innimellom. Avtaler kan settes opp som faste oppdrag eller bestilles ved enkeltstående arbeid, alt etter hva bygget krever. Kontakt oss gjerne for å høre hvordan vi kan hjelpe deg.",
                ],
                "img": "feiemaskin-3",
            },
        ],
        "tasks": [
            {"name": "Gressklipping", "img": "plen"},
            {"name": "Feiing og rydding", "img": "feiemaskin-1"},
            {"name": "Bortkjøring av avfall", "img": "avfall"},
            {"name": "Vedlikehold av uteareal", "img": "uteareal"},
            {"name": "Høytrykksspyling", "img": "hoytrykksspyling"},
            {"name": "Skift av lysrør og lyspærer", "img": "lysror"},
            {"name": "Strøing og snømåking", "img": "snofreser"},
            {"name": "Reparasjon av dører, hengsler etc", "img": "dorreparasjon"},
        ],
    },
    {
        "slug": "vintertjenester",
        "name": "Vintertjenester",
        "title": "Vintertjenester | Follo Eiendomsservice AS",
        "desc": "Vi tar oss av brøyting, strøing, manuell måking og fresing. Med godt og riktig utstyr utfører vi arbeidet effektivt og til en rettferdig pris.",
        "h1": "Vintertjenester",
        "lead": "Vi har brøyteberedskap døgnet rundt, alle dager i uka, og tar ansvar for å holde veier, gangveier og parkeringsplasser i orden. Slik blir adkomsten god og trygg for dine beboere.",
        "card": "Vi har brøyteberedskap døgnet rundt, alle dager i uka, og tar ansvar for å holde veier, gangveier og parkeringsplasser i orden. Slik blir adkomsten god og trygg for dine beboere.",
        "card_img": "vinter-traktor",
        "hero_img": "broyting",
        "sections": [
            {
                "h2": "Beredskap 24/7",
                "text": [
                    "Gode rutiner for beredskap er viktig når snøfallet plutselig kommer. Kort utrykningstid og effektiv gjennomføring.",
                ],
                "img": "vinter-traktor",
            },
            {
                "h2": "Vi har utstyret som trengs",
                "text": [
                    "Det er viktig med riktig utstyr for å komme til alle steder. Vi tilpasser oss ditt behov, enten det er maskinell eller manuell måking.",
                ],
                "img": None,
            },
            {
                "h2": "Gratis befaring",
                "text": [
                    "En gjennomgående befaring er viktig for å avklare arbeidsområdet og behov. Vi tilbyr gratis befaring og konkurransedyktige priser.",
                ],
                "img": "snofreser",
            },
        ],
        "tasks": [
            {"name": "Brøyting", "img": "broyting"},
            {"name": "Strøing", "img": "stroebil"},
            {"name": "Håndmåking", "img": "handmaking"},
            {"name": "Bortkjøring av snø", "img": "snobortkjoring"},
            {"name": "Fjerning av istapper", "img": "istapper"},
        ],
    },
    {
        "slug": "feiing-og-spyling",
        "name": "Feiing og spyling",
        "title": "Feiing og spyling | Follo Eiendomsservice AS",
        "desc": "Vi tilbyr feiing og spyling av garasjeanlegg, parkeringsplasser og gangveier slik at uteområdene alltid er velholdt. Kontakt oss for en avtale.",
        "h1": "Feiing og spyling",
        "lead": "Kontakt oss for høytrykksspyling av fasader og fellesareal samt vask av vinduer og søppelkonteinere. Vårt personell har god og variert kompetanse på området.",
        "card": "Kontakt oss for høytrykksspyling av fasader og fellesareal samt vask av vinduer og søppelkonteinere. Vårt personell har god og variert kompetanse på området.",
        "card_img": "feiemaskin-4",
        "hero_img": "feiemaskin-4",
        "sections": [
            {
                "h2": "Få det rent",
                "text": [
                    "Vi feier og spyler garasjeanlegg, parkeringsplasser og gangveier, slik at uteområdene holder seg velholdt. Kontakt oss, så setter vi opp en løsning som passer ditt bygg.",
                ],
                "img": "garasjeanlegg",
            },
            {
                "h2": "Ivareta byggene",
                "text": [
                    "Fasader utsettes for forurensning, mikroorganismer og smuss gjennom året. Fasadevask om våren fjerner belegget som holder på fukt og bryter ned overflaten. Regelmessig vask reduserer slitasje og gjør skader lettere å oppdage.",
                ],
                "img": None,
            },
            {
                "h2": "Vi utfører takvask",
                "text": [
                    "Vi utfører også takvask og fjerner smuss og belegg som bryter ned taket over tid. Riktig utstyr og riktig metode gjør jobben skånsom og effektiv.",
                ],
                "img": "lift-tak",
            },
        ],
        "tasks": [
            {"name": "Vårfeiing", "img": "feiemaskin-5"},
            {"name": "Fasadevask", "img": "fasadevask"},
            {"name": "Spyling av takrenner", "img": "takrennerens"},
            {"name": "Takvask", "img": "lift-tak"},
        ],
    },
    {
        "slug": "garasjevask",
        "name": "Garasjevask",
        "title": "Profesjonell garasjevask for borettslag og næring | Follo Eiendomsservice AS",
        "desc": "Effektiv og skånsom garasjevask til fast pris per parkeringsplass for borettslag, sameier og næring. Prøv priskalkulatoren og få en veiledende pris.",
        "h1": "Profesjonell garasjevask for borettslag og næring",
        "lead": "Vi leverer grundig garasjevask med fast pris per parkeringsplass. Effektiv gjennomføring, skånsom behandling og forutsigbare kostnader.",
        "card": "Grundig garasjevask med fast pris per parkeringsplass for borettslag, sameier og næring.",
        "card_img": "gv-1",
        "hero_img": "gv-hero",
        "sections": [
            {
                "h2": "Profesjonell og effektiv garasjevask",
                "text": [
                    "Vi tilbyr profesjonell og effektiv garasjevask for borettslag, sameier, næringsbygg og gårdsanlegg. Over tid samler garasjeanlegg store mengder sand, støv, eksosrester og forurensning som påvirker både bygg, biler og inneklima.",
                    "Med riktig utstyr og erfaring sørger vi for en grundig rengjøring som gir et synlig og varig resultat, uten unødvendig belastning på betong eller asfalt. Vi jobber strukturert, effektivt og med minst mulig ulempe for brukerne av anlegget.",
                    "En ren garasje forlenger levetiden på betong og asfalt, reduserer slitasje på biler og dekk, gir et tryggere og mer trivelig miljø og et bedre førsteinntrykk for beboere og besøkende.",
                ],
                "img": "gv-1",
            },
            {
                "h2": "Slik utfører vi garasjevask",
                "text": [
                    "Arbeidet starter med grundig grovrengjøring og fjerning av løsmasser. Deretter vaskes gulvene med profesjonell garasjevasker hvor skittent vann suges opp igjen. Dette gir et rent resultat uten at skitt og vann blir liggende igjen i anlegget.",
                    "Metoden er effektiv, skånsom og godt egnet for både betong- og asfaltunderlag. Profesjonell garasjevask gir bedre inneklima og mindre støvspredning, redusert vedlikeholdsbehov, lengre levetid på gulv og overflater og et renere og mer representativt bygg.",
                ],
                "img": "gv-2",
            },
            {
                "h2": "Hvorfor velge profesjonell garasjevask?",
                "text": [
                    "Garasjeanlegg utsettes daglig for sand, fukt, veisalt og eksos. Uten regelmessig vask bygger dette seg opp og fører til økt slitasje på både gulv, konstruksjon og kjøretøy.",
                ],
                "img": None,
            },
        ],
        "pris": {
            "intro": "Garasjevask prises per parkeringsplass, slik at styret enkelt kan beregne kostnadene på forhånd. Én parkeringsplass tilsvarer ca. 25 m². Større anlegg gir lavere pris per plass, og vi tilbyr gunstige avtaler for regelmessig vask.",
            "inngar": [
                "Feiing og grovrengjøring",
                "Fjerning av støv, sand og grus",
                "Vasking med vann som suges opp igjen med garasjevasker",
                "Utstyr og materiell: garasjevasker, kost og feieutstyr, slanger og vanntilkobling",
            ],
            "tabeller": [
                {"navn": "Betongunderlag (1 person)", "rader": [("1–50 plasser", "230 kr"), ("51–150 plasser", "220 kr"), ("151–400 plasser", "205 kr"), ("Over 400 plasser", "Pris på forespørsel")], "min": "Minstepris: 8 500 kr"},
                {"navn": "Asfaltunderlag (2 personer)", "rader": [("1–50 plasser", "270 kr"), ("51–100 plasser", "255 kr"), ("101–200 plasser", "235 kr"), ("Over 200 plasser", "Pris på forespørsel")], "min": "Minstepris: 8 500 kr"},
            ],
            "rabatter": [("2 års binding", "10 %"), ("3 års binding", "15 %"), ("5 års binding", "20 %")],
            "kjoring": "Oppmøte/kjøring: 13 kr per km fra Ås, beregnet én vei.",
        },
        "risiko": [
            "Glatte gulv under og etter vask",
            "Elektriske installasjoner",
            "Eldre betonggulv",
            "Avrenning av skittent vann",
        ],
        "forberedelser": [
            "Garasjen tømmes for løse gjenstander",
            "Tilgang til vann og strøm",
            "Port må kunne stå åpen under vask",
        ],
        "tasks": [
            {"name": "Feiing av garasjeanlegg", "img": "feiemaskin-5"},
            {"name": "Garasjevask på betong", "img": "garasjevask"},
            {"name": "Garasjevask på asfalt", "img": "garasjeanlegg"},
        ],
    },
    {
        "slug": "gartner-og-grontareal",
        "name": "Gartner og grøntareal",
        "title": "Gartner og grøntareal | Follo Eiendomsservice AS",
        "desc": "Trenger hekken en stuss? Har du et tre som er til sjenanse for naboene? På tide å stelle plenen? Vi gjør små og store anleggsgartneroppdrag.",
        "h1": "Vi tar oss av utearealet ditt",
        "lead": "Av oss får du utført plen- og kantklipping, utplanting, fjerning av ugress, beskjæring samt stell av busker.",
        "card": "Av oss får du utført plen- og kantklipping, utplanting, fjerning av ugress, beskjæring samt stell av busker.",
        "card_img": "hekkeklipping",
        "hero_img": "hekkeklipping",
        "sections": [
            {
                "h2": "Vi tar ansvar for å gjøre jobben",
                "text": [
                    "Gjennom flere år har vi opparbeidet både små hager og større uteområder for private og borettslag. Vi legger plen, planter hekker og bygger opp områder fra grunnen av. Arbeidet planlegges og gjennomføres i tråd med det du ønsker deg.",
                ],
                "img": "ferdigplen",
            },
            {
                "h2": "Lang erfaring",
                "text": [
                    "Vi har lang erfaring med anleggsgartnerarbeid, fra små hager til større uteområder. Du får hjelp til både planlegging og gjennomføring.",
                ],
                "img": None,
            },
            {
                "h2": "Ingen mellomledd",
                "text": [
                    "Vi importerer planter direkte uten fordyrende mellomledd. Det gir oss bedre kontroll på kvalitet og levering, og gjør det mulig å tilby fordelaktige priser til våre kunder, på både små og større beplantningsprosjekter.",
                ],
                "img": "planter",
            },
        ],
        "tasks": [
            {"name": "Beplantning", "img": "utplanting"},
            {"name": "Etablering av hekk", "img": "hekk"},
            {"name": "Beskjæring av hekk og trær", "img": "hekkeklipping"},
            {"name": "Trefelling", "img": "trefelling-motorsag"},
            {"name": "Legging av plen", "img": "ferdigplen"},
            {"name": "Luking og stell etc", "img": "planter"},
        ],
    },
    {
        "slug": "renhold",
        "name": "Renhold",
        "title": "Renhold for borettslag og bedrifter",
        "desc": "Vi utfører profesjonelt renhold på fast basis eller engangsbasis. Vi har lang erfaring og vet hva som gir et flunkende rent resultat.",
        "h1": "Renhold for borettslag og bedrifter",
        "lead": "Enten du ønsker en fast renholdsavtale eller engangsrenhold, hjelper vi bedrifter og borettslag med et rent og hygienisk uttrykk.",
        "card": "Enten du ønsker en fast renholdsavtale eller engangsrenhold, hjelper vi bedrifter og borettslag med et rent og hygienisk uttrykk.",
        "card_img": "renhold-mopp",
        "hero_img": "renhold-trapp",
        "sections": [
            {
                "h2": "Fast renhold",
                "text": [
                    "Follo Eiendomsservice AS leverer fast renhold for en rekke bedrifter og borettslag i Follo. Vi kan tilby renhold ukentlig, månedlig eller etter intervallet du måtte ønske.",
                    "- Kontorvask",
                    "- Vask av kantine og kjøkken",
                    "- Trappevask",
                    "- Vindusvask",
                    "- Fasadevask",
                ],
                "img": "renhold-flater",
            },
            {
                "h2": "Engangsrenhold (flyttevask og nedvasking)",
                "text": [
                    "Trenger du et renholdsfirma til å hjelpe deg med flyttevask, nedvasking av et lokale eller annet engangsrenhold? Vi er rett partner for jobben!",
                ],
                "img": None,
            },
        ],
        "tasks": [
            {"name": "Kontorvask", "img": "stovsuging"},
            {"name": "Vask av kantine og kjøkken", "img": "kantine"},
            {"name": "Trappevask", "img": "renhold-mopp"},
            {"name": "Vindusvask", "img": "vindusvask"},
            {"name": "Fasadevask", "img": "fasadevask"},
            {"name": "Flyttevask", "img": "vask-servant"},
            {"name": "Nedvasking av lokale", "img": "kontorlandskap"},
        ],
    },
    {
        "slug": "hms-brannsikring-kontroll-av-lekeplasser",
        "name": "HMS",
        "title": "Brannsikring og lekeplasskontroll | Follo Eiendomsservice AS",
        "desc": "Kontroll av rømningsveier, røykvarslere og pulverapparater. Vi har fagfolk som kontrollerer utstyret og utfører service på det.",
        "h1": "HMS (brannsikring og kontroll av lekeplass)",
        "lead": "Brannsikkerhet i bygg krever jevnlig oppfølging. Follo Eiendomsservice AS kontrollerer rømningsveier, røykvarslere og pulverapparater, og hjelper med planer for evakuering ved brann. Utstyret gjennomgås og vedlikeholdes av fagfolk.",
        "card": "Follo Eiendomsservice AS utfører kontroll av rømningsveier, røykvarslere og pulverapparater. Våre fagfolk kontrollerer utstyret og utfører service.",
        "card_img": "lekeplass",
        "hero_img": "brannslukker",
        "sections": [
            {
                "h2": "Vi kan hjelpe deg med brannsikring og kontroll av lekeplasser",
                "text": [
                    "Vi kontrollerer rømningsveier, røykvarslere og pulverapparater, og utfører service slik at utstyret er klart hvis det skjer noe. Vi gjennomfører også kontroll av lekeplasser, slik at de er trygge å bruke.",
                ],
                "img": "brannslukker",
            },
        ],
        "tasks": [
            {"name": "Brannsikring", "img": "brannslukker"},
            {"name": "Lekeplasskontroll", "img": "lekeplass"},
        ],
    },
    {
        "slug": "matteutleie",
        "name": "Matteutleie",
        "title": "Høykvalitets matter | Follo Eiendomsservice AS",
        "desc": "Driver du et bygg eller et lokale som utsettes for mye trafikk i løpet av en dag? Matter til bedrifter, borettslag, butikker og restauranter.",
        "h1": "Høykvalitets-matter for et flott inngangsparti",
        "lead": "Trenger du matter? Vi leier ut matter for inngangsparti i borettslag, butikker og andre lokaler med mye trafikk.",
        "card": "Trenger du matter? Vi leier ut matter for inngangsparti i borettslag, butikker og andre lokaler med mye trafikk.",
        "card_img": "matte-brun",
        "hero_img": "kontor",
        "sections": [
            {
                "h2": "Renere lokaler",
                "text": [
                    "Mattene samler opp skitt og fuktighet fra skoene, slik at inngangspartiet holder seg renere lenger. Det gir mindre søle og mindre behov for vask i resten av lokalet.",
                ],
                "img": "kontorlandskap",
            },
            {
                "h2": "Gir et godt førsteinntrykk",
                "text": [
                    "En heldekkende matte ved inngangen gir besøkende et ryddig og profesjonelt førsteinntrykk. Det er en enkel måte å holde lokalet presentabelt på.",
                ],
                "img": None,
            },
            {
                "h2": "Trygt og sikkert",
                "text": [
                    "Mattene er såpass tunge at de ligger godt på bakken. Dette gjør at du slipper skumle kanter som stikker opp, eller at matten glir unna. Matten suger opp fuktighet fra skoene til de besøkende og kan dermed forhindre skliulykker.",
                ],
                "img": "matte-brun",
            },
            {
                "h2": "Matteutleie fra Leko",
                "text": [
                    "Les mer om matteutleie hos vår samarbeidspartner: https://www.leko.no/matteutleie/",
                ],
                "img": None,
            },
        ],
        "tasks": [
            {"name": "Matter for bedrifter", "img": "matte-heis"},
            {"name": "Matter for borettslag", "img": "matte-svart"},
            {"name": "Matter for butikker", "img": "matte-inngang"},
            {"name": "Matter for restauranter", "img": "matte-rod"},
        ],
    },
    {
        "slug": "salg-av-bjorkeved",
        "name": "Salg av bjørkeved",
        "card": "Vi selger og leverer bjørkeved hjem til deg samt tilbyr bæring av veden dit du ønsker.",
        "card_img": "bjorkeved-levering",
    },
    {
        "slug": "trefelling",
        "name": "Trefelling",
        "title": "Trefelling | Follo Eiendomsservice AS",
        "desc": "Vi utfører trefelling for private, borettslag og næringsdrivende. Fellingen planlegges ut fra plassering, høyde og forholdene rundt treet.",
        "h1": "Trefelling",
        "lead": "Et tre kan bli for stort, stå for tett på bygninger eller være skadet etter vær og vind. Follo Eiendomsservice AS utfører trefelling for private, borettslag og næringsdrivende. Trefellingen planlegges alltid ut fra plassering, høyde og forholdene rundt treet, slik at fellingen kan gjennomføres på en trygg måte.",
        "card": "Follo Eiendomsservice AS utfører trefelling for private, borettslag og næringsdrivende.",
        "card_img": "trefelling-1",
        "hero_img": "trefelling-1",
        "sections": [
            {
                "h2": "Felling der det er liten plass",
                "text": [
                    "Selv der det er liten plass, finner vi en trygg måte å felles treet på. Fellingen planlegges alltid ut fra plasseringen og forholdene rundt treet.",
                ],
                "img": "trefelling-2",
            },
            {
                "h2": "Opprydding etter trefelling",
                "text": [
                    "Etter fellingen kan stammer, greiner og kvist kjøres bort, om du ønsker det. Vil du beholde veden eller få den kappet opp? Det er heller ikke noe problem, og vi hjelper deg gjerne med det også.",
                ],
                "img": None,
            },
            {
                "h2": "Fjerning av trær som står i veien",
                "text": [
                    "Vi fjerner trær som står for tett på bygninger, er skadet eller er til sjenanse for naboene. Ta kontakt, så ser vi på hva som trengs hos deg.",
                ],
                "img": "trefelling-3",
            },
        ],
        "tasks": [],
    },
]

REFERENCES = [
    {
        "name": "Peder Aaling",
        "role": "Styreleder i borettslag",
        "quote": [
            "Vi bruker Follo Eiendomsservice AS til vaktmestertjenester og renhold. De er profesjonelle og kan sine saker. De har hjulpet oss med gartnerarbeid, klipping av hekk, måking av snø og strøing.",
            "Vi og våre beboere er veldig fornøyde med servicen vi har fått!",
        ],
    },
    {
        "name": "Vegard Thomassen",
        "role": "Styreleder i borettslag",
        "quote": [
            "De oppgavene som Follo Eiendomsservice har tatt seg av har vi vært veldig fornøyde med. Det å ha en kontaktperson som er «vår» og som vi kan ringe når vi trenger hjelp, er helt nydelig.",
            "Vi har fått hjelp til alt fra enkle vedlikeholdsoppgaver til snømåking og renholdsoppgaver som trappevask. Vi har valgt Follo Eiendomsservice for en lengre avtale, og det har vi ikke angret på et sekund. Dersom du er ute etter en vaktmester som tar seg av alt, er dette de rette folka.",
        ],
    },
]

ABOUT = {
    "h1": "Om oss",
    "lead": "Tidligere Min Eiendomsservice AS har nå byttet navn til Follo Eiendomsservice AS. Vi leverer vaktmester- og vedlikeholdstjenester til privatpersoner, borettslag og bedrifter i Follo og nærliggende områder.",
    "text": [
        "Tidligere Min Eiendomsservice AS har nå byttet navn til Follo Eiendomsservice AS! Vårt mål er å levere vaktmester- og vedlikeholdstjenester til privatpersoner, borettslag og bedrifter, med hovedfokus på Follo og nærliggende områder. Dette er vårt satsingsområde.",
        "Vi legger vår stolthet i å levere kvalitetsarbeid hver gang!",
    ],
}
