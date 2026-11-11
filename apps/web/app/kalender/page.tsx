import type { Metadata } from "next";
import Link from "next/link";
import { bulan } from "@/lib/api";
import Kisi from "./kisi";

export const metadata: Metadata = { title: "Kalender · Zetalmanac" };

const TOMBOL_NAV =
  "inline-flex h-11 items-center border border-rule bg-surface px-4 transition-colors hover:border-muted hover:bg-chip";

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
    <main className="mx-auto flex max-w-5xl flex-col gap-7 px-6 py-14">
      <div className="flex flex-wrap items-end justify-between gap-5">
        <div className="flex flex-col gap-1.5">
          <p className="font-caps tracking-[0.14em] text-accent">Kalender Bulanan</p>
          <h1 className="font-display text-[2.5rem] leading-tight sm:text-5xl">
            {hasil.ok ? `${hasil.data.month_name} ${pilihan.year}` : "Kalender"}
          </h1>
          {hasil.ok ? (
            <p className="text-muted">
              {rentang(hasil.data.days.map((h) => `${h.hijri.month_name} ${h.hijri.year} H`))}
            </p>
          ) : null}
        </div>
        <nav aria-label="Pindah bulan" className="flex flex-wrap gap-2">
          <Link href={`/kalender?year=${sebelum.year}&month=${sebelum.month}`} className={TOMBOL_NAV}>
            ← Sebelumnya
          </Link>
          <Link href="/kalender" className={TOMBOL_NAV}>
            Bulan ini
          </Link>
          <Link href={`/kalender?year=${sesudah.year}&month=${sesudah.month}`} className={TOMBOL_NAV}>
            Berikutnya →
          </Link>
        </nav>
      </div>

      {hasil.ok ? (
        // key: pindah bulan memulai ulang pilihan tanggal (kembali ke hari ini atau tanggal 1)
        <Kisi
          key={`${pilihan.year}-${pilihan.month}`}
          days={hasil.data.days}
          year={pilihan.year}
          month={pilihan.month}
          monthName={hasil.data.month_name}
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
        Klik sebuah tanggal untuk melihat rinciannya. Baris kedua tiap sel adalah tanggal Hijriah urfi
        (skema II, epoch sipil), berlaku untuk siang hari, dan setelah magrib sudah masuk ke tanggal
        berikutnya. Baris ketiga adalah tanggal China (nama bulan muncul di awal bulan). Tanda ●
        menandai <em>zhongqi</em>.
      </p>
    </main>
  );
}
