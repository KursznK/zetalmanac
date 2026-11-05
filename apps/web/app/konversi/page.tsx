import type { Metadata } from "next";
import { KALENDER, konversi, type HasilKonversi, type Kalender, type Langkah } from "@/lib/api";

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
        <p className="font-caps tracking-[0.14em] text-accent">konversi</p>
        <h1 className="font-display text-5xl leading-tight">Konversi tanggal</h1>
      </div>

      <form method="get" action="/konversi" className="border-[3px] border-double border-rule bg-surface p-1.5">
        <div className="flex flex-wrap items-end gap-4 border-b border-rule p-5">
          <label className="flex flex-[2_1_14rem] flex-col gap-1.5 text-sm text-muted">
            Tanggal
            <input
              name="date"
              defaultValue={opsi.date}
              maxLength={20}
              required
              className="h-12 border border-rule bg-bg px-3 font-mono text-base text-ink"
            />
          </label>
          <label className="flex flex-[1_1_11rem] flex-col gap-1.5 text-sm text-muted">
            Dari kalender
            <select name="from" defaultValue={opsi.from} className="h-12 border border-rule bg-bg px-3 text-base text-ink">
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
        <p className="px-5 pt-3 text-sm text-muted">
          Format: {KALENDER.map((k) => `${k.label} ${k.contoh}`).join(" · ")}. Tahun SM ditulis negatif
          secara astronomis: 44 SM = -43.
        </p>
        <div className="flex flex-wrap gap-x-8 gap-y-4 p-5">
          <label className="flex flex-col gap-1.5 text-sm text-muted">
            Skema kabisat urfi
            <select name="scheme" defaultValue={opsi.scheme} className="h-11 border border-rule bg-bg px-3 text-base text-ink">
              {SKEMA.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </label>
          <label className="flex flex-col gap-1.5 text-sm text-muted">
            Epoch Hijriah
            <select name="epoch" defaultValue={opsi.epoch} className="h-11 border border-rule bg-bg px-3 text-base text-ink">
              <option value="civil">Sipil (16 Juli 622 J)</option>
              <option value="astronomical">Astronomis (15 Juli 622 J)</option>
            </select>
          </label>
          <label className="flex flex-col gap-1.5 text-sm text-muted">
            Korelasi Maya
            <select
              name="correlation"
              defaultValue={opsi.correlation}
              className="h-11 border border-rule bg-bg px-3 font-mono text-base text-ink"
            >
              {KORELASI.map((k) => (
                <option key={k} value={k}>
                  {k}
                </option>
              ))}
            </select>
          </label>
          <div className="flex flex-col justify-end gap-1">
            <label className="sunset-field flex min-h-9 items-center gap-2">
              <input type="checkbox" name="after_sunset" value="true" defaultChecked={opsi.afterSunset} className="size-[18px]" />
              Setelah magrib
            </label>
            <label className="leap-field min-h-9 items-center gap-2">
              <input type="checkbox" name="leap" value="true" defaultChecked={opsi.leap} className="size-[18px]" />
              Bulan kabisat
            </label>
          </div>
        </div>
      </form>

      {hasil.ok ? (
        <Hasil data={hasil.data} />
      ) : (
        <p role="alert" className="border border-accent bg-surface p-5 text-ink">
          {hasil.pesan}
        </p>
      )}
    </main>
  );
}

function Kartu({ judul, utama, catatan }: { judul: string; utama: string; catatan?: string }) {
  return (
    <div className="flex min-w-0 flex-[1_1_13rem] flex-col gap-1.5 border border-rule bg-surface p-5">
      <h3 className="font-caps tracking-[0.08em] text-muted">{judul}</h3>
      <p className="font-serif text-[22px] leading-snug">{utama}</p>
      {catatan ? <p className="text-sm text-muted">{catatan}</p> : null}
    </div>
  );
}

function Hasil({ data }: { data: HasilKonversi }) {
  const { gregorian, julian, hijri, china, maya } = data;
  return (
    <section aria-labelledby="hasil" className="flex flex-col gap-4">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 id="hasil" className="font-display text-3xl">
          Hasil
        </h2>
        <p className="font-mono text-sm text-muted">
          RD {data.rd} · JDN {data.jdn}
        </p>
      </div>
      <div className="flex flex-wrap gap-4">
        <Kartu judul="gregorian" utama={`${data.hari}, ${gregorian.label}`} />
        <Kartu judul="julian" utama={julian.label} />
        <Kartu
          judul="hijriah · urfi"
          utama={hijri.label}
          catatan={`Skema ${hijri.scheme}, epoch ${hijri.epoch === "civil" ? "sipil" : "astronomis"}${
            hijri.after_sunset ? ", setelah magrib" : ""
          }`}
        />
        <Kartu
          judul="china"
          utama={china ? `${china.label} · ${china.year_ganzhi}` : "—"}
          catatan={
            china
              ? `Tahun ${china.year_label} · bulan ${china.month}${china.leap ? " kabisat" : ""} hari ${china.day} · hari ${china.day_ganzhi}`
              : "Hanya tersedia untuk 1901–2100."
          }
        />
        <Kartu
          judul="maya"
          utama={maya.long_count}
          catatan={`${maya.tzolkin} · ${maya.haab} · ${maya.lord_of_night} · korelasi ${maya.correlation}`}
        />
      </div>
      {data.steps ? (
        <details className="border border-rule bg-surface">
          <summary className="cursor-pointer px-5 py-4 font-display text-2xl">Tunjukkan langkah</summary>
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
