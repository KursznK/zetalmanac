"use client";

import { type ChangeEvent, useRef } from "react";

// Kolom "Tanggal" dengan ikon kalender.
// Kolom teksnya tetap bebas diketik (format Maya "13.0.14.1.7" atau tahun negatif tidak bisa
// diwakili <input type="date">). Ikon di kanan adalah <input type="date"> transparan: saat
// diklik, browser menampilkan pemilih tanggalnya sendiri. Tanggal yang dipilih selalu Gregorian,
// jadi kolom teks diisi dan "Dari kalender" dipindah ke Gregorian.
export default function DateField({
  defaultValue,
  className = "",
}: {
  defaultValue: string;
  className?: string;
}) {
  const teks = useRef<HTMLInputElement>(null);

  function pilih(e: ChangeEvent<HTMLInputElement>) {
    const nilai = e.currentTarget.value; // "TTTT-BB-HH", atau "" kalau dikosongkan
    if (!nilai || !teks.current) return;
    teks.current.value = nilai;
    const dari = e.currentTarget.form?.elements.namedItem("from");
    if (dari instanceof HTMLSelectElement) dari.value = "gregorian";
  }

  return (
    <div className={`flex flex-col gap-1.5 text-sm text-muted ${className}`}>
      <label htmlFor="tanggal">Tanggal</label>
      <div className="field flex h-12">
        <input
          ref={teks}
          id="tanggal"
          name="date"
          defaultValue={defaultValue}
          maxLength={20}
          required
          autoComplete="off"
          className="min-w-0 flex-1 bg-transparent px-3 font-mono text-base text-ink"
        />
        <span
          title="Pilih dari kalender (Gregorian)"
          className="relative flex w-12 shrink-0 items-center justify-center border-l border-rule text-muted transition-colors focus-within:bg-chip focus-within:text-accent hover:bg-chip hover:text-accent"
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.6"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <rect x="3.5" y="5" width="17" height="15.5" rx="1.5" />
            <path d="M3.5 10h17M8 3v4M16 3v4" />
            <path d="M7.5 13.5h2M11 13.5h2M14.5 13.5h2M7.5 17h2M11 17h2" />
          </svg>
          {/* Tanpa atribut name, jadi nilainya tidak ikut terkirim bersama formulir. */}
          <input
            type="date"
            min="0001-01-01"
            max="9999-12-31"
            aria-label="Pilih tanggal Gregorian dari kalender"
            onChange={pilih}
            className="date-pick absolute inset-0 size-full cursor-pointer opacity-0"
          />
        </span>
      </div>
    </div>
  );
}
