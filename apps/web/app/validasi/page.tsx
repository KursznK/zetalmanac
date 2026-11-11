import type { Metadata } from "next";

export const metadata: Metadata = { title: "Validasi · Zetalmanac" };

type Status = "terverifikasi" | "teruji";

const STATUS: { kalender: string; pembanding: string; tes: string; status: Status }[] = [
  {
    kalender: "Gregorian",
    pembanding: "Modul datetime Python untuk setiap hari tahun 1–9999; jangkar JD 0, tahun 0 dan negatif",
    tes: "42",
    status: "terverifikasi",
  },
  {
    kalender: "Hijriah urfi · skema II",
    pembanding:
      "ICU islamic-civil dan islamic-tbla: 54.937 titik (setiap pergantian bulan 1–2000 H, setiap hari 1440–1460 H)",
    tes: "50",
    status: "terverifikasi",
  },
  {
    kalender: "China",
    pembanding:
      "Tabel Hong Kong Observatory 1901–2100: setiap hari (73.048) dan setiap zhongqi, dengan pengecualian terdokumentasi di bawah",
    tes: "37",
    status: "terverifikasi",
  },
  {
    kalender: "Hijriah urfi · skema I, III, IV",
    pembanding: "Belum ada pembanding independen; sifat struktural (11 kabisat per 30 tahun, siklus 10.631 hari)",
    tes: "bagian dari 47",
    status: "teruji",
  },
  {
    kalender: "Julian",
    pembanding: "Jangkar reformasi Oktober 1582, JD 0, abad ke-3; hari berurutan 4713 SM–2101 M",
    tes: "17",
    status: "teruji",
  },
  {
    kalender: "Maya",
    pembanding: "Prasasti Palenque (Calendar Round cocok dengan Hitungan Panjang); 13.0.0.0.0 = 21 Des 2012 (GMT)",
    tes: "18",
    status: "teruji",
  },
];

const PENGECUALIAN_CHINA = [
  ["24 Apr 1906 (awal bulan), 21 Jan 1909, 23 Nov 1912, 24 Sep 1913 (zhongqi)",
    "HKO mencatat hari berikutnya walaupun menurut efemeris modern momennya 4–27 menit sebelum tengah malam waktu lokal Beijing. Dugaan: mengikuti kalender resmi masa itu. Belum dipastikan."],
  ["28 Sep 2057, 7 Agu 2097 (awal bulan), 19 Mar 2084 (zhongqi)",
    "Momen 0–2 menit setelah tengah malam; HKO sendiri menandai tanggal ini bisa meleset satu hari."],
  ["23 Des 1951, 21 Jan 1979 (zhongqi)", "Momen kurang dari 30 detik sebelum tengah malam."],
] as const;

export default function ValidasiPage() {
  return (
    <main className="mx-auto flex max-w-5xl flex-col gap-12 px-6 py-14">
      <div className="flex max-w-3xl flex-col gap-3">
        <p className="font-caps tracking-[0.14em] text-accent">Validasi</p>
        <h1 className="font-display text-5xl leading-tight">Seberapa bisa dipercaya?</h1>
        <p className="text-lg text-muted">
          Setiap kalender diuji berlapis. Halaman ini menampilkan statusnya apa adanya, termasuk
          yang belum punya pembanding independen. Status per 5 November 2026; total 169 tes.
        </p>
      </div>

      <section aria-labelledby="status" className="flex flex-col gap-4">
        <h2 id="status" className="font-display text-3xl">Status per kalender</h2>
        <div className="overflow-x-auto border border-rule bg-surface">
          <table className="w-full min-w-[720px] border-collapse text-left">
            <thead className="bg-chip font-caps tracking-[0.08em] text-muted">
              <tr>
                <th scope="col" className="px-4 py-3 font-normal">Kalender</th>
                <th scope="col" className="px-4 py-3 font-normal">Pembanding</th>
                <th scope="col" className="px-4 py-3 font-normal">Tes</th>
                <th scope="col" className="px-4 py-3 font-normal">Status</th>
              </tr>
            </thead>
            <tbody>
              {STATUS.map((s) => (
                <tr key={s.kalender} className="border-t border-rule align-top">
                  <th scope="row" className="px-4 py-4 font-serif text-lg font-normal">{s.kalender}</th>
                  <td className="px-4 py-4">{s.pembanding}</td>
                  <td className="px-4 py-4 font-mono">{s.tes}</td>
                  <td className="px-4 py-4">
                    <span className="inline-block border border-current px-2.5 py-0.5 text-sm font-bold whitespace-nowrap text-accent">
                      {s.status === "terverifikasi" ? "✓ Terverifikasi" : "○ Teruji"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-sm text-muted">
          <strong className="text-ink">Terverifikasi</strong>: cocok dengan implementasi atau tabel
          independen. <strong className="text-ink">Teruji</strong>: lolos jangkar dari literatur dan uji
          sifat, tetapi pembanding independen belum ada.
        </p>
      </section>

      <section aria-labelledby="pengecualian" className="flex flex-col gap-4">
        <h2 id="pengecualian" className="font-display text-3xl">Selisih dengan HKO yang terdokumentasi</h2>
        <dl className="flex flex-col">
          {PENGECUALIAN_CHINA.map(([tanggal, alasan]) => (
            <div key={tanggal} className="flex flex-col gap-1 border-b border-rule py-4">
              <dt className="font-serif text-lg">{tanggal}</dt>
              <dd className="text-muted">{alasan}</dd>
            </div>
          ))}
        </dl>
        <p className="text-sm text-muted">
          Satu baris (30 Desember 2069) tidak ada di file teks berbahasa Inggris HKO, tetapi ada di
          versi berbahasa China; tanggal itu tetap ikut diuji.
        </p>
      </section>

      <section aria-labelledby="lapis" className="flex flex-col gap-4">
        <h2 id="lapis" className="font-display text-3xl">Lapis pengujian</h2>
        <ol className="flex flex-wrap gap-5">
          {[
            ["Jangkar", "Tanggal yang sudah pasti dari literatur."],
            ["Berkas acuan", "Ribuan tanggal dari sumber independen, dibekukan dan dicek di setiap commit."],
            ["Uji sifat", "Hari berurutan dan bolak-balik konversi untuk jutaan tanggal."],
            ["Pembanding", "Hasil dicocokkan dengan pustaka atau lembaga lain."],
            ["Tinjauan manusia", "Spesifikasi dibaca ulang terhadap sumber aslinya."],
          ].map(([judul, isi], i) => (
            <li key={judul} className="flex min-w-0 flex-[1_1_11rem] flex-col gap-1 border-t-2 border-ink pt-3">
              <span className="font-mono text-accent">{String(i + 1).padStart(2, "0")}</span>
              <strong className="font-serif text-xl font-normal">{judul}</strong>
              <span className="text-sm text-muted">{isi}</span>
            </li>
          ))}
        </ol>
      </section>

      <section aria-labelledby="sumber" className="flex flex-col gap-3">
        <h2 id="sumber" className="font-display text-3xl">Sumber</h2>
        <ul className="flex list-disc flex-col gap-2 pl-5 text-muted">
          <li>
            Dershowitz &amp; Reingold (1990); Reingold, Dershowitz &amp; Clamen (1993); kode CALENDRICA
            4.0 (Apache-2.0) yang menyertai <em>Calendrical Calculations</em> ed. ke-4 (2018).
          </li>
          <li>ICU (International Components for Unicode), kalender islamic-civil dan islamic-tbla.</li>
          <li>
            Skyfield dan efemeris JPL DE440s untuk momen bulan baru dan zhongqi.
          </li>
          <li>
            Halaman ini memuat informasi yang disalin atau diekstrak dari data yang tersedia di situs
            Hong Kong Observatory (
            <a className="underline" href="https://www.hko.gov.hk/en/gts/time/conversion1_text.htm">
              Gregorian-Lunar Calendar Conversion Table
            </a>
            ), situs yang diterbitkan oleh Observatory. Penyediaan informasi ini bukan bentuk kerja
            sama atau afiliasi dengan Observatory, dan Observatory tidak menyetujui atau
            merekomendasikan Zetalmanac.
          </li>
        </ul>
      </section>
    </main>
  );
}
