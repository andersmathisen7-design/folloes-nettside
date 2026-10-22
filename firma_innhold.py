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
        "Garasjevask – fast pris per parkeringsplass.",
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
        "title": "Vaktmester for borettslag og bedrifter i Follo",
        "desc": "Vi tilbyr vaktmestertjenester for private boliger, borettslag og næringsbygg. Vi er raskt på plass for å utføre jobben når det trengs!",
        "faq": [
            ("Hva gjør en vaktmester for borettslag og bedrifter i Follo?", "Vi tar blant annet gressklipping, feiing og rydding, bortkjøring av avfall, vedlikehold av uteareal, høytrykksspyling, skift av lysrør og lyspærer, strøing og snømåking og enkle reparasjoner av dører og hengsler."),
            ("Tilbyr dere vaktmestertjenester for private boliger i Ås?", "Ja. Vi holder til i Ås og tar oppdrag for privatpersoner, borettslag og bedrifter i hele Follo, også fritidsboliger og næringsbygg."),
            ("Kan vi få fast vaktmesteravtale, eller bare enkeltoppdrag?", "Begge deler går bra. Noen eiendommer trenger fast oppfølging gjennom året, andre bestiller når behovet oppstår."),
            ("Hva koster en vaktmester?", "Prisen avhenger av hva som skal gjøres, hvor ofte og hvor stor eiendommen er. Ring 48 99 39 00 for et uforpliktende tilbud."),
            ("Hvilke steder i Follo dekker dere?", "Vi arbeider i Ås, Nordre Follo, Nesodden, Vestby, Frogn og Enebakk."),
        ],
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
        "title": "Brøyting og snømåking i Ås og Follo",
        "desc": "Brøyting, strøing, snømåking og fresing i Ås og resten av Follo, for private, borettslag og bedrifter. Brøyteberedskap døgnet rundt.",
        "faq": [
            ("Brøyter dere for privatpersoner i Ås?", "Ja. Vi tar oppdrag for privatpersoner, borettslag og bedrifter i Ås og resten av Follo."),
            ("Hva omfatter vintertjenestene deres?", "Vi tar oss av brøyting, strøing, håndmåking, bortkjøring av snø og fjerning av istapper, med maskinelt eller manuelt utstyr etter behov."),
            ("Har dere brøyteberedskap når snøen kommer?", "Ja, vi har brøyteberedskap døgnet rundt, alle dager i uka, slik at veier, gangveier og parkeringsplasser holdes i orden."),
            ("Kan vi ha fast brøyteavtale for borettslaget?", "Ja. Vi tilbyr fast avtale eller enkeltoppdrag, alt etter hva eiendommen trenger."),
            ("Hva koster brøyting?", "Prisen avhenger av arbeidsområdet og behovet, for eksempel størrelsen på området og om det skal måkes maskinelt eller for hånd. Ring 48 99 39 00 for et uforpliktende tilbud."),
        ],
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
        "title": "Feiing og spyling av garasjeanlegg i Follo",
        "desc": "Vi tilbyr feiing og spyling av garasjeanlegg, parkeringsplasser og gangveier slik at uteområdene alltid er velholdt. Kontakt oss for en avtale.",
        "faq": [
            ("Hva er vårfeiing?", "Vårfeiing er feiing av utearealer som garasjeanlegg, parkeringsplasser og gangveier etter vinteren, slik at uteområdene blir velholdt."),
            ("Spyler dere garasjeanlegg og parkeringsplasser for borettslag?", "Ja. Vi feier og spyler garasjeanlegg, parkeringsplasser og gangveier for borettslag, bedrifter og andre i Follo."),
            ("Hvorfor bør fasaden vaskes?", "Fasader utsettes for forurensning, mikroorganismer og smuss. Fasadevask om våren fjerner belegget som holder på fukt og bryter ned overflaten."),
            ("Utfører dere takvask og spyling av takrenner?", "Ja. Vi utfører takvask og spyler takrenner, og bruker utstyr og metode som er skånsom mot taket."),
            ("Hva koster feiing og spyling?", "Prisen avhenger av type jobb og størrelsen på området eller bygget. Ring 48 99 39 00 for et uforpliktende tilbud."),
        ],
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
            {"name": "Garasjevask", "img": "garasjeanlegg", "href": "/garasjevask/"},
            {"name": "Fasadevask", "img": "fasadevask"},
            {"name": "Spyling av takrenner", "img": "takrennerens"},
            {"name": "Takvask", "img": "lift-tak"},
        ],
    },
    {
        "slug": "gartner-og-grontareal",
        "name": "Gartner og grøntareal",
        "title": "Gartner og grøntareal i Ås og Follo",
        "desc": "Hekk, plen, beskjæring og nye uteområder. Vi gjør små og store anleggsgartneroppdrag for private og borettslag i Ås og resten av Follo.",
        "faq": [
            ("Hva gjør en anleggsgartner?", "Vi legger plen, planter hekker, beplanter og bygger opp uteområder fra grunnen av. Vi tar også plen- og kantklipping, beskjæring, fjerning av ugress og stell av busker."),
            ("Kan dere klippe hekken og beskjære trær?", "Ja. Vi beskjærer hekker og trær, og tar også trefelling om treet må ned."),
            ("Tar dere oppdrag for private hager i Ås og Follo?", "Ja. Vi gjør små og store oppdrag, fra små hager til større uteområder, for privatpersoner og borettslag i hele Follo."),
            ("Kan dere legge ny plen?", "Ja. Vi legger ferdigplen og hjelper med planlegging og gjennomføring slik du ønsker det."),
            ("Hva koster gartnerarbeid?", "Prisen avhenger av hva som skal gjøres og hvor stort området er. Ring 48 99 39 00 for et uforpliktende tilbud."),
        ],
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
        "title": "Renhold for borettslag og bedrifter i Follo",
        "desc": "Vi utfører profesjonelt renhold på fast basis eller engangsbasis. Vi har lang erfaring og vet hva som gir et flunkende rent resultat.",
        "faq": [
            ("Tilbyr dere renhold for bedrifter og borettslag i Follo?", "Ja. Vi leverer fast renhold for en rekke bedrifter og borettslag i Follo, blant annet kontorvask, trappevask og vindusvask."),
            ("Kan vi få renhold ukentlig eller månedlig?", "Ja. Vi kan tilby renhold ukentlig, månedlig eller etter intervallet du ønsker."),
            ("Tar dere flyttevask?", "Ja. Vi utfører flyttevask, nedvasking av lokaler og annet engangsrenhold."),
            ("Vasker dere kantine og kjøkken?", "Ja. Vask av kantine og kjøkken er en del av det faste renholdet vårt, sammen med kontorvask og fasadevask."),
            ("Hva koster renhold?", "Prisen avhenger av type renhold, størrelsen på lokalet og hvor ofte det skal vaskes. Ring 48 99 39 00 for et uforpliktende tilbud."),
        ],
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
        "title": "Brannsikring og lekeplasskontroll i Follo",
        "desc": "Kontroll av rømningsveier, røykvarslere og pulverapparater. Vi har fagfolk som kontrollerer utstyret og utfører service på det.",
        "faq": [
            ("Hva kontrollerer dere av brannsikring?", "Vi kontrollerer rømningsveier, røykvarslere og pulverapparater, og utfører service på utstyret."),
            ("Kan dere kontrollere lekeplassen til borettslaget?", "Ja. Vi gjennomfører kontroll av lekeplasser, slik at de er trygge å bruke."),
            ("Hjelper dere med evakueringsplaner ved brann?", "Ja. Vi hjelper med planer for evakuering ved brann."),
            ("Hvem utfører kontrollen?", "Utstyret gjennomgås og vedlikeholdes av fagfolk fra Follo Eiendomsservice AS."),
            ("Hva koster brannsikring og lekeplasskontroll?", "Prisen avhenger av størrelsen på bygget eller lekeplassen og hvor mye utstyr som skal kontrolleres. Ring 48 99 39 00 for et uforpliktende tilbud."),
        ],
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
        "title": "Matteutleie og inngangsmatter i Follo",
        "desc": "Leie av inngangsmatter til bedrifter, borettslag, butikker og restauranter i Follo. Mattene holder skitt og fukt ute og hindrer skliulykker.",
        "faq": [
            ("Leier dere ut matter til bedrifter og borettslag?", "Ja. Vi leier ut matter for inngangsparti til bedrifter, borettslag, butikker og restauranter i Follo."),
            ("Hvorfor bør man ha matte i inngangspartiet?", "Mattene samler opp skitt og fuktighet fra skoene. Da holder inngangspartiet seg renere lenger, og det blir mindre behov for vask i resten av lokalet."),
            ("Kan matter hindre skliulykker?", "Matten suger opp fuktighet fra skoene og kan dermed forhindre skliulykker. Mattene er tunge nok til å ligge godt på bakken."),
            ("Hvem leverer mattene?", "Vi samarbeider med Leko om matteutleie. Les mer på leko.no/matteutleie."),
            ("Hva koster det å leie matte?", "Prisen avhenger av antall matter og størrelsen på inngangspartiet. Ring 48 99 39 00 for et uforpliktende tilbud."),
        ],
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
        "title": "Trefelling i Ås og Follo, også der det er trangt",
        "desc": "Trefelling for private, borettslag og næring i Ås og Follo. Vi feller trygt også der det er liten plass, og kan kjøre bort eller kappe veden.",
        "faq": [
            ("Kan dere felle trær på små tomter i Ås?", "Ja. Selv der det er liten plass, finner vi en trygg måte å felle treet på."),
            ("Hvordan planlegger dere trefelling?", "Fellingen planlegges ut fra plassering, høyde og forholdene rundt treet, slik at den kan gjennomføres trygt."),
            ("Tar dere trefelling for borettslag og bedrifter?", "Ja. Vi utfører trefelling for privatpersoner, borettslag og næringsdrivende i hele Follo."),
            ("Når bør et tre felles?", "Et tre kan bli for stort, stå for tett på bygninger eller være skadet etter vær og vind. Ta kontakt, så vurderer vi hva som er best."),
            ("Hva koster trefelling?", "Prisen avhenger av treets plassering og høyde og forholdene rundt det. Ring 48 99 39 00 for et uforpliktende tilbud."),
        ],
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

# Garasjevask er en egen del av nettstedet, som bjørkeved (ikke blant tjenestene).
GARASJEVASK_SIDE = {
    "slug": "garasjevask",
    "name": "Garasjevask",
    "title": "Garasjevask for borettslag og næring | Follo Eiendomsservice AS",
    "desc": "Profesjonell garasjevask for borettslag, sameier og næringsbygg i Follo. Fast pris per parkeringsplass, og en priskalkulator som gir deg en veiledende pris med en gang.",
    "h1": "Profesjonell garasjevask for borettslag og næring",
    "lead": "Vi leverer grundig garasjevask med fast pris per parkeringsplass. Effektiv gjennomføring, skånsom behandling og forutsigbare kostnader.",
    "card": "Grundig vask av garasjeanlegg for borettslag, sameier og næringsbygg, med fast pris per parkeringsplass. Regn ut en veiledende pris med en gang.",
    "card_img": "garasjevask",
    "hero_img": "garasjevask",
    "sections": [
        {
            "h2": "Profesjonell og effektiv garasjevask",
            "text": [
                "Vi tilbyr profesjonell og effektiv garasjevask for borettslag, sameier, næringsbygg og gårdsanlegg. Over tid samler garasjeanlegg store mengder sand, støv, eksosrester og forurensning som påvirker både bygg, biler og inneklima.",
                "Med riktig utstyr og erfaring sørger vi for en grundig rengjøring som gir et synlig og varig resultat, uten unødvendig belastning på betong eller asfalt. Vi jobber strukturert, effektivt og med minst mulig ulempe for dem som bruker anlegget.",
                "- Forlenger levetiden på betong og asfalt",
                "- Reduserer slitasje på biler og dekk",
                "- Gir et tryggere og mer trivelig miljø",
                "- Gir et bedre førsteinntrykk for beboere og besøkende",
            ],
            "img": "garasjeanlegg",
        },
        {
            "h2": "Slik utfører vi garasjevasken",
            "text": [
                "Arbeidet starter med grundig grovrengjøring og fjerning av løsmasser. Deretter vaskes gulvene med en profesjonell garasjevasker som suger opp det skitne vannet igjen. Da blir verken skitt eller vann liggende igjen i anlegget.",
                "Metoden er effektiv, skånsom og passer for både betong og asfalt.",
                "- Bedre inneklima og mindre støv",
                "- Mindre behov for vedlikehold",
                "- Lengre levetid på gulv og overflater",
                "- Et renere og mer representativt bygg",
            ],
            "img": "garasjevask",
        },
        {
            "h2": "Hvorfor velge profesjonell garasjevask?",
            "text": [
                "Garasjeanlegg utsettes hver dag for sand, fukt, veisalt og eksos. Uten jevnlig vask bygger dette seg opp og gir økt slitasje på gulv, konstruksjon og kjøretøy.",
            ],
            "img": None,
        },
    ],
    "tasks": [],
}

# Garasjevask: priser og kalkulator (fra garasjevasken.no, oktober 2026).
# Tabellene på /garasjevask/ og priskalkulatoren bruker de samme tallene.
GARASJEVASK = {
    "m2_per_plass": 25,
    "minstepris": 8500,
    "km_pris": 13,  # per km fra Ås, én vei
    "underlag": [
        {"id": "betong", "name": "Betongunderlag", "who": "1 person",
         # (til og med antall plasser, pris per plass); over siste grense: pris på forespørsel
         "tiers": [(50, 230), (150, 220), (400, 205)]},
        {"id": "asfalt", "name": "Asfaltunderlag", "who": "2 personer",
         "tiers": [(50, 270), (100, 255), (200, 235)]},
    ],
    "binding": [(0, 0), (2, 10), (3, 15), (5, 20)],  # (år, rabatt i prosent)
    "inngar": [
        "Feiing og grovrengjøring",
        "Fjerning av støv, sand og grus",
        "Vask med vann som suges opp igjen med garasjevasker",
    ],
    "utstyr": ["Garasjevasker", "Kost og feieutstyr", "Slanger og vanntilkobling"],
    "risiko": [
        "Glatte gulv under og etter vask",
        "Elektriske installasjoner",
        "Eldre betonggulv",
        "Avrenning av skittent vann",
    ],
    "forberedelser": [
        "Garasjen tømmes for løse gjenstander",
        "Tilgang til vann og strøm",
        "Porten må kunne stå åpen under vask",
    ],
}
