import Link from "next/link";
import { connection } from "next/server";
import { hariIniDiJakarta, hariPenting, KALENDER, konversi, type HasilKonversi } from "@/lib/api";

export default async function Home() {
  await connection(); // "hari ini" berubah setiap hari, jadi halaman dirender saat diminta
  const tanggal = hariIniDiJakarta();
  const [hasil, acara] = await Promise.all([
    konversi({
      from: "gregorian",
      date: tanggal,
      scheme: "II",
      epoch: "civil",
      correlation: "584283",
      leap: false,
      afterSunset: false,
    }),
    hariPenting(tanggal),
  ]);

  return (
    <main className="mx-auto flex max-w-5xl flex-col gap-14 px-6 py-16">
      <section className="flex flex-col gap-5">
        <p className="font-caps tracking-[0.14em] text-accent">konverter kalender · almanak terbuka</p>
        <h1 className="font-display text-5xl leading-tight sm:text-6xl">Satu hari, lima cara menghitungnya.</h1>
        <p className="max-w-[34em] text-lg text-muted">
          Ubah tanggal antara Gregorian, Julian, Hijriah (hisab urfi), China, dan Maya. Setiap hasil
          bisa dibuka langkah hitungnya, lengkap dengan varian dan sumbernya.
        </p>
        <form method="get" action="/konversi" className="border-[3px] border-double border-rule bg-surface p-1.5">
          <div className="flex flex-wrap items-end gap-4 p-5">
            <label className="flex flex-[2_1_12rem] flex-col gap-1.5 text-sm text-muted">
              Tanggal
              <input
                name="date"
                defaultValue={tanggal}
                maxLength={20}
                required
                className="h-12 border border-rule bg-bg px-3 font-mono text-base text-ink"
              />
            </label>
            <label className="flex flex-[1_1_10rem] flex-col gap-1.5 text-sm text-muted">
              Dari kalender
              <select name="from" defaultValue="gregorian" className="h-12 border border-rule bg-bg px-3 text-base text-ink">
                {KALENDER.map((k) => (
                  <option key={k.id} value={k.id}>
                    {k.label}
                  </option>
                ))}
              </select>
            </label>
            <button type="submit" className="h-12 bg-btn-bg px-6 font-bold text-btn-ink">
              Konversi
            </button>
          </div>
        </form>
      </section>

      <div className="flex flex-wrap gap-8">
        <section aria-labelledby="hari-ini" className="min-w-0 flex-[999_1_34rem] border border-rule bg-surface">
          <div className="flex flex-wrap items-baseline justify-between gap-2 border-b border-rule px-6 py-4">
            <h2 id="hari-ini" className="font-display text-3xl">
              Hari ini
            </h2>
            {hasil.ok ? (
              <p className="font-mono text-sm text-muted">
                JDN {hasil.data.jdn} · RD {hasil.data.rd}
              </p>
            ) : null}
          </div>
          {hasil.ok ? (
            <HariIni data={hasil.data} />
          ) : (
            <p role="alert" className="p-6">
              {hasil.pesan}
            </p>
          )}
        </section>

        <section aria-labelledby="berikutnya" className="flex min-w-0 flex-[1_1_18rem] flex-col gap-4">
          <h2 id="berikutnya" className="font-display text-3xl">
            Berikutnya
          </h2>
          {acara.ok ? (
            <ul className="flex flex-col gap-3">
              {acara.data.map((a) => (
                <li key={a.nama} className="flex items-center gap-4 border border-rule bg-surface px-5 py-4">
                  <p className="min-w-16 font-display text-4xl leading-none text-accent">
                    {a.hari_lagi === 0 ? "Hari ini" : a.hari_lagi}
                  </p>
                  <div className="flex flex-col">
                    <span className="font-bold">{a.nama}</span>
                    <span className="text-sm text-muted">{a.label}</span>
                  </div>
                </li>
              ))}
            </ul>
          ) : (
            <p role="alert">{acara.pesan}</p>
          )}
          <p className="text-sm text-muted">
            Angka besar = hari lagi. Tanggal urfi bisa berbeda dengan penetapan resmi berdasarkan rukyat
            atau hisab lain.
          </p>
        </section>
      </div>

      <section className="border-y border-rule py-5 text-muted">
        <strong className="text-ink">Kapan sebuah hari dimulai?</strong> Gregorian, Julian, dan Maya
        berganti pada tengah malam waktu lokal. Hari China berganti pada tengah malam waktu Beijing
        (UTC+8). Hari Hijriah dimulai saat matahari terbenam, jadi tanggalnya bisa sudah berganti
        padahal kalender Masehi belum.
      </section>

      <section aria-labelledby="cara" className="flex flex-col gap-6">
        <h2 id="cara" className="font-display text-4xl">
          Cara kami menghitung
        </h2>
        <div className="flex flex-wrap gap-8">
          {[
            ["§1", "Satu titik pusat", "Semua kalender diubah dulu ke hitungan hari tetap (Rata Die), lalu dari situ ke kalender tujuan."],
            ["§2", "Diuji berlapis", "Jangkar dari literatur, berkas acuan ICU dan Hong Kong Observatory, uji sifat, dan tinjauan manusia."],
            ["§3", "Varian ditampilkan", "Skema urfi I–IV, epoch sipil atau astronomis, tiga korelasi Maya. Kalau ada lebih dari satu jawaban yang sah, kamu melihat semuanya."],
          ].map(([nomor, judul, isi]) => (
            <div key={nomor} className="flex min-w-0 flex-[1_1_16rem] flex-col gap-2 border-t-2 border-ink pt-4">
              <p className="font-mono text-accent">{nomor}</p>
              <h3 className="font-serif text-2xl">{judul}</h3>
              <p className="text-muted">{isi}</p>
            </div>
          ))}
        </div>
        <Link href="/validasi" className="self-start underline underline-offset-4">
          Lihat status validasi
        </Link>
      </section>
    </main>
  );
}

function HariIni({ data }: { data: HasilKonversi }) {
  const baris: [string, string, string?][] = [
    ["gregorian", `${data.hari}, ${data.gregorian.label}`],
    ["julian", data.julian.label],
    ["hijriah · urfi", data.hijri.label, "Skema II, epoch sipil. Setelah magrib sudah tanggal berikutnya."],
    [
      "china",
      data.china ? `${data.china.label} · ${data.china.year_ganzhi} (${data.china.year_label})` : "—",
      data.china ? `Hari ${data.china.day_ganzhi} · waktu Beijing (UTC+8)` : "Hanya tersedia untuk 1901–2100.",
    ],
    ["maya", data.maya.long_count, `${data.maya.tzolkin} · ${data.maya.haab} · korelasi GMT ${data.maya.correlation}`],
  ];
  return (
    <dl>
      {baris.map(([judul, utama, catatan]) => (
        <div key={judul} className="flex flex-wrap gap-x-6 gap-y-1 border-b border-rule px-6 py-4 last:border-b-0">
          <dt className="flex-[0_0_10rem] font-caps tracking-[0.08em] text-muted">{judul}</dt>
          <dd className="flex min-w-0 flex-[1_1_16rem] flex-col">
            <span className="font-serif text-xl">{utama}</span>
            {catatan ? <span className="text-sm text-muted">{catatan}</span> : null}
          </dd>
        </div>
      ))}
    </dl>
  );
}
