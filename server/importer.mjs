// Flytter bestillingene fra regnearket «Follo Bjørkeved – leveringskalender» inn i databasen.
//
// 1. Åpne regnearket, velg arket «Bestillinger», og Fil → Last ned → CSV.
// 2. npm run importer -- ~/Nedlastinger/Bestillinger.csv            (den ekte databasen)
//    npm run importer -- Bestillinger.csv --local                    (den lokale testdatabasen)
//    npm run importer -- Bestillinger.csv --bare-sql                 (lager bare import.sql, sender ingenting)
//
// Kan kjøres flere ganger: rader med samme ID blir oppdatert, ikke lagt inn to ganger.
// Fulle dager ligger ikke i arket. Sett dem på nytt på eiersiden etter importen.
import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

const fil = process.argv.slice(2).find((a) => !a.startsWith("--"));
if (!fil) { console.error("Bruk: npm run importer -- Bestillinger.csv [--local | --bare-sql]"); process.exit(1); }
const lokal = process.argv.includes("--local"), bareSql = process.argv.includes("--bare-sql");

// CSV etter RFC 4180 (Google Sheets bruker komma og "" for anførselstegn).
export function lesCsv(tekst) {
  const rader = [];
  let rad = [], felt = "", i = 0, iAnf = false;
  tekst = tekst.replace(/^﻿/, "");
  for (; i < tekst.length; i++) {
    const c = tekst[i];
    if (iAnf) {
      if (c === '"' && tekst[i + 1] === '"') { felt += '"'; i++; }
      else if (c === '"') iAnf = false;
      else felt += c;
    } else if (c === '"') iAnf = true;
    else if (c === ",") { rad.push(felt); felt = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && tekst[i + 1] === "\n") i++;
      rad.push(felt); felt = "";
      if (rad.some((f) => f !== "")) rader.push(rad);
      rad = [];
    } else felt += c;
  }
  rad.push(felt);
  if (rad.some((f) => f !== "")) rader.push(rad);
  return rader;
}

// Datoer kan komme som 2026-11-10, 10.11.2026 eller 10/11/2026, med eller uten klokkeslett.
function dato(v) {
  v = String(v || "").trim().replace(/^'/, "");
  let m = v.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (m) return `${m[1]}-${m[2]}-${m[3]}`;
  m = v.match(/^(\d{1,2})[./](\d{1,2})[./](\d{4})/);
  if (m) return `${m[3]}-${m[2].padStart(2, "0")}-${m[1].padStart(2, "0")}`;
  return "";
}
function tidspunkt(v) {
  const d = dato(v);
  const t = String(v || "").match(/(\d{1,2})[:.](\d{2})(?::\d{2})?\s*$/);
  return d ? d + (t ? ` ${t[1].padStart(2, "0")}:${t[2]}` : " 00:00") : "";
}
const tall = (v) => { const s = String(v || "").trim().replace(/\s/g, "").replace(",", "."); return s === "" || isNaN(Number(s)) ? null : Number(s); };
const ja = (v) => /^(ja|x|1|true)$/i.test(String(v || "").trim());
const q = (v) => (v == null ? "NULL" : typeof v === "number" ? String(v) : "'" + String(v).replace(/'/g, "''") + "'");
// Arket lagret tekst som begynte med = + - @ med en ' foran, så den ikke ble en formel. Den fjernes her.
const ren = (v) => String(v == null ? "" : v).replace(/^'(?=[=+\-@\t\r])/, "");

const rader = lesCsv(readFileSync(fil, "utf8"));
const hode = rader[0].map((h) => h.trim());
const kol = (r, navn) => { const i = hode.indexOf(navn); return i < 0 ? "" : r[i] ?? ""; };
for (const k of ["Leveringsdag", "Minutter", "Adresse"]) {
  if (!hode.includes(k)) { console.error(`Fant ikke kolonnen «${k}». Er det arket «Bestillinger» som er lastet ned?`); process.exit(1); }
}

const sql = [], hoppet = [];
rader.slice(1).forEach((r, n) => {
  const dag = dato(kol(r, "Leveringsdag"));
  if (!dag) { hoppet.push(n + 2); return; }
  const id = String(kol(r, "ID")).trim();
  const status = ["Ny", "Bekreftet", "Levert", "Avbestilt"].includes(kol(r, "Status").trim()) ? kol(r, "Status").trim() : "Ny";
  const v = {
    id: id || "rad-" + (n + 2), dato: dag, minutter: Math.round(tall(kol(r, "Minutter")) || 0), status,
    navn: ren(kol(r, "Navn")), telefon: ren(kol(r, "Telefon")), adresse: ren(kol(r, "Adresse")), omrade: ren(kol(r, "Område")),
    sekker: Math.round(tall(kol(r, "Sekker")) || 0), baering: ren(kol(r, "Bæring")), totalpris: ren(kol(r, "Totalpris")),
    epost: ren(kol(r, "E-post")), melding: ren(kol(r, "Melding")),
    hyppighet: (ren(kol(r, "Melding")).match(/^Vedabonnement: (fast levering hver \d\. uke)/i) || [])[1] || "",
    registrert: tidspunkt(kol(r, "Registrert")) || dag + " 00:00",
    lossetid: tall(kol(r, "Lossetid")), lat: tall(kol(r, "Lat")), lon: tall(kol(r, "Lon")),
    // Rader uten ID er lagt inn for hånd i arket: da er minuttene satt av eieren.
    fast: !id || ja(kol(r, "Fast tid")) ? 1 : 0, betalt: ja(kol(r, "Betalt")) ? 1 : 0
  };
  if (v.hyppighet) v.hyppighet = "Fast levering " + v.hyppighet.replace(/^fast levering /i, "");
  const k = Object.keys(v);
  sql.push(`INSERT INTO bestillinger (${k.join(", ")}) VALUES (${k.map((x) => q(v[x])).join(", ")})
  ON CONFLICT (id) DO UPDATE SET ${k.filter((x) => x !== "id").map((x) => `${x} = excluded.${x}`).join(", ")};`);
});

writeFileSync(new URL("import.sql", import.meta.url), sql.join("\n") + "\n");
console.log(`${sql.length} bestillinger klare${hoppet.length ? `, ${hoppet.length} rader uten gyldig leveringsdag hoppet over (rad ${hoppet.join(", ")})` : ""}.`);
if (bareSql) { console.log("Skrev import.sql. Ingenting er sendt."); process.exit(0); }
execFileSync("npx", ["wrangler", "d1", "execute", "folloes", lokal ? "--local" : "--remote", "--file", "import.sql", "--yes"],
  { stdio: "inherit", cwd: new URL(".", import.meta.url).pathname });
console.log("Ferdig. Sjekk eiersiden, og sett fulle dager på nytt der.");
