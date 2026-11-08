-- Databasen for folloes.no: vedbestillinger, henvendelser fra kontaktskjemaet og innlogging til eiersiden.

-- Vedbestillinger. Samme felt som kolonnene i det gamle regnearket «Bestillinger».
CREATE TABLE bestillinger (
  id         TEXT PRIMARY KEY,
  dato       TEXT NOT NULL,              -- leveringsdag, ÅÅÅÅ-MM-DD
  minutter   INTEGER NOT NULL DEFAULT 0, -- beregnet tid (kjøring, lossing og bæring) fra skjemaet eller eieren
  status     TEXT NOT NULL DEFAULT 'Ny', -- Ny, Bekreftet, Levert, Avbestilt
  navn       TEXT NOT NULL DEFAULT '',
  telefon    TEXT NOT NULL DEFAULT '',
  adresse    TEXT NOT NULL DEFAULT '',
  omrade     TEXT NOT NULL DEFAULT '',
  sekker     INTEGER NOT NULL DEFAULT 0,
  baering    TEXT NOT NULL DEFAULT '',
  totalpris  TEXT NOT NULL DEFAULT '',
  epost      TEXT NOT NULL DEFAULT '',
  melding    TEXT NOT NULL DEFAULT '',
  hyppighet  TEXT NOT NULL DEFAULT '',   -- vedabonnement, f.eks. «Fast levering hver 4. uke»
  registrert TEXT NOT NULL,              -- ÅÅÅÅ-MM-DD TT:MM (norsk tid)
  lossetid   REAL,                       -- lossing og bæring i minutter (uten kjøring)
  lat        REAL,
  lon        REAL,
  fast       INTEGER NOT NULL DEFAULT 0, -- 1 = eieren har satt minuttene selv, ikke med i ruteberegningen
  betalt     INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX bestillinger_dato ON bestillinger (dato);

-- Henvendelser fra kontaktskjemaet på firmasidene (også garasjevask).
CREATE TABLE henvendelser (
  id         TEXT PRIMARY KEY,
  registrert TEXT NOT NULL,
  gjelder    TEXT NOT NULL DEFAULT '',
  navn       TEXT NOT NULL DEFAULT '',
  telefon    TEXT NOT NULL DEFAULT '',
  epost      TEXT NOT NULL DEFAULT '',
  melding    TEXT NOT NULL DEFAULT '',
  side       TEXT NOT NULL DEFAULT '',
  status     TEXT NOT NULL DEFAULT 'Ny'  -- Ny, Besvart, Arkivert
);
CREATE INDEX henvendelser_registrert ON henvendelser (registrert);

-- Dager eieren har satt som fulle.
CREATE TABLE fulle_dager (dato TEXT PRIMARY KEY);

-- Innloggingsbilletter til eiersiden. Bare sjekksummen lagres.
CREATE TABLE billetter (hash TEXT PRIMARY KEY, utloper INTEGER NOT NULL);

-- Passordet til eiersiden (salt og PBKDF2-sjekksum). Settes med «npm run passord».
CREATE TABLE innstillinger (nokkel TEXT PRIMARY KEY, verdi TEXT NOT NULL);

-- Tellere for vern mot misbruk (feil passord, mange bestillinger), og svar fra Kartverket og OSRM.
CREATE TABLE teller (nokkel TEXT PRIMARY KEY, verdi INTEGER NOT NULL, utloper INTEGER NOT NULL);
CREATE TABLE cache (nokkel TEXT PRIMARY KEY, verdi TEXT NOT NULL, utloper INTEGER NOT NULL);
