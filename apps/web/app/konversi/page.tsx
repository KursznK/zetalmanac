import type { Metadata } from "next";
import { KALENDER, konversi, type HasilKonversi, type Kalender, type Langkah } from "@/lib/api";
import CopyButton from "../copy-button";
import DateField from "../date-field";
import { FormatHint, FromField, SelectField } from "../form-fields";

export const metadata: Metadata = { title: "Konversi · Zetalmanac" };

function satu(nilai: string | string[] | undefined): string | undefined {
  return Array.isArray(nilai) ? nilai[0] : nilai;
}

function pilih<T extends string>(nilai: string | undefined, pilihan: readonly T[], bawaan: T): T {
  return pilihan.includes(nilai as T) ? (nilai as T) : bawaan;
}

function hariIniDiJakarta(): string {
  // en-CA menghasilkan format TAHUN-BULAN-TANGGAL
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Jakarta" }).format(new Date());
}

const SKEMA = ["I", "II", "III", "IV"] as const;
const EPOCH = ["civil", "astronomical"] as const;
const KORELASI = ["584283", "584285", "584286"] as const;
const ID_KALENDER = KALENDER.map((k) => k.id);

export default async function KonversiPage(props: PageProps<"/konversi">) {
  const sp = await props.searchParams;
  const tanggal = satu(sp.date)?.trim();
  const opsi = {
    from: tanggal ? pilih<Kalender>(satu(sp.from), ID_KALENDER, "gregorian") : "gregorian",
    date: tanggal || hariIniDiJakarta(),
    scheme: pilih(satu(sp.scheme), SKEMA, "II"),
    epoch: pilih(satu(sp.epoch), EPOCH, "civil"),
    correlation: pilih(satu(sp.correlation), KORELASI, "584283"),
    leap: satu(sp.leap) === "true",
    afterSunset: satu(sp.after_sunset) === "true",
  } as const;
  const hasil = await konversi({ ...opsi, steps: true });

  return (
    <main className="mx-auto flex max-w-5xl flex-col gap-10 px-6 py-14">
      <div className="flex flex-col gap-2">
        <p className="font-caps tracking-[0.14em] text-accent">Konversi</p>
        <h1 className="font-display text-[2.5rem] leading-tight sm:text-5xl">Konversi Tanggal</h1>
      </div>

      {/* key: kalau alamat berubah (mis. dari tautan "Berikutnya"), isi formulir ikut diperbarui */}
      <form
        key={JSON.stringify(opsi)}
        method="get"
        action="/konversi"
        className="border-[3px] border-double border-rule bg-surface p-1.5"
      >
        <div className="flex flex-wrap items-end gap-4 border-b border-rule p-5">
          <DateField defaultValue={opsi.date} className="flex-[2_1_14rem]" />
          <FromField defaultValue={opsi.from} className="flex-[1_1_11rem]" />
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
        <p className="px-5 pt-3 text-sm text-muted">
          <FormatHint /> · Tahun SM ditulis negatif secara astronomis, contoh: 44 SM ={" "}
          <span className="font-mono text-ink">-43</span>.
        </p>
        <div className="flex flex-wrap items-end gap-x-8 gap-y-4 p-5">
          <SelectField label="Skema kabisat urfi" name="scheme" defaultValue={opsi.scheme} pendek>
            {SKEMA.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </SelectField>
          <SelectField label="Epoch Hijriah" name="epoch" defaultValue={opsi.epoch} pendek>
            <option value="civil">Sipil (16 Juli 622 J)</option>
            <option value="astronomical">Astronomis (15 Juli 622 J)</option>
          </SelectField>
          <SelectField label="Korelasi Maya" name="correlation" defaultValue={opsi.correlation} pendek mono>
            {KORELASI.map((k) => (
              <option key={k} value={k}>
                {k}
              </option>
            ))}
          </SelectField>
          <div className="flex flex-col justify-end gap-1">
            <label className="sunset-field flex min-h-11 cursor-pointer items-center gap-2">
              <input
                type="checkbox"
                name="after_sunset"
                value="true"
                defaultChecked={opsi.afterSunset}
                className="size-[18px] accent-btn-bg"
              />
              Setelah magrib
            </label>
            <label className="leap-field min-h-11 cursor-pointer items-center gap-2">
              <input
                type="checkbox"
                name="leap"
                value="true"
                defaultChecked={opsi.leap}
                className="size-[18px] accent-btn-bg"
              />
              Bulan kabisat
            </label>
          </div>
        </div>
      </form>

      {hasil.ok ? (
        <Hasil data={hasil.data} asal={opsi.from} />
      ) : (
        <p role="alert" className="border border-accent bg-surface p-5 text-ink">
          {hasil.pesan}
        </p>
      )}
    </main>
  );
}

function Kartu({
  judul,
  utama,
  catatan,
  asal = false,
}: {
  judul: string;
  utama: string;
  catatan?: string;
  asal?: boolean;
}) {
  return (
    <div className="kartu-angkat flex min-w-0 flex-[1_1_17.5rem] flex-col gap-1 border border-rule bg-surface pt-3.5 pr-3.5 pb-4.5 pl-5">
      <div className="flex min-h-9 items-center gap-2.5">
        <h3 className="font-caps tracking-[0.08em] text-muted">{judul}</h3>
        {asal ? (
          <span className="border border-accent px-2 text-xs leading-normal font-bold text-accent">Asal</span>
        ) : null}
        <CopyButton teks={utama} label={`Salin hasil ${judul}`} />
      </div>
      <p className="pr-1.5 font-serif text-[22px] leading-snug">{utama}</p>
      {catatan ? <p className="pr-1.5 text-sm text-muted">{catatan}</p> : null}
    </div>
  );
}

function Hasil({ data, asal }: { data: HasilKonversi; asal: Kalender }) {
  const { gregorian, julian, hijri, china, maya } = data;
  return (
    <section aria-labelledby="hasil" className="flex flex-col gap-4">
      <h2 id="hasil" className="font-display text-3xl">
        Hasil
      </h2>
      <div className="flex flex-wrap gap-4">
        <Kartu judul="Gregorian" utama={`${data.hari}, ${gregorian.label}`} asal={asal === "gregorian"} />
        <Kartu judul="Julian" utama={julian.label} asal={asal === "julian"} />
        <Kartu
          judul="Hijriah · Urfi"
          utama={hijri.label}
          catatan={`Skema ${hijri.scheme}, Epoch ${hijri.epoch === "civil" ? "Sipil" : "Astronomis"}${
            hijri.after_sunset ? ", setelah magrib" : ""
          }`}
          asal={asal === "hijri"}
        />
        <Kartu
          judul="China"
          utama={china ? `${china.label} · ${china.year_ganzhi}` : "—"}
          catatan={
            china
              ? `Tahun ${china.year_label} · bulan ${china.month}${china.leap ? " kabisat" : ""} hari ${china.day} · hari ${china.day_ganzhi}`
              : "Hanya tersedia untuk 1901–2100."
          }
          asal={asal === "china"}
        />
        <Kartu
          judul="Maya"
          utama={maya.long_count}
          catatan={`${maya.tzolkin} · ${maya.haab} · ${maya.lord_of_night} · Korelasi ${maya.correlation}`}
          asal={asal === "maya"}
        />
        <Kartu judul="Hitungan Hari" utama={`JDN ${data.jdn}`} catatan={`RD ${data.rd} · Rata Die`} />
      </div>
      {data.steps ? (
        <details className="border border-rule bg-surface">
          <summary className="flex cursor-pointer items-center gap-2.5 px-5 py-4 font-display text-2xl transition-colors hover:bg-chip">
            <svg
              className="chev"
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M9 6l6 6-6 6" />
            </svg>
            Tunjukkan langkah
          </summary>
          <div className="flex flex-wrap border-t border-rule">
            {data.steps.gregorian ? (
              <BlokLangkah judul="Gregorian → RD" langkah={data.steps.gregorian} />
            ) : null}
            <BlokLangkah judul={`RD → Hijriah urfi (skema ${hijri.scheme})`} langkah={data.steps.hijri} />
            <BlokLangkah judul={`RD → Maya (korelasi ${maya.correlation})`} langkah={data.steps.maya} />
          </div>
          <p className="border-t border-rule px-5 py-3 text-sm text-muted">
            Rumus mengikuti Reingold &amp; Dershowitz, <em>Calendrical Calculations</em>. Setiap langkah
            dihitung ulang dan dicocokkan dengan jawaban di atas.
          </p>
        </details>
      ) : null}
    </section>
  );
}

function BlokLangkah({ judul, langkah }: { judul: string; langkah: Langkah[] }) {
  return (
    <div className="flex min-w-0 flex-[1_1_20rem] flex-col gap-3 p-5">
      <h3 className="font-serif text-xl">{judul}</h3>
      <ol className="flex list-decimal flex-col gap-3 pl-6">
        {langkah.map((l) => (
          <li key={l.judul}>
            <span>{l.judul}</span>
            {l.baris.map((b) => (
              <code key={b} className="mt-1 block overflow-x-auto font-mono text-[15px] whitespace-pre text-accent">
                {b}
              </code>
            ))}
          </li>
        ))}
      </ol>
    </div>
  );
}
