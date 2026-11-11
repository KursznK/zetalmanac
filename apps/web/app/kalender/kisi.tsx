"use client";

import Link from "next/link";
import { type ReactNode, useState } from "react";
import type { HariBulan } from "@/lib/api";

const NAMA_HARI = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];

// Kisi satu bulan. Komponen klien karena menyimpan tanggal yang sedang dipilih:
// klik sebuah sel menampilkan rinciannya di panel atas, tanpa memanggil API lagi
// (semua data bulan itu sudah dikirim server lewat prop `days`).
export default function Kisi({
  days,
  year,
  month,
  monthName,
  hariIni,
}: {
  days: HariBulan[];
  year: number;
  month: number;
  monthName: string;
  hariIni: number | null;
}) {
  const [pilih, setPilih] = useState(hariIni ?? days[0]?.day ?? 1);
  const p = days.find((h) => h.day === pilih) ?? days[0];
  const kosong = days[0]?.weekday ?? 0;

  return (
    <>
      {p ? (
        <section
          aria-label="Tanggal dipilih"
          aria-live="polite"
          className="border-[3px] border-double border-rule bg-surface p-1.5"
        >
          <div className="flex flex-wrap items-center gap-x-8 gap-y-3.5 px-5 py-3.5">
            <Rinci label="Tanggal Dipilih" className="flex-[1_1_15rem]">
              <span className="text-2xl">
                {NAMA_HARI[p.weekday]}, {p.day} {monthName} {year}
              </span>
            </Rinci>
            <Rinci label="Hijriah · Urfi" className="flex-[1_1_11rem]">
              {p.hijri.day} {p.hijri.month_name} {p.hijri.year} H
            </Rinci>
            <Rinci label="China" className="flex-[1_1_9rem]">
              {p.china
                ? `Bulan ${p.china.month}${p.china.leap ? " kabisat" : ""}, hari ${p.china.day}${
                    p.china.zhongqi ? ` · ${p.china.zhongqi}` : ""
                  }`
                : "—"}
            </Rinci>
            <Rinci label="JDN">
              <span className="font-mono text-[17px]">{p.rd + 1721425}</span>
            </Rinci>
            <Link
              href={`/konversi?from=gregorian&date=${year}-${month}-${p.day}`}
              className="tombol inline-flex h-11 items-center gap-2 bg-btn-bg px-4.5 font-bold text-btn-ink"
            >
              Buka di Konversi{" "}
              <span className="panah" aria-hidden="true">
                →
              </span>
            </Link>
          </div>
        </section>
      ) : null}

      <div className="overflow-x-auto">
        <table className="w-full min-w-[640px] table-fixed border-collapse">
          <thead>
            <tr>
              {NAMA_HARI.map((nama, i) => (
                <th
                  key={nama}
                  scope="col"
                  className={`border border-rule bg-chip px-3 py-2 text-left font-caps text-[15px] font-normal tracking-[0.08em] ${
                    i === 0 ? "text-accent" : "text-muted"
                  }`}
                >
                  {nama}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {baris(days, kosong).map((minggu, i) => (
              <tr key={i}>
                {minggu.map((h, j) =>
                  h ? (
                    <Sel
                      key={j}
                      h={h}
                      hariIni={h.day === hariIni}
                      terpilih={h.day === pilih}
                      label={`${NAMA_HARI[h.weekday]}, ${h.day} ${monthName} ${year}`}
                      onPilih={() => setPilih(h.day)}
                    />
                  ) : (
                    <td key={j} className="border border-rule bg-chip" />
                  ),
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

function Rinci({
  label,
  className = "",
  children,
}: {
  label: string;
  className?: string;
  children: ReactNode;
}) {
  return (
    <div className={`min-w-0 ${className}`}>
      <p className="font-caps text-sm tracking-[0.08em] text-muted">{label}</p>
      <p className="font-serif text-[19px]">{children}</p>
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

function Sel({
  h,
  hariIni,
  terpilih,
  label,
  onPilih,
}: {
  h: HariBulan;
  hariIni: boolean;
  terpilih: boolean;
  label: string;
  onPilih: () => void;
}) {
  const awalHijri = h.hijri.day === 1;
  const awalChina = h.china?.day === 1;
  const angka = hariIni
    ? "-mt-0.5 -ml-1 bg-btn-bg px-2 py-0.5 text-btn-ink"
    : h.weekday === 0
      ? "text-accent"
      : "";
  return (
    <td aria-current={hariIni ? "date" : undefined} className="h-28 border border-rule p-0 align-top">
      <button
        type="button"
        onClick={onPilih}
        aria-pressed={terpilih}
        aria-label={label}
        className={`flex size-full min-h-28 cursor-pointer flex-col gap-0.5 bg-surface p-2 text-left transition-colors hover:bg-chip ${
          terpilih ? "shadow-[inset_0_0_0_2px_var(--btn-bg)]" : ""
        }`}
      >
        <span className="flex items-start justify-between gap-1">
          <span className={`font-display text-3xl leading-none ${angka}`}>{h.day}</span>
          {h.china?.zhongqi ? (
            <span className="text-xs text-accent" title={`Zhongqi ${h.china.zhongqi}`}>
              ● {h.china.zhongqi}
            </span>
          ) : hariIni ? (
            <span className="text-xs text-accent">Hari ini</span>
          ) : null}
        </span>
        <span className={`mt-auto text-[13px] ${awalHijri ? "font-bold text-ink" : "text-muted"}`}>
          {awalHijri ? `1 ${h.hijri.month_name}` : h.hijri.day}
        </span>
        <span className={`text-[13px] ${awalChina ? "font-bold text-ink" : "text-muted"}`}>
          {h.china ? h.china.label : ""}
        </span>
      </button>
    </td>
  );
}
