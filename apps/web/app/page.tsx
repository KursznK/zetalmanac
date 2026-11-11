import Link from "next/link";
import { connection } from "next/server";
import { hariIniDiJakarta, hariPenting, konversi, rdKeIso, type HasilKonversi } from "@/lib/api";
import DateField from "./date-field";
import { FormatHint, FromField } from "./form-fields";

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
        <p className="font-caps tracking-[0.14em] text-accent">Konverter Kalender</p>
        <h1 className="font-display text-[2.5rem] leading-tight text-balance sm:text-6xl">
          Konversi 5 Kalender Sekaligus
        </h1>
        <p className="max-w-[34em] text-lg text-muted">
          Ubah tanggal antara Kalender Gregorian, Kalender Julian, Kalender Hijriah (hisab urfi),
          Kalender China, dan Kalender Maya. Setiap hasil dapat ditunjukkan langkah-langkah
          perhitungannya, lengkap dengan varian dan sumbernya.
        </p>
        <form method="get" action="/konversi" className="border-[3px] border-double border-rule bg-surface p-1.5">
          <div className="flex flex-wrap items-end gap-4 p-5">
            <DateField defaultValue={tanggal} className="flex-[2_1_12rem]" />
            <FromField defaultValue="gregorian" className="flex-[1_1_10rem]" />
            <button
              type="submit"
              className="tombol inline-flex h-12 cursor-pointer items-center gap-2 bg-btn-bg px-6 font-bold text-btn-ink"
            >
              Konversi{" "}
              <span className="panah" aria-hidden="true">
                →
              </span>
            </button>
          </div>
          <p className="border-t border-rule px-5 pt-3 pb-2.5 text-sm text-muted">
            <FormatHint />
          </p>
        </form>
      </section>

      <div className="flex flex-wrap gap-8">
        <section
          aria-labelledby="hari-ini"
          className="min-w-0 flex-[999_1_34rem] self-start border border-rule bg-surface"
        >
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
                <li key={a.nama}>
                  <Link
                    href={`/konversi?from=gregorian&date=${rdKeIso(a.rd)}`}
                    className="kartu-angkat flex items-center gap-4 border border-rule bg-surface px-5 py-3.5"
                  >
                    <span className="flex min-w-17 flex-col gap-1">
                      <span className="font-display text-4xl leading-none text-accent">
                        {a.hari_lagi === 0 ? "Hari ini" : a.hari_lagi}
                      </span>
                      {a.hari_lagi === 0 ? null : (
                        <span className="font-caps text-[13px] leading-none tracking-[0.08em] text-muted">
                          hari lagi
                        </span>
                      )}
                    </span>
                    <span className="flex min-w-0 flex-1 flex-col">
                      <span className="font-bold">{a.nama}</span>
                      <span className="text-sm text-muted">{a.label}</span>
                    </span>
                    <span className="panah" aria-hidden="true">
                      →
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          ) : (
            <p role="alert">{acara.pesan}</p>
          )}
        </section>
      </div>

      <p className="text-sm text-muted">
        <b>Perhatian:</b>
        <br />
        Tanggal di Kalender Hijri Hisab Urfi bisa berbeda dengan penetapan resmi berdasarkan rukyat
        atau hisab lain.
      </p>

      <section className="border-y border-rule py-5 text-muted">
        <strong className="text-ink">Kapan sebuah hari dimulai?</strong> Gregorian, Julian, dan Maya
        berganti pada tengah malam waktu lokal. Hari di Kalender China berganti pada tengah malam
        waktu Beijing (UTC+8). Hari pada Kalender Hijriah dimulai saat matahari terbenam.
      </section>

      <section aria-labelledby="cara" className="flex flex-col gap-6">
        <h2 id="cara" className="font-display text-3xl text-balance sm:text-4xl">
          Bagaimana cara kami menghitungnya?
        </h2>
        <div className="flex flex-wrap gap-8">
          {[
            ["§1", "Satu titik pusat", "Semua kalender diubah terlebih dulu ke hitungan hari tetap (Rata Die), lalu diubah ke kalender tujuan."],
            ["§2", "Diuji berlapis", "Berdasar dari literatur, berkas acuan ICU dan Hong Kong Observatory, dilakukan uji sifat, dan terdapat tinjauan manusia."],
            ["§3", "Varian ditampilkan", "Terdapat skema urfi I–IV, epoch sipil atau astronomis, dan tiga korelasi Maya. Kalau ada lebih dari satu jawaban yang sah, kamu dapat melihat semuanya."],
          ].map(([nomor, judul, isi]) => (
            <div key={nomor} className="flex min-w-0 flex-[1_1_16rem] flex-col gap-2 border-t-2 border-ink pt-4">
              <p className="font-mono text-accent">{nomor}</p>
              <h3 className="font-serif text-2xl">{judul}</h3>
              <p className="text-muted">{isi}</p>
            </div>
          ))}
        </div>
        <Link href="/validasi" className="tautan self-start">
          Lihat status validasi →
        </Link>
      </section>
    </main>
  );
}

function HariIni({ data }: { data: HasilKonversi }) {
  const baris: [string, string, string?][] = [
    ["Gregorian", `${data.hari}, ${data.gregorian.label}`],
    ["Julian", data.julian.label],
    ["Hijriah · Urfi", data.hijri.label, "Skema II. Epoch Sipil. Setelah magrib masuk ke tanggal berikutnya."],
    [
      "China",
      data.china ? `${data.china.label} · ${data.china.year_ganzhi} (${data.china.year_label})` : "—",
      data.china ? `Hari ${data.china.day_ganzhi} · Zona Waktu Beijing (UTC+8)` : "Hanya tersedia untuk 1901–2100.",
    ],
    ["Maya", data.maya.long_count, `${data.maya.tzolkin} · ${data.maya.haab} · Korelasi GMT ${data.maya.correlation}`],
  ];
  return (
    <dl>
      {baris.map(([judul, utama, catatan]) => (
        <div
          key={judul}
          className="flex flex-wrap gap-x-6 gap-y-1 border-b border-rule px-6 py-4 transition-colors last:border-b-0 hover:bg-chip"
        >
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
