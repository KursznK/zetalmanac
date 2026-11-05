// Membuat golden file Hijriah urfi dari ICU (lewat Intl bawaan Node.js).
// Jalankan dari folder mana saja:  node packages/zetalmanac-core/scripts/gen_hijri_icu.mjs
// Hasil: packages/zetalmanac-core/tests/data/hijri_icu.csv
//
// Isi file:
// 1. Dua baris di setiap pergantian bulan untuk tahun 1–2000 H:
//    hari ketika islamic-civil tanggal 1 dan hari ketika islamic-tbla tanggal 1.
//    (Karena tbla sehari lebih awal, baris kedua juga menguji tanggal terakhir bulan civil.)
// 2. Setiap hari untuk tahun 1440–1460 H (civil).
import { mkdirSync, writeFileSync } from "node:fs";

const options = { timeZone: "UTC", year: "numeric", month: "numeric", day: "numeric" };
const civil = new Intl.DateTimeFormat("en-u-ca-islamic-civil", options);
const tbla = new Intl.DateTimeFormat("en-u-ca-islamic-tbla", options);

function parts(formatter, date) {
  const p = {};
  for (const { type, value } of formatter.formatToParts(date)) p[type] = value;
  return [Number(p.year), Number(p.month), Number(p.day)];
}

const DAY_MS = 86_400_000;
const start = Date.UTC(622, 6, 18); // 18 Juli 622 Gregorian, sehari sebelum 1 Muharam 1 H (tbla)
const rows = [];
for (let ms = start; ; ms += DAY_MS) {
  const date = new Date(ms);
  const c = parts(civil, date);
  const t = parts(tbla, date);
  if (c[0] > 2000) break;
  const keep = (c[0] >= 1 && (c[2] === 1 || t[2] === 1)) || (c[0] >= 1440 && c[0] <= 1460);
  if (keep) rows.push([date.toISOString().slice(0, 10), ...c, ...t].join(","));
}

const header = [
  `# Sumber: ICU ${process.versions.icu} lewat Node.js ${process.version} (Intl.DateTimeFormat)`,
  "# islamic-civil = skema II + epoch sipil; islamic-tbla = skema II + epoch astronomis",
  "# Dibuat oleh scripts/gen_hijri_icu.mjs. Jangan disunting manual.",
  "gregorian,civil_year,civil_month,civil_day,tbla_year,tbla_month,tbla_day",
];

const dir = new URL("../tests/data/", import.meta.url);
mkdirSync(dir, { recursive: true });
writeFileSync(new URL("hijri_icu.csv", dir), header.concat(rows).join("\n") + "\n");
console.log(`Menulis ${rows.length} baris ke tests/data/hijri_icu.csv`);
