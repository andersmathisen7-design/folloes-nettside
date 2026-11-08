/**
 * Serveren for folloes.no (Cloudflare Worker med D1-database). Erstatter leveringskalenderen i Google-regnearket
 * (kalender/kalender.gs) og svarer på de samme forespørslene, så bestillingsskjemaet og eiersiden virker som før.
 *
 *  - GET  /                          bestilt tid per leveringsdag og fulle dager (ingen kundedata)
 *  - POST /  { date, minutes, … }    ny vedbestilling fra nettsiden
 *  - POST /  { action: "ledig" }     hvilke dager en bestilling til en adresse får plass
 *  - POST /  { action: "henvendelse" }  kontaktskjemaet på firmasidene (også garasjevask)
 *  - POST /  { action: "login" | "logout" | "list" | "status" | "add" | "full" | "sacks" | "dato"
 *              | "henvendelser" | "henvendelse-status", token }   eiersiden
 *
 * Sikkerhet (som før):
 *  - Passordet lagres bare som salt + PBKDF2-sjekksum. Innloggingen gir en tilfeldig billett som utløper
 *    (12 timer, eller 30 dager med «husk meg»). Maks 10 feil passord per 15 minutter.
 *  - Uten innlogging får man bare vite minutter per dag og om en adresse får plass. Aldri kundedata.
 *  - Nettbestillinger bare for leveringsdager de neste 6 ukene, og maks 30 per time. Henvendelser maks 30 per time.
 *  - Kunden får bare en fast bekreftelsestekst med verdier vi har kontrollert, aldri fritekst fra skjemaet.
 *
 * Innstillinger i wrangler.toml ([vars]) og hemmeligheten RESEND_API_KEY (e-post via resend.com).
 */

export const TIDSSONE = "Europe/Oslo";
export const STATUSER = ["Ny", "Bekreftet", "Levert", "Avbestilt"];
export const HENV_STATUSER = ["Ny", "Besvart", "Arkivert"];
const MAKS_DAGER_FRAM = 42;
const MAKS_NETTBESTILLINGER_PER_TIME = 30;
const MAKS_HENVENDELSER_PER_TIME = 30;
const MAKS_LEDIG_SJEKK_PER_TIME = 600;
const MAKS_FEIL_PASSORD = 10;
const BILLETT_TIMER = 12, BILLETT_HUSK_DAGER = 30;

export const LAGER = { lat: 59.68112, lon: 10.74194 };   // Smebølveien 3, 1433 Ås
const RUTE_TILLEGG = 1.2;                                // OSRM regner med personbil; lastebil med ved går saktere
const LOSSING = 10, BAERING_PER_SEKK = 0.5;              // bare for gamle bestillinger uten lossetid
const KOMMUNE = { "Ås": "3218", "Ski og Langhus": "3207", "Kolbotn og Oppegård": "3207", "Vestby og Son": "3216",
                  "Drøbak": "3214", "Nesodden": "3212", "Enebakk": "3220" };
const FOLLO = ["3207", "3212", "3214", "3216", "3218", "3220"];
const MAKS_PUNKTER = 100;
const PBKDF2_RUNDER = 100000;

// ------------------------------------------------------------------ hjelpere

export function idag(na = new Date()) {
  return new Intl.DateTimeFormat("sv-SE", { timeZone: TIDSSONE, year: "numeric", month: "2-digit", day: "2-digit" }).format(na);
}
function naTekst(na = new Date()) {
  return new Intl.DateTimeFormat("sv-SE", { timeZone: TIDSSONE, year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", hour12: false }).format(na).replace(",", "");
}
export function leggTilDager(iso, n) {
  const d = new Date(iso + "T12:00:00Z");
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}
const ISO = /^\d{4}-\d{2}-\d{2}$/;
const gyldigDato = (s) => ISO.test(s) && !isNaN(new Date(s + "T12:00:00Z").getTime());

// Tekst fra nettsiden: uten kontrolltegn, og kortet ned.
export function tekst(v, max) {
  return String(v == null ? "" : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "").slice(0, max);
}
// Én linje, uten linjeskift (så tekst fra nettsiden aldri kan lage ekstra e-posthoder).
export function linje(v, max) { return tekst(String(v == null ? "" : v).replace(/[\r\n]+/g, " "), max); }
const num = (v) => (v === "" || v == null || isNaN(Number(v)) ? null : Number(v));

async function sha256(s) {
  const b = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("");
}
export async function pbkdf2(passord, salt, runder = PBKDF2_RUNDER) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(passord), "PBKDF2", false, ["deriveBits"]);
  const bits = await crypto.subtle.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: new TextEncoder().encode(salt), iterations: runder }, key, 256);
  return [...new Uint8Array(bits)].map((x) => x.toString(16).padStart(2, "0")).join("");
}
// Sammenligning som tar like lang tid uansett hvor tidlig strengene er ulike.
function likt(a, b) {
  a = String(a); b = String(b);
  let diff = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}
const tilfeldig = (n) => [...crypto.getRandomValues(new Uint8Array(n))].map((x) => x.toString(16).padStart(2, "0")).join("");

// Teller som nullstilles etter ttl sekunder. Gir verdien før økningen.
async function tell(db, nokkel, ttl, ok = true) {
  const na = Date.now();
  const r = await db.prepare("SELECT verdi, utloper FROM teller WHERE nokkel = ?").bind(nokkel).first();
  const verdi = r && r.utloper > na ? r.verdi : 0;
  if (ok) {
    await db.prepare("INSERT INTO teller (nokkel, verdi, utloper) VALUES (?, ?, ?) ON CONFLICT (nokkel) DO UPDATE SET verdi = excluded.verdi, utloper = excluded.utloper")
      .bind(nokkel, verdi + 1, r && r.utloper > na ? r.utloper : na + ttl * 1000).run();
  }
  return verdi;
}
async function lesTeller(db, nokkel) { return tell(db, nokkel, 0, false); }

async function cacheHent(db, nokkel) {
  const r = await db.prepare("SELECT verdi, utloper FROM cache WHERE nokkel = ?").bind(nokkel).first();
  return r && r.utloper > Date.now() ? r.verdi : null;
}
async function cacheLagre(db, nokkel, verdi, ttl) {
  await db.prepare("INSERT INTO cache (nokkel, verdi, utloper) VALUES (?, ?, ?) ON CONFLICT (nokkel) DO UPDATE SET verdi = excluded.verdi, utloper = excluded.utloper")
    .bind(nokkel, verdi, Date.now() + ttl * 1000).run();
}

// ------------------------------------------------------------------ innlogging

async function loggInn(db, passord, husk) {
  const rader = await db.prepare("SELECT nokkel, verdi FROM innstillinger WHERE nokkel IN ('pw_salt', 'pw_hash')").all();
  const inn = Object.fromEntries(rader.results.map((r) => [r.nokkel, r.verdi]));
  if (!inn.pw_salt || !inn.pw_hash) return { ok: false, error: "ikke-satt-opp" };
  if ((await lesTeller(db, "feil_passord")) >= MAKS_FEIL_PASSORD) return { ok: false, error: "sperret" };
  if (!likt(await pbkdf2(String(passord || ""), inn.pw_salt), inn.pw_hash)) {
    await tell(db, "feil_passord", 15 * 60);
    return { ok: false, error: "passord" };
  }
  const na = Date.now();
  await db.prepare("DELETE FROM billetter WHERE utloper < ?").bind(na).run();
  const billett = tilfeldig(32);
  const utloper = na + (husk ? BILLETT_HUSK_DAGER * 864e5 : BILLETT_TIMER * 36e5);
  await db.prepare("INSERT INTO billetter (hash, utloper) VALUES (?, ?)").bind(await sha256(billett), utloper).run();
  return { ok: true, token: billett, expires: utloper };
}
async function gyldigBillett(db, billett) {
  if (!billett || String(billett).length < 40) return false;
  const r = await db.prepare("SELECT utloper FROM billetter WHERE hash = ?").bind(await sha256(String(billett))).first();
  return !!r && r.utloper > Date.now();
}
async function loggUt(db, billett) {
  if (billett) await db.prepare("DELETE FROM billetter WHERE hash = ?").bind(await sha256(String(billett))).run();
}

// ------------------------------------------------------------------ bestillinger

// Raden fra databasen, i samme form som eiersiden fikk fra regnearket.
export function tilBestilling(r) {
  return {
    id: r.id, date: r.dato, minutes: r.minutter || 0, status: r.status || "Ny", name: r.navn, phone: r.telefon,
    address: r.adresse, area: r.omrade, sacks: r.sekker || 0, carry: r.baering, total: r.totalpris, email: r.epost,
    message: r.melding, frequency: r.hyppighet, service: num(r.lossetid), lat: num(r.lat), lon: num(r.lon),
    fixed: !!r.fast, paid: !!r.betalt, registered: r.registrert
  };
}
async function bestillinger(db, fra) {
  const q = fra ? db.prepare("SELECT * FROM bestillinger WHERE dato >= ? ORDER BY dato, registrert").bind(fra)
                : db.prepare("SELECT * FROM bestillinger ORDER BY dato, registrert");
  return (await q.all()).results.map(tilBestilling);
}

// Kommende bestillinger som tar tid, gruppert per dag. Avbestilte teller ikke.
export function perDag(alle, iDag) {
  const out = {};
  alle.forEach((b) => {
    if (b.date >= iDag && b.minutes > 0 && b.status !== "Avbestilt") (out[b.date] = out[b.date] || []).push(b);
  });
  return out;
}
export function bestilt(planer) {
  const out = {};
  Object.keys(planer).forEach((d) => { out[d] = planer[d].minutter; });
  return out;
}

async function leggTil(db, b, status) {
  const id = tilfeldig(4);
  await db.prepare(`INSERT INTO bestillinger (id, dato, minutter, status, navn, telefon, adresse, omrade, sekker, baering,
      totalpris, epost, melding, hyppighet, registrert, lossetid, lat, lon, fast) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`)
    .bind(id, b.date, Math.round(Number(b.minutes)) || 0, status, tekst(b.name, 80), tekst(b.phone, 30), tekst(b.address, 120),
      tekst(b.area, 60), Math.max(0, Math.min(1000, Math.round(Number(b.sacks)) || 0)), tekst(b.carry, 80), tekst(b.total, 40),
      tekst(b.email, 100), tekst(b.message, 1000), linje(b.frequency, 60), naTekst(), b.service == null ? null : b.service,
      b.lat == null ? null : b.lat, b.lon == null ? null : b.lon, b.fixed ? 1 : 0)
    .run();
  return id;
}

// Betalt kan bare være ja for leverte bestillinger. «Angre» (status Ny) fjerner også betalt.
async function endreStatus(db, id, status, betalt) {
  if (!STATUSER.includes(status)) return { ok: false, error: "ugyldig" };
  const r = await db.prepare("UPDATE bestillinger SET status = ?, betalt = ? WHERE id = ?")
    .bind(status, status === "Levert" && betalt ? 1 : 0, id).run();
  return r.meta.changes ? { ok: true } : { ok: false, error: "fant ikke bestillingen" };
}

// Nytt antall sekker. Minutter og lossetid er regnet ut på eiersiden (samme formel som skjemaet).
async function endreSekker(db, id, sekker, minutter, lossetid) {
  sekker = Math.round(Number(sekker));
  minutter = Math.round(Number(minutter));
  if (!(sekker >= 1 && sekker <= 1000) || !(minutter >= 0 && minutter <= 24 * 60)) return { ok: false, error: "ugyldig" };
  const l = service(lossetid);
  const r = await db.prepare("UPDATE bestillinger SET sekker = ?, minutter = ?, lossetid = CASE WHEN lossetid IS NOT NULL AND ? IS NOT NULL THEN ? ELSE lossetid END WHERE id = ?")
    .bind(sekker, minutter, l, l, id).run();
  return r.meta.changes ? { ok: true } : { ok: false, error: "fant ikke bestillingen" };
}

// Flytt en bestilling til en annen dag (før: endre datoen i regnearket).
async function endreDato(db, id, dato) {
  if (!gyldigDato(dato)) return { ok: false, error: "ugyldig" };
  const r = await db.prepare("UPDATE bestillinger SET dato = ? WHERE id = ?").bind(dato, id).run();
  return r.meta.changes ? { ok: true } : { ok: false, error: "fant ikke bestillingen" };
}

// ------------------------------------------------------------------ fulle dager

async function fulleDager(db, iDag) {
  return (await db.prepare("SELECT dato FROM fulle_dager WHERE dato >= ? ORDER BY dato").bind(iDag).all()).results.map((r) => r.dato);
}
async function settFull(db, dato, full, iDag) {
  if (!gyldigDato(dato)) return { ok: false, error: "ugyldig" };
  await db.prepare("DELETE FROM fulle_dager WHERE dato = ? OR dato < ?").bind(dato, iDag).run();
  if (full && dato >= iDag) await db.prepare("INSERT INTO fulle_dager (dato) VALUES (?)").bind(dato).run();
  return { ok: true, fullDays: await fulleDager(db, iDag) };
}

// ------------------------------------------------------------------ ruter

// Slår opp en adresse i Follo hos Kartverket. Gir { lat, lon }, eller null. Svaret huskes i 6 timer.
async function geokod(db, adresse, omrade) {
  const a = String(adresse || "").replace(/\s+/g, " ").trim();
  if (a.length < 3) return null;
  const nokkel = "geo_" + (await sha256(a.toLowerCase() + "|" + omrade)).slice(0, 32);
  const husket = await cacheHent(db, nokkel);
  if (husket) return husket === "-" ? null : JSON.parse(husket);
  // Først bare gatenavn og nummer i kommunen for området, så hele teksten i hele landet (men bare treff i Follo).
  const gate = a.split(",")[0].trim(), kn = KOMMUNE[omrade], forsok = [];
  if (kn) forsok.push({ sok: gate, kommunenummer: kn }, { sok: gate, kommunenummer: kn, fuzzy: "true" });
  forsok.push({ sok: a.replace(/,/g, " ") });
  // Søket finner også «Kirkeveien 10» for «Kirkeveien 1», så riktig husnummer foretrekkes.
  const nr = gate.match(/(\d+)\s*([a-zæøå])?\s*$/i) || [];
  const riktigNr = (x) => !nr[1] || (x.nummer === Number(nr[1]) && (!nr[2] || String(x.bokstav).toLowerCase() === nr[2].toLowerCase()));
  let treff = null, svarte = true;
  for (let i = 0; i < forsok.length && !treff; i++) {
    const url = "https://ws.geonorge.no/adresser/v1/sok?treffPerSide=20&utkoordsys=4258&" + new URLSearchParams(forsok[i]);
    try {
      const r = await fetch(url, { signal: AbortSignal.timeout(8000) });
      if (r.status !== 200) { svarte = false; continue; }
      const liste = ((await r.json()).adresser || []).filter((x) => FOLLO.includes(x.kommunenummer) && x.representasjonspunkt);
      const adr = liste.filter(riktigNr)[0] || liste[0];
      if (adr) treff = { lat: +adr.representasjonspunkt.lat.toFixed(6), lon: +adr.representasjonspunkt.lon.toFixed(6) };
    } catch (e) { svarte = false; }
  }
  // «Fant ikke» huskes bare når Kartverket faktisk svarte, så et kort brudd ikke henger igjen.
  if (treff || svarte) await cacheLagre(db, nokkel, treff ? JSON.stringify(treff) : "-", 6 * 3600);
  return treff;
}

// Kjøretid i sekunder mellom alle punktene, fra OSRM. Gir null hvis tjenesten ikke svarer.
async function matrise(db, pkt) {
  if (pkt.length < 2 || pkt.length > MAKS_PUNKTER) return null;
  const koord = pkt.map((p) => p.lon.toFixed(5) + "," + p.lat.toFixed(5)).join(";");
  const nokkel = "osrm_" + (await sha256(koord)).slice(0, 32), husket = await cacheHent(db, nokkel);
  if (husket) return JSON.parse(husket);
  try {
    const r = await fetch("https://router.project-osrm.org/table/v1/driving/" + koord + "?annotations=duration", { signal: AbortSignal.timeout(10000) });
    const j = await r.json();
    if (j.code !== "Ok" || !j.durations) return null;
    const m = j.durations.map((rad) => rad.map((s) => (s == null ? null : Math.round(s))));
    await cacheLagre(db, nokkel, JSON.stringify(m), 6 * 3600);
    return m;
  } catch (e) {
    return null;
  }
}

// Raskeste runde fra lageret (punkt 0) innom alle stoppene og tilbake. Eksakt for opptil 10 stopp,
// ellers nærmeste nabo forbedret med 2-opt. Gir { rekke, ben (sekunder per etappe), sek }, eller null.
export function rute(m, stopp) {
  const n = stopp.length;
  if (!n) return { rekke: [], ben: [], sek: 0 };
  const d = (a, b) => { const v = m[a][b]; return v == null ? Infinity : v; };
  const lengde = (r) => {
    let s = d(0, stopp[r[0]]) + d(stopp[r[r.length - 1]], 0);
    for (let x = 1; x < r.length; x++) s += d(stopp[r[x - 1]], stopp[r[x]]);
    return s;
  };
  let rekke = [];
  if (n <= 10) {
    const FULL = (1 << n) - 1, dp = [], fra = [];
    for (let mask = 0; mask <= FULL; mask++) { dp.push(new Array(n).fill(Infinity)); fra.push(new Array(n).fill(-1)); }
    for (let j = 0; j < n; j++) dp[1 << j][j] = d(0, stopp[j]);
    for (let mask = 1; mask <= FULL; mask++) {
      for (let j = 0; j < n; j++) {
        if (!(mask & (1 << j)) || dp[mask][j] === Infinity) continue;
        for (let k = 0; k < n; k++) {
          if (mask & (1 << k)) continue;
          const nm = mask | (1 << k), v = dp[mask][j] + d(stopp[j], stopp[k]);
          if (v < dp[nm][k]) { dp[nm][k] = v; fra[nm][k] = j; }
        }
      }
    }
    let best = Infinity, sist = -1;
    for (let j = 0; j < n; j++) { const t = dp[FULL][j] + d(stopp[j], 0); if (t < best) { best = t; sist = j; } }
    if (sist < 0) return null;
    let mask = FULL;
    while (sist >= 0) { rekke.unshift(sist); const f = fra[mask][sist]; mask &= ~(1 << sist); sist = f; }
  } else {
    const igjen = stopp.map((_, x) => x);
    let her = 0;
    while (igjen.length) {
      let bi = 0;
      for (let i = 1; i < igjen.length; i++) if (d(her, stopp[igjen[i]]) < d(her, stopp[igjen[bi]])) bi = i;
      const neste = igjen.splice(bi, 1)[0];
      rekke.push(neste); her = stopp[neste];
    }
    for (let bedre = true; bedre;) {
      bedre = false;
      for (let i = 0; i < n - 1; i++) for (let k = i + 1; k < n; k++) {
        const ny = rekke.slice(0, i).concat(rekke.slice(i, k + 1).reverse(), rekke.slice(k + 1));
        if (lengde(ny) < lengde(rekke) - 1) { rekke = ny; bedre = true; }
      }
    }
  }
  const punkter = [0].concat(rekke.map((x) => stopp[x]), [0]), ben = [];
  for (let i = 1; i < punkter.length; i++) ben.push(d(punkter[i - 1], punkter[i]));
  const sek = ben.reduce((s, x) => s + x, 0);
  return isFinite(sek) ? { rekke, ben, sek } : null;
}

// Bestillinger med faste minutter tas ikke med i ruten, selv om de har koordinater.
const harKoord = (b) => !!b && !b.fixed && b.lat != null && b.lon != null;

function lossetid(b) {
  if (b.service != null) return b.service;
  return LOSSING + (/^\s*(ingen|$)/i.test(b.carry || "") ? 0 : (b.sacks || 0) * BAERING_PER_SEKK);
}

// Punktene (lageret først) for bestillingene med koordinater, og kjøretidene mellom dem.
async function nett(db, liste, kunHvisPlass) {
  const pkt = [LAGER], plass = {};
  const nokkel = (b) => b.lat.toFixed(5) + "," + b.lon.toFixed(5);
  liste.forEach((b) => { if (harKoord(b) && !(nokkel(b) in plass)) { plass[nokkel(b)] = pkt.length; pkt.push(b); } });
  if (kunHvisPlass && pkt.length > MAKS_PUNKTER) return null;
  return { m: pkt.length > MAKS_PUNKTER ? null : await matrise(db, pkt), nr: (b) => plass[nokkel(b)] };
}

// Plan per dag: { minutter, kjoring, ruteOk, rute: [{ id, ben }], tilbake }. Med «ekstra» får hver plan også «med»:
// minuttene hvis den nye bestillingen kommer i tillegg.
export async function planer(db, dager, ekstra) {
  const datoer = Object.keys(dager);
  let alle = [];
  datoer.forEach((d) => { alle = alle.concat(dager[d]); });
  const felles = await nett(db, ekstra ? alle.concat([ekstra]) : alle, true);
  const sum = (liste, f) => liste.reduce((s, b) => s + f(b), 0);
  const plan = (liste, n) => {
    const med = liste.filter(harKoord), uten = liste.filter((b) => !harKoord(b));
    const r = n.m && med.length ? rute(n.m, med.map(n.nr)) : null;
    if (med.length && !r) return { minutter: sum(liste, (b) => b.minutes), kjoring: null, ruteOk: false, rute: [] };
    const min = (sek) => Math.round((sek / 60) * RUTE_TILLEGG);
    const kjoring = r ? min(r.sek) : 0;
    return {
      minutter: Math.round(kjoring + sum(med, lossetid) + sum(uten, (b) => b.minutes)),
      kjoring, ruteOk: !!r,
      rute: r ? r.rekke.map((x, i) => ({ id: med[x].id, ben: min(r.ben[i]) })) : [],
      tilbake: r ? min(r.ben[r.ben.length - 1]) : 0
    };
  };
  const out = {};
  for (const d of datoer) {
    const n = felles || (await nett(db, ekstra ? dager[d].concat([ekstra]) : dager[d]));
    out[d] = plan(dager[d], n);
    if (ekstra) out[d].med = plan(dager[d].concat([ekstra]), n).minutter;
  }
  return out;
}

// Kommende bestillinger uten koordinater slås opp når eiersiden henter listen (maks 15 om gangen).
async function fyllKoordinater(db, alle, iDag) {
  const mangler = alle.filter((b) => b.date >= iDag && b.status !== "Avbestilt" && !b.fixed && !harKoord(b) && b.address).slice(0, 15);
  for (const b of mangler) {
    const p = await geokod(db, b.address, b.area);
    if (!p) continue;
    await db.prepare("UPDATE bestillinger SET lat = ?, lon = ? WHERE id = ?").bind(p.lat, p.lon, b.id).run();
    b.lat = p.lat; b.lon = p.lon;
  }
}

// Lossing og bæring fra nettsiden, kontrollert.
export function service(v) {
  const n = Number(v);
  return v === undefined || v === null || v === "" || !(n >= 0 && n <= 600) ? null : Math.round(n * 10) / 10;
}

// Slår opp adressen og legger på koordinater og lossetid. Verdiene fra nettsiden brukes ikke direkte.
async function medKoord(db, b) {
  const p = await geokod(db, b.address, String(b.area || ""));
  b.lat = p ? p.lat : null; b.lon = p ? p.lon : null;
  b.service = service(b.service);
  if (b.service == null) b.lat = b.lon = null;
}

// ------------------------------------------------------------------ e-post

const UKEDAGER = ["søndag", "mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag"];
const MANEDER = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"];
export function dagTekst(iso) {
  const d = new Date(String(iso) + "T12:00:00Z");
  if (!ISO.test(String(iso)) || isNaN(d.getTime())) return String(iso);
  return UKEDAGER[d.getUTCDay()] + " " + d.getUTCDate() + ". " + MANEDER[d.getUTCMonth()];
}
const HYPPIGHETER = ["Fast levering hver 2. uke", "Fast levering hver 4. uke", "Fast levering hver 6. uke"];

// Teksten til eieren og bekreftelsen til kunden. Kunden får bare fast tekst med tall og dato vi har kontrollert,
// aldri fritekst fra skjemaet, så ingen kan bruke skjemaet til å sende egne e-poster fra oss.
export function bestillingEpost(b, id, cfg) {
  const hyppighet = linje(b.frequency, 60), abonnement = !!hyppighet, kort = hyppighet.replace(/^Fast levering /, "").toLowerCase();
  const hyppKunde = HYPPIGHETER.includes(hyppighet) ? hyppighet : "";
  const sekker = Math.max(0, Math.min(1000, Math.round(Number(b.sacks)) || 0));
  const dag = dagTekst(b.date), dagStor = dag.charAt(0).toUpperCase() + dag.slice(1);
  const adresse = linje(b.address, 120), omrade = linje(b.area, 60), total = linje(b.total, 40);
  const subject = (abonnement ? "Nytt vedabonnement: " + sekker + " sekker " + kort : "Ny vedbestilling: " + sekker + " sekker") +
    " – " + adresse + ", " + omrade + " – " + dag;
  let linjer = [
    (abonnement ? "Nytt vedabonnement" : "Ny vedbestilling") + " fra " + cfg.domene, "",
    (abonnement ? "Første leveringsdag: " : "Leveringsdag: ") + dagStor + " (" + linje(b.date, 10) + ")",
    "Antall sekker: " + sekker,
    "Bæring: " + linje(b.carry, 80)];
  if (abonnement) linjer.push("Hyppighet: " + hyppighet);
  linjer = linjer.concat([
    "Adresse: " + adresse + ", " + omrade,
    "Telefon: " + linje(b.phone, 30),
    "E-post: " + linje(b.email, 100),
    "Totalpris: " + total + (abonnement ? " per levering" : ""),
    "Beregnet tid: " + (Math.round(Number(b.minutes)) || 0) + " min (kjøring, lossing og bæring)",
    "Melding: " + tekst(b.message, 1000),
    "ID: " + id + " (står som «Ny» på eiersiden)", "",
    "Eiersiden: https://" + cfg.domene + "/admin/"]);
  const kunde = "Takk for bestillingen hos " + cfg.firma + "! Vi har mottatt bestilling på " + sekker + " sekker bjørkeved" +
    (hyppKunde ? ", " + hyppKunde.toLowerCase() : "") + ". Veden kommer på dagen du valgte. " +
    (hyppKunde ? "Første leveringsdag: " : "Ønsket leveringsdag: ") + dag + ". " +
    "Prisen du så i skjemaet gjelder, og du betaler ingenting nå. Spørsmål? Ring " + cfg.telefon + ".";
  return { subject, body: linjer.join("\n"), customerSubject: "Takk for bestillingen hos " + cfg.firma, customerBody: kunde };
}

export function henvendelseEpost(h, id, cfg) {
  const gjelder = linje(h.gjelder, 80) || "Annet";
  return {
    subject: "Ny henvendelse fra nettsiden: " + gjelder,
    body: [
      "Ny henvendelse fra " + cfg.domene, "",
      "Gjelder: " + gjelder,
      "Navn: " + linje(h.navn, 80),
      "Telefon: " + linje(h.telefon, 30),
      "E-post: " + linje(h.epost, 100),
      "Side: " + linje(h.side, 120), "",
      "Melding:", tekst(h.melding, 3000), "",
      "ID: " + id,
      "Eiersiden: https://" + cfg.domene + "/admin/"].join("\n")
  };
}

const gyldigEpost = (s) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(s || "").trim());

// Sender én e-post med Resend (resend.com). Kaster ved feil.
async function sendEpost(env, { to, cc, replyTo, subject, text }) {
  if (!env.RESEND_API_KEY) throw new Error("RESEND_API_KEY mangler");
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: "Bearer " + env.RESEND_API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({ from: env.EPOST_FRA, to: [].concat(to), cc: cc && cc.length ? [].concat(cc) : undefined,
      reply_to: replyTo || undefined, subject, text }),
    signal: AbortSignal.timeout(10000)
  });
  if (!r.ok) throw new Error("Resend svarte " + r.status + ": " + (await r.text()).slice(0, 200));
}

function cfgFra(env) {
  return { domene: env.DOMENE || "folloes.no", firma: env.FIRMA || "Follo Bjørkeved", telefon: env.TELEFON || "48 99 39 00",
    til: (env.BESTILLING_TIL || "").split(",").map((s) => s.trim()).filter(Boolean),
    kopi: (env.BESTILLING_KOPI || "").split(",").map((s) => s.trim()).filter(Boolean) };
}

// Bestillingen til eieren (med kopi), og bekreftelsen til kunden. Gir { mailed, mailError }.
async function sendBestilling(env, b, id) {
  const cfg = cfgFra(env), m = bestillingEpost(b, id, cfg), epost = String(b.email || "").trim();
  try {
    await sendEpost(env, { to: cfg.til, cc: cfg.kopi, replyTo: gyldigEpost(epost) ? epost : "", subject: m.subject, text: m.body });
  } catch (e) {
    return { mailed: false, mailError: String((e && e.message) || e) };
  }
  if (gyldigEpost(epost)) {
    try { await sendEpost(env, { to: epost, subject: m.customerSubject, text: m.customerBody }); } catch (e) {}
  }
  return { mailed: true };
}

// ------------------------------------------------------------------ forespørslene

async function ledig(db, b, iDag) {
  if ((await tell(db, "ledigsjekk", 3600)) >= MAKS_LEDIG_SJEKK_PER_TIME) return { ok: false, error: "travelt" };
  const min = Math.round(Number(b.minutes)), kap = Number(b.capacity) || 300;
  if (!(min > 0 && min <= 24 * 60) || !(kap > 0 && kap <= 24 * 60)) return { ok: false, error: "ugyldig" };
  const ny = { id: "ny", address: String(b.address || "").slice(0, 120), area: String(b.area || "").slice(0, 60), service: b.service, minutes: min };
  await medKoord(db, ny);
  const p = await planer(db, perDag(await bestillinger(db, iDag), iDag), ny), fits = {}, fulle = await fulleDager(db, iDag);
  Object.keys(p).forEach((d) => { fits[d] = !(p[d].minutter > 0) || p[d].med <= kap; });
  fulle.forEach((d) => { fits[d] = false; });
  return { ok: true, found: harKoord(ny), fits, booked: bestilt(p), fullDays: fulle };
}

async function nyBestilling(db, env, b, iDag) {
  const dag = String(b.date || ""), min = Math.round(Number(b.minutes)), kap = Number(b.capacity) || 300;
  if (!gyldigDato(dag) || !(min > 0 && min <= 24 * 60) || !(kap > 0 && kap <= 24 * 60)) return { ok: false, error: "ugyldig" };
  const leveringsdager = String(env.LEVERINGSDAGER || "1,2").split(",").map(Number);
  // Ingen levering samme dag eller bakover i tid, bare leveringsdager, og ikke for langt fram.
  if (dag <= iDag || dag > leggTilDager(iDag, MAKS_DAGER_FRAM) || !leveringsdager.includes(new Date(dag + "T12:00:00Z").getUTCDay())) {
    return { ok: false, error: "dato", booked: bestilt(await planer(db, perDag(await bestillinger(db, iDag), iDag))) };
  }
  if ((await lesTeller(db, "nettbestillinger")) >= MAKS_NETTBESTILLINGER_PER_TIME) return { ok: false, error: "travelt" };
  await medKoord(db, b);
  b.minutes = min;
  b.name = "";
  b.fixed = false;   // bare eieren kan sette faste minutter

  const sjekk = async (utenId) => {
    const alle = (await bestillinger(db, iDag)).filter((x) => x.id !== utenId);
    const dager = perDag(alle, iDag), fulle = await fulleDager(db, iDag);
    if (fulle.includes(dag)) return { ok: false, full: true, booked: bestilt(await planer(db, dager)), fullDays: fulle };
    const enDag = dager[dag] ? { [dag]: dager[dag] } : {};
    const plan = (await planer(db, enDag, Object.assign({ id: "ny" }, b)))[dag];
    // En tom dag tar alltid imot, også en stor bestilling som alene er over grensen.
    if (plan && plan.minutter > 0 && plan.med > kap) return { ok: false, full: true, booked: bestilt(await planer(db, dager)) };
    return null;
  };
  const nei = await sjekk();
  if (nei) return nei;
  const id = await leggTil(db, b, "Ny");
  await tell(db, "nettbestillinger", 3600);
  // To kunder kan sende samtidig. Sjekk igjen etter lagring: ble dagen for full med de andre som kom før, trekkes den tilbake.
  // Bare de som ble lagret før denne (rowid) teller, så av to samtidige bestillinger beholdes alltid den første.
  const foran = (await db.prepare(`SELECT * FROM bestillinger WHERE dato = ? AND status != 'Avbestilt' AND minutter > 0
      AND rowid < (SELECT rowid FROM bestillinger WHERE id = ?)`).bind(dag, id).all()).results.map(tilBestilling);
  if (foran.length) {
    const meg = tilBestilling(await db.prepare("SELECT * FROM bestillinger WHERE id = ?").bind(id).first());
    const p = (await planer(db, { [dag]: foran }, meg))[dag];
    if (p && p.minutter > 0 && p.med > kap) {
      await db.prepare("DELETE FROM bestillinger WHERE id = ?").bind(id).run();
      return { ok: false, full: true, booked: bestilt(await planer(db, perDag(await bestillinger(db, iDag), iDag))) };
    }
  }
  const e = await sendBestilling(env, b, id);
  const ut = { ok: true, id, mailed: e.mailed };
  if (!e.mailed) ut.mailError = e.mailError;
  return ut;
}

async function nyHenvendelse(db, env, b) {
  const h = { navn: tekst(b.navn, 80).trim(), telefon: tekst(b.telefon, 30).trim(), epost: tekst(b.epost, 100).trim(),
    gjelder: linje(b.gjelder, 80).trim(), melding: tekst(b.melding, 3000).trim(), side: linje(b.side, 120) };
  if (!h.navn || !h.melding || (!h.telefon && !h.epost) || (h.epost && !gyldigEpost(h.epost))) return { ok: false, error: "ugyldig" };
  if ((await lesTeller(db, "henvendelser")) >= MAKS_HENVENDELSER_PER_TIME) return { ok: false, error: "travelt" };
  const id = tilfeldig(4);
  await db.prepare("INSERT INTO henvendelser (id, registrert, gjelder, navn, telefon, epost, melding, side) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
    .bind(id, naTekst(), h.gjelder, h.navn, h.telefon, h.epost, h.melding, h.side).run();
  await tell(db, "henvendelser", 3600);
  const cfg = cfgFra(env), m = henvendelseEpost(h, id, cfg);
  try {
    await sendEpost(env, { to: cfg.til, cc: cfg.kopi, replyTo: h.epost, subject: m.subject, text: m.body });
    return { ok: true, id, mailed: true };
  } catch (e) {
    return { ok: true, id, mailed: false, mailError: String((e && e.message) || e) };
  }
}

async function eier(db, b, iDag) {
  switch (b.action) {
    case "list": {
      const alle = await bestillinger(db);
      await fyllKoordinater(db, alle, iDag);
      const nye = await db.prepare("SELECT COUNT(*) AS n FROM henvendelser WHERE status = 'Ny'").first();
      return { ok: true, orders: alle, today: iDag, plans: await planer(db, perDag(alle, iDag)), depot: LAGER,
        fullDays: await fulleDager(db, iDag), newInquiries: nye ? nye.n : 0 };
    }
    case "status": return endreStatus(db, String(b.id || ""), String(b.status || ""), b.paid === true);
    case "sacks": return endreSekker(db, String(b.id || ""), b.sacks, b.minutes, b.service);
    case "dato": return endreDato(db, String(b.id || ""), String(b.date || ""));
    case "full": return settFull(db, String(b.date || ""), b.full === true, iDag);
    case "add": {
      if (!gyldigDato(String(b.date || "")) || !(Number(b.minutes) >= 0 && Number(b.minutes) <= 24 * 60)) return { ok: false, error: "ugyldig" };
      // Har eieren skrevet inn minuttene selv, kommer ingen lossetid. Da brukes minuttene som de er.
      b.fixed = service(b.service) == null;
      if (b.fixed) b.service = b.lat = b.lon = null; else await medKoord(db, b);
      return { ok: true, id: await leggTil(db, b, "Bekreftet") };
    }
    case "henvendelser": {
      const r = await db.prepare("SELECT * FROM henvendelser ORDER BY registrert DESC LIMIT 300").all();
      return { ok: true, inquiries: r.results };
    }
    case "henvendelse-status": {
      const st = String(b.status || "");
      if (!HENV_STATUSER.includes(st)) return { ok: false, error: "ugyldig" };
      const r = await db.prepare("UPDATE henvendelser SET status = ? WHERE id = ?").bind(st, String(b.id || "")).run();
      return r.meta.changes ? { ok: true } : { ok: false, error: "fant ikke henvendelsen" };
    }
  }
  return { ok: false, error: "ugyldig" };
}
const EIER = ["list", "status", "sacks", "dato", "full", "add", "henvendelser", "henvendelse-status"];

export async function svar(req, env) {
  const db = env.DB, iDag = idag();
  if (req.method === "GET") {
    const p = await planer(db, perDag(await bestillinger(db, iDag), iDag));
    return { booked: bestilt(p), fullDays: await fulleDager(db, iDag) };
  }
  if (req.method !== "POST") return { ok: false, error: "ugyldig" };
  let b;
  try { b = JSON.parse(await req.text()); } catch (e) { return { ok: false, error: "ugyldig" }; }
  if (!b || typeof b !== "object" || Array.isArray(b)) return { ok: false, error: "ugyldig" };

  if (b.action === "login") return loggInn(db, b.password, b.remember === true);
  if (b.action === "logout") { await loggUt(db, b.token); return { ok: true }; }
  if (EIER.includes(b.action)) {
    if (!(await gyldigBillett(db, b.token))) return { ok: false, error: "token" };
    return eier(db, b, iDag);
  }
  if (b.action === "ledig") return ledig(db, b, iDag);
  if (b.action === "henvendelse") return nyHenvendelse(db, env, b);
  if (b.action) return { ok: false, error: "ugyldig" };
  return nyBestilling(db, env, b, iDag);
}

export default {
  async fetch(req, env) {
    const opphav = req.headers.get("Origin") || "";
    const tillatt = String(env.TILLATTE_OPPHAV || "").split(",").map((s) => s.trim()).filter(Boolean);
    const cors = { "Access-Control-Allow-Origin": tillatt.includes(opphav) ? opphav : tillatt[0] || "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS", "Access-Control-Allow-Headers": "Content-Type", Vary: "Origin" };
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    let ut;
    try {
      ut = await svar(req, env);
    } catch (e) {
      console.error(e);
      ut = { ok: false, error: "serverfeil" };
    }
    return new Response(JSON.stringify(ut), { headers: Object.assign({ "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }, cors) });
  }
};
