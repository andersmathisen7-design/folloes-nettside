// Tester serveren i Miniflare (Cloudflare sin lokale simulator) med en tom D1-database.
// Kartverket, OSRM og Resend er simulert, så ingenting går ut på nettet og ingen e-post sendes.
//
//   cd server && npm test
import { Miniflare } from "miniflare";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { pbkdf2, idag, leggTilDager } from "../src/logikk.js";

const rot = fileURLToPath(new URL("..", import.meta.url));
const eposter = [];
let resendNede = false, osrmNede = false;

// Adresser i testen: «Testveien N» ligger N kilometer øst for lageret.
function utgaende(req) {
  const u = new URL(req.url);
  if (u.hostname === "ws.geonorge.no") {
    const m = (u.searchParams.get("sok") || "").match(/Testveien (\d+)/);
    const adresser = m ? [{ kommunenummer: "3218", nummer: +m[1], bokstav: "",
      representasjonspunkt: { lat: 59.68112, lon: 10.74194 + +m[1] * 0.0177 } }] : [];
    return Response.json({ adresser });
  }
  if (u.hostname === "router.project-osrm.org") {
    if (osrmNede) return new Response("nede", { status: 503 });
    const pkt = u.pathname.split("/").pop().split(";").map((p) => p.split(",").map(Number));
    // 1 minutt kjøring per kilometer (ca. 0,0177 grader lengde per km her).
    const durations = pkt.map((a) => pkt.map((b) => Math.round((Math.abs(a[0] - b[0]) / 0.0177) * 60)));
    return Response.json({ code: "Ok", durations });
  }
  if (u.hostname === "api.resend.com") {
    if (resendNede) return new Response("nede", { status: 500 });
    return req.json().then((j) => { eposter.push(j); return Response.json({ id: "x" }); });
  }
  return new Response("ukjent vert " + u.hostname, { status: 599 });
}

function lag(medNokkel = true) {
  return new Miniflare({
    modules: true, scriptPath: rot + "src/index.js", compatibilityDate: "2026-10-01",
    modulesRules: [{ type: "ESModule", include: ["**/*.js"] }],
    d1Databases: ["DB"], outboundService: utgaende,
    bindings: { DOMENE: "folloes.no", FIRMA: "Follo Bjørkeved", TELEFON: "48 99 39 00", BESTILLING_TIL: "eier@example.com",
      BESTILLING_KOPI: "kopi@example.com", EPOST_FRA: "Test <test@folloes.no>", LEVERINGSDAGER: "1,2",
      TILLATTE_OPPHAV: "https://folloes.no,http://localhost:8000", ...(medNokkel ? { RESEND_API_KEY: "re_test" } : {}) }
  });
}

async function migrer(mf) {
  const db = await mf.getD1Database("DB");
  const sql = readFileSync(rot + "migrations/0001_start.sql", "utf8").replace(/--.*$/gm, "");
  for (const s of sql.split(";").map((x) => x.trim()).filter(Boolean)) await db.prepare(s).run();
  return db;
}

let mf, db;
const post = (body, opphav = "https://folloes.no") =>
  mf.dispatchFetch("http://server/", { method: "POST", headers: { "Content-Type": "text/plain;charset=utf-8", Origin: opphav }, body: JSON.stringify(body) })
    .then(async (r) => Object.assign(await r.json(), { _cors: r.headers.get("Access-Control-Allow-Origin") }));
const get = () => mf.dispatchFetch("http://server/").then((r) => r.json());

// Neste mandag minst 2 dager fram, og onsdagen etter.
let mandag = leggTilDager(idag(), 2);
while (new Date(mandag + "T12:00:00Z").getUTCDay() !== 1) mandag = leggTilDager(mandag, 1);
const tirsdag = leggTilDager(mandag, 1), onsdag = leggTilDager(mandag, 2);

const bestilling = (extra = {}) => Object.assign({ date: mandag, minutes: 60, service: 20, capacity: 300, area: "Ås", sacks: 20,
  phone: "48 00 00 00", address: "Testveien 10", carry: "Ingen bæring", total: "2 279 kr", email: "kunde@example.com",
  message: "=HYPERLINK(\"x\") Ring på", frequency: "" }, extra);

let feil = 0, antall = 0;
async function test(navn, fn) {
  antall++;
  try { await fn(); console.log("OK   " + navn); } catch (e) { feil++; console.log("FEIL " + navn + "\n     " + (e && e.stack || e)); }
}
function forvent(v, tekst) { if (!v) throw new Error(tekst || "forventet sann verdi"); }
function lik(a, b, tekst) { if (JSON.stringify(a) !== JSON.stringify(b)) throw new Error((tekst || "ulike") + ": " + JSON.stringify(a) + " ≠ " + JSON.stringify(b)); }

mf = lag();
db = await migrer(mf);

await test("GET uten bestillinger gir tom kalender", async () => {
  const j = await get();
  lik(j, { booked: {}, fullDays: [] });
});

await test("Nettbestilling lagres, eieren får e-post med kopi, og kunden får fast bekreftelse", async () => {
  const j = await post(bestilling());
  forvent(j.ok && j.id && j.mailed === true, JSON.stringify(j));
  lik(j._cors, "https://folloes.no", "CORS");
  lik(eposter.length, 2, "antall e-poster");
  const [eier, kunde] = eposter;
  lik(eier.to, ["eier@example.com"]); lik(eier.cc, ["kopi@example.com"]); lik(eier.reply_to, "kunde@example.com");
  forvent(eier.subject.startsWith("Ny vedbestilling: 20 sekker – Testveien 10, Ås – mandag"), eier.subject);
  forvent(eier.text.includes("Eiersiden: https://folloes.no/admin/"), "lenke til eiersiden");
  lik(kunde.to, ["kunde@example.com"]);
  forvent(!kunde.text.includes("HYPERLINK") && !kunde.text.includes("Testveien"), "kunden skal ikke få fritekst");
  const rad = await db.prepare("SELECT * FROM bestillinger WHERE id = ?").bind(j.id).first();
  lik([rad.status, rad.navn, rad.fast, rad.lat != null], ["Ny", "", 0, true]);
  forvent(rad.melding.startsWith("=HYPERLINK"), "meldingen lagres som tekst");
});

await test("GET viser brukt tid: 10 min kjøring hver vei × 1,2 + 20 min lossing = 44", async () => {
  const j = await get();
  lik(j.booked, { [mandag]: 44 });
});

await test("Onsdag og i dag avvises med «dato»", async () => {
  lik((await post(bestilling({ date: onsdag }))).error, "dato");
  lik((await post(bestilling({ date: idag() }))).error, "dato");
});

await test("Ugyldige verdier avvises", async () => {
  lik((await post(bestilling({ minutes: 0 }))).error, "ugyldig");
  lik((await post(bestilling({ date: "i morgen" }))).error, "ugyldig");
  lik((await post({ action: "slett-alt" })).error, "ugyldig");
  lik((await mf.dispatchFetch("http://server/", { method: "POST", body: "{ikke json" }).then((r) => r.json())).error, "ugyldig");
});

await test("Ledig: samme gate får plass, men ikke når kapasiteten er brukt opp", async () => {
  const j = await post({ action: "ledig", address: "Testveien 10", area: "Ås", minutes: 60, service: 20, capacity: 300 });
  forvent(j.ok && j.found, JSON.stringify(j));
  lik(j.fits[mandag], true);
  const k = await post({ action: "ledig", address: "Testveien 30", area: "Ås", minutes: 60, service: 20, capacity: 70 });
  lik(k.fits[mandag], false, "60 min kjøring hver vei passer ikke i 70 min");
});

await test("Full dag: ny bestilling avvises når den ikke får plass", async () => {
  const j = await post(bestilling({ address: "Testveien 30", capacity: 70 }));
  lik([j.ok, j.full], [false, true]);
  forvent(j.booked && j.booked[mandag] === 44, JSON.stringify(j.booked));
});

await test("Uten Resend-nøkkel lagres bestillingen, men mailed er false (nettsiden bruker da FormSubmit)", async () => {
  const mf2 = lag(false), db2 = await migrer(mf2);
  const svar = await mf2.dispatchFetch("http://server/", { method: "POST", body: JSON.stringify(bestilling({ date: tirsdag })) }).then((r) => r.json());
  forvent(svar.ok && svar.mailed === false && /RESEND_API_KEY/.test(svar.mailError), JSON.stringify(svar));
  lik((await db2.prepare("SELECT COUNT(*) AS n FROM bestillinger").first()).n, 1);
  await mf2.dispose();
});

await test("OSRM nede: faste minutter fra skjemaet brukes", async () => {
  osrmNede = true;
  await db.prepare("DELETE FROM cache").run();
  const j = await get();
  osrmNede = false;
  lik(j.booked[mandag], 60);
});

await test("Henvendelse fra kontaktskjemaet lagres og sendes til eieren", async () => {
  eposter.length = 0;
  const j = await post({ action: "henvendelse", navn: "Kari", telefon: "", epost: "kari@example.com", gjelder: "Garasjevask",
    melding: "Tilbud på 40 plasser\nAdresse: Storgata 1", side: "/garasjevask/" });
  forvent(j.ok && j.mailed, JSON.stringify(j));
  lik(eposter.length, 1);
  lik(eposter[0].subject, "Ny henvendelse fra nettsiden: Garasjevask");
  lik(eposter[0].reply_to, "kari@example.com");
  forvent(eposter[0].text.includes("Tilbud på 40 plasser\nAdresse: Storgata 1"));
});

await test("Henvendelse uten telefon og e-post, eller med ugyldig e-post, avvises", async () => {
  lik((await post({ action: "henvendelse", navn: "Ola", melding: "Hei" })).error, "ugyldig");
  lik((await post({ action: "henvendelse", navn: "Ola", epost: "ikke-epost", melding: "Hei" })).error, "ugyldig");
});

await test("Resend nede: henvendelsen er lagret, mailed er false", async () => {
  resendNede = true;
  const j = await post({ action: "henvendelse", navn: "Per", telefon: "99999999", gjelder: "Renhold", melding: "Ring meg" });
  resendNede = false;
  forvent(j.ok && j.mailed === false, JSON.stringify(j));
});

let token = "";
await test("Eiersiden: uten passord satt opp svarer innloggingen «ikke-satt-opp»", async () => {
  lik((await post({ action: "login", password: "x" })).error, "ikke-satt-opp");
});

await test("Eiersiden: feil passord avvises, riktig gir billett", async () => {
  const salt = "abc123";
  await db.prepare("INSERT INTO innstillinger (nokkel, verdi) VALUES ('pw_salt', ?), ('pw_hash', ?)").bind(salt, await pbkdf2("hemmelig-passord", salt)).run();
  lik((await post({ action: "login", password: "feil" })).error, "passord");
  const j = await post({ action: "login", password: "hemmelig-passord", remember: true });
  forvent(j.ok && j.token.length >= 40 && j.expires > Date.now() + 29 * 864e5, JSON.stringify(j));
  token = j.token;
});

await test("Eiersiden: uten billett ingen kundedata", async () => {
  lik((await post({ action: "list" })).error, "token");
  lik((await post({ action: "list", token: "x".repeat(64) })).error, "token");
  lik((await post({ action: "henvendelser", token: "" })).error, "token");
});

await test("Eiersiden: list gir bestillinger, rute, depot og antall nye henvendelser", async () => {
  const j = await post({ action: "list", token });
  forvent(j.ok, JSON.stringify(j));
  lik(j.orders.length, 1);
  lik(j.today, idag());
  lik(j.plans[mandag].rute.length, 1);
  lik(j.newInquiries, 2);
  forvent(j.depot && j.depot.lat, "depot");
});

await test("Eiersiden: telefonbestilling med egne minutter, flytt dag, endre sekker og status", async () => {
  const add = await post({ action: "add", token, date: tirsdag, minutes: 45, service: null, name: "Telefonkunde", phone: "1", address: "Et sted", area: "Ås", sacks: 10 });
  forvent(add.ok, JSON.stringify(add));
  const rad = await db.prepare("SELECT * FROM bestillinger WHERE id = ?").bind(add.id).first();
  lik([rad.status, rad.fast, rad.minutter, rad.lat], ["Bekreftet", 1, 45, null]);
  lik((await post({ action: "dato", token, id: add.id, date: mandag })).ok, true);
  lik((await post({ action: "dato", token, id: add.id, date: "feil" })).error, "ugyldig");
  lik((await post({ action: "sacks", token, id: add.id, sacks: 12, minutes: 50 })).ok, true);
  lik((await post({ action: "status", token, id: add.id, status: "Levert", paid: true })).ok, true);
  const etter = await db.prepare("SELECT * FROM bestillinger WHERE id = ?").bind(add.id).first();
  lik([etter.dato, etter.sekker, etter.minutter, etter.status, etter.betalt], [mandag, 12, 50, "Levert", 1]);
  lik((await post({ action: "status", token, id: add.id, status: "Ny" })).ok, true);
  lik((await db.prepare("SELECT betalt FROM bestillinger WHERE id = ?").bind(add.id).first()).betalt, 0, "angre fjerner betalt");
  lik((await post({ action: "status", token, id: add.id, status: "Slettet" })).error, "ugyldig");
  lik((await post({ action: "status", token, id: "finnes-ikke", status: "Levert" })).ok, false);
});

await test("Eiersiden: sett dagen som full og åpne igjen", async () => {
  lik((await post({ action: "full", token, date: tirsdag, full: true })).fullDays, [tirsdag]);
  lik((await get()).fullDays, [tirsdag]);
  lik((await post(bestilling({ date: tirsdag }))).full, true);
  lik((await post({ action: "full", token, date: tirsdag, full: false })).fullDays, []);
});

await test("Eiersiden: henvendelser kan listes og merkes som besvart", async () => {
  const j = await post({ action: "henvendelser", token });
  lik(j.inquiries.length, 2);
  lik((await post({ action: "henvendelse-status", token, id: j.inquiries[0].id, status: "Besvart" })).ok, true);
  lik((await post({ action: "henvendelse-status", token, id: j.inquiries[0].id, status: "Borte" })).error, "ugyldig");
  lik((await post({ action: "list", token })).newInquiries, 1);
});

await test("Eiersiden: utlogging gjør billetten ugyldig", async () => {
  await post({ action: "logout", token });
  lik((await post({ action: "list", token })).error, "token");
});

await test("Maks 10 feil passord, deretter sperret (også med riktig passord)", async () => {
  for (let i = 0; i < 9; i++) await post({ action: "login", password: "feil" });
  lik((await post({ action: "login", password: "hemmelig-passord" })).error, "sperret");
});

await test("Ukjent opphav får ikke sitt eget opphav tilbake i CORS", async () => {
  lik((await post({ action: "ledig" }, "https://ondsinnet.example")).__proto__ && (await post({ action: "ledig" }, "https://ondsinnet.example"))._cors, "https://folloes.no");
});

await test("Samtidige bestillinger: den siste plassen går bare til én", async () => {
  const mf3 = lag(), db3 = await migrer(mf3);
  // Én alene: 20 min hver vei × 1,2 + 20 lossing = 68 min. To i samme gate: ca. 90 min. Bare én får plass i 80.
  const send = (adr) => mf3.dispatchFetch("http://server/", { method: "POST",
    body: JSON.stringify(bestilling({ address: adr, capacity: 80 })) }).then((r) => r.json());
  const svar = await Promise.all([send("Testveien 20"), send("Testveien 21"), send("Testveien 22")]);
  const ok = svar.filter((s) => s.ok).length;
  lik((await db3.prepare("SELECT COUNT(*) AS n FROM bestillinger").first()).n, ok, "lagret = godtatt");
  forvent(ok === 1, "bare én skal få plass, fikk " + ok + ": " + JSON.stringify(svar));
  await mf3.dispose();
});

await mf.dispose();
console.log(feil ? `${feil} av ${antall} tester feilet` : `Alle ${antall} tester OK`);
process.exit(feil ? 1 : 0);
