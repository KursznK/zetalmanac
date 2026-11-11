import type { ReactNode } from "react";
import { KALENDER } from "@/lib/api";

// Dropdown dengan bingkai dan panah yang seragam di semua browser.
export function SelectField({
  label,
  name,
  defaultValue,
  className = "",
  mono = false,
  pendek = false,
  children,
}: {
  label: string;
  name: string;
  defaultValue: string;
  className?: string;
  mono?: boolean;
  pendek?: boolean;
  children: ReactNode;
}) {
  return (
    <label className={`flex flex-col gap-1.5 text-sm text-muted ${className}`}>
      {label}
      <span className={`field relative flex ${pendek ? "h-11" : "h-12"}`}>
        <select
          name={name}
          defaultValue={defaultValue}
          className={`min-w-0 flex-1 cursor-pointer appearance-none bg-bg pr-10 pl-3 text-base text-ink ${
            mono ? "font-mono" : ""
          }`}
        >
          {children}
        </select>
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
          className="pointer-events-none absolute top-1/2 right-3 -translate-y-1/2 text-muted"
        >
          <path d="M6 9l6 6 6-6" />
        </svg>
      </span>
    </label>
  );
}

// Pilihan "Dari kalender". Atribut name="from" dipakai aturan :has() di globals.css.
export function FromField({ defaultValue, className }: { defaultValue: string; className?: string }) {
  return (
    <SelectField label="Dari kalender" name="from" defaultValue={defaultValue} className={className}>
      {KALENDER.map((k) => (
        <option key={k.id} value={k.id}>
          {k.label}
        </option>
      ))}
    </SelectField>
  );
}

// Contoh format untuk kalender asal yang sedang dipilih. Kelima contoh dirender,
// lalu globals.css (.format-hint) hanya menampilkan yang cocok dengan pilihan.
export function FormatHint() {
  return (
    <span className="format-hint">
      {KALENDER.map((k) => (
        <span key={k.id} data-for={k.id}>
          Contoh format {k.label}: <span className="font-mono text-ink">{k.contoh}</span>
        </span>
      ))}
    </span>
  );
}
