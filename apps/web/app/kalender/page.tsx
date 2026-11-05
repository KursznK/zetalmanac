import type { Metadata } from "next";
import Link from "next/link";
import { bulan, type HariBulan } from "@/lib/api";

export const metadata: Metadata = { title: "Kalender · Zetalmanac" };

const NAMA_HARI = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];

function satu(nilai: string | string[] | undefined): string | undefined {
  return Array.isArray(nilai) ? nilai[0] : nilai;
}

function hariIniDiJakarta(): { year: number; month: number; day: number } {
  const [y, m, d] = new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Jakarta" })
    .format(new Date())
    .split("-")
    .map(Number);
  return { year: y, month: m, day: d };
}

function bulanTetangga(year: number, month: number, langkah: -1 | 1) {
  const m = month + langkah;
  if (m < 1) return { year: year - 1, month: 12 };
  if (m > 12) return { year: year + 1, month: 1 };
  return { year, month: m };
}

function rentang(nama: string[]): string {
  const unik = nama.filter((n, i) => n !== nama[i - 1]);
  return unik.length > 1 ? `${unik[0]} – ${unik[unik.length - 1]}` : unik[0];
}

export default async function KalenderPage(props: PageProps<"/kalender">) {
  const sp = await props.searchParams;
  const hariIni = hariIniDiJakarta();
  const year = Number.parseInt(satu(sp.year) ?? "", 10);
  const month = Number.parseInt(satu(sp.month) ?? "", 10);
  const pilihan = Number.isInteger(year) && Number.isInteger(month)
    ? { year, month }
    : { year: hariIni.year, month: hariIni.month };
  const hasil = await bulan(pilihan.year, pilihan.month);
  const sebelum = bulanTetangga(pilihan.year, pilihan.month, -1);
  const sesudah = bulanTetangga(pilihan.year, pilihan.month, 1);

  return (
    <main className="mx-auto flex max-w-5xl flex-col gap-8 px-6 py-14">
      <div className="flex flex-wrap items-end justify-between gap-5">
        <div className="flex flex-col gap-1.5">
          <p className="font-caps tracking-[0.14em] text-accent">kalender bulanan</p>
          <h1 className="font-display text-5xl leading-tight">
            {hasil.ok ? `${hasil.data.month_name} ${pilihan.year}` : "Kalender"}
          </h1>
          {hasil.ok ? (
            <p className="text-muted">
              {rentang(hasil.data.days.map((h) => `${h.hijri.month_name} ${h.hijri.year} H`))}
            </p>
          ) : null}
        </div>
        <nav aria-label="Pindah bulan" className="flex gap-2">
          <Link
            href={`/kalender?year=${sebelum.year}&month=${sebelum.month}`}
            className="inline-flex h-11 items-center border border-rule bg-surface px-4"
          >
            ← Sebelumnya
          </Link>
          <Link href="/kalender" className="inline-flex h-11 items-center border border-rule bg-surface px-4">
            Bulan ini
          </Link>
          <Link
            href={`/kalender?year=${sesudah.year}&month=${sesudah.month}`}
            className="inline-flex h-11 items-center border border-rule bg-surface px-4"
          >
            Berikutnya →
          </Link>
        </nav>
      </div>

      {hasil.ok ? (
        <Kisi
          days={hasil.data.days}
          hariIni={
            hariIni.year === pilihan.year && hariIni.month === pilihan.month ? hariIni.day : null
          }
        />
      ) : (
        <p role="alert" className="border border-accent bg-surface p-5">
          {hasil.pesan}
        </p>
      )}

      <p className="text-sm text-muted">
        Baris kedua tiap sel: tanggal Hijriah urfi (skema II, epoch sipil), berlaku untuk siang hari;
        setelah magrib sudah tanggal berikutnya. Baris ketiga: tanggal China (nama bulan muncul di
        awal bulan). Tanda ● menandai zhongqi.
      </p>
    </main>
  );
}

function Kisi({ days, hariIni }: { days: HariBulan[]; hariIni: number | null }) {
  const kosong = days[0]?.weekday ?? 0;
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[640px] table-fixed border-collapse">
        <thead>
          <tr>
            {NAMA_HARI.map((nama) => (
              <th
                key={nama}
                scope="col"
                className="border border-rule bg-chip px-3 py-2 text-left font-caps text-[15px] font-normal tracking-[0.08em] text-muted"
              >
                {nama.toLowerCase()}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {baris(days, kosong).map((minggu, i) => (
            <tr key={i}>
              {minggu.map((h, j) =>
                h ? (
                  <Sel key={j} h={h} hariIni={h.day === hariIni} />
                ) : (
                  <td key={j} className="border border-rule bg-chip" />
                ),
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function baris(days: HariBulan[], kosong: number): (HariBulan | null)[][] {
  const sel: (HariBulan | null)[] = [...Array<null>(kosong).fill(null), ...days];
  while (sel.length % 7 !== 0) sel.push(null);
  const hasil: (HariBulan | null)[][] = [];
  for (let i = 0; i < sel.length; i += 7) hasil.push(sel.slice(i, i + 7));
  return hasil;
}

function Sel({ h, hariIni }: { h: HariBulan; hariIni: boolean }) {
  const hijri = h.hijri.day === 1 ? `1 ${h.hijri.month_name}` : String(h.hijri.day);
  return (
    <td
      aria-current={hariIni ? "date" : undefined}
      className={`h-28 border border-rule bg-surface p-2 align-top ${hariIni ? "outline-2 -outline-offset-2 outline-ink" : ""}`}
    >
      <div className="flex h-full flex-col gap-0.5">
        <div className="flex items-start justify-between">
          <span className="font-display text-3xl leading-none">{h.day}</span>
          {h.china?.zhongqi ? (
            <span className="text-xs text-accent" title={`Zhongqi ${h.china.zhongqi}`}>
              ● {h.china.zhongqi}
            </span>
          ) : null}
        </div>
        <span className="mt-auto text-[13px] text-muted">{hijri}</span>
        <span className="text-[13px] text-muted">{h.china ? h.china.label : ""}</span>
      </div>
    </td>
  );
}
