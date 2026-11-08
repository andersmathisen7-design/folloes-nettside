// Lager nytt passord til eiersiden og logger ut alle enheter. Passordet vises én gang.
//
//   npm run passord                    # i den ekte databasen hos Cloudflare
//   npm run passord -- --local         # i den lokale testdatabasen
//   npm run passord -- --logg-ut-alle  # bare logg ut alle enheter, behold passordet
import { execFileSync } from "node:child_process";
import { randomBytes, randomInt } from "node:crypto";
import { pbkdf2 } from "./src/logikk.js";

const lokal = process.argv.includes("--local");
const bareUt = process.argv.includes("--logg-ut-alle");

function sql(kommando) {
  execFileSync("npx", ["wrangler", "d1", "execute", "folloes", lokal ? "--local" : "--remote", "--command", kommando],
    { stdio: ["ignore", "ignore", "inherit"], cwd: new URL(".", import.meta.url).pathname });
}

if (bareUt) {
  sql("DELETE FROM billetter");
  console.log("Alle enheter er logget ut av eiersiden.");
  process.exit(0);
}

const tegn = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789";
let pw = "";
for (let i = 0; i < 20; i++) pw += tegn[randomInt(tegn.length)];
pw = pw.replace(/(.{5})(?!$)/g, "$1-");   // f.eks. abcde-fghij-kmnpq-rstuv
const salt = randomBytes(16).toString("hex");
const hash = await pbkdf2(pw, salt);
sql(`INSERT INTO innstillinger (nokkel, verdi) VALUES ('pw_salt', '${salt}'), ('pw_hash', '${hash}')
     ON CONFLICT (nokkel) DO UPDATE SET verdi = excluded.verdi; DELETE FROM billetter;`);
console.log(`\nNytt passord til eiersiden (folloes.no/admin/):\n\n    ${pw}\n\nLagre det i en passordbehandler. Det vises ikke igjen. Alle enheter er logget ut.\n`);
