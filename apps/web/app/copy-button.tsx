"use client";

import { useState } from "react";

// Tombol kecil untuk menyalin satu hasil ke papan klip. Ikon berubah jadi centang sebentar.
export default function CopyButton({ teks, label }: { teks: string; label: string }) {
  const [tersalin, setTersalin] = useState(false);

  async function salin() {
    try {
      await navigator.clipboard.writeText(teks);
    } catch {
      return; // Browser menolak akses papan klip: jangan mengaku sudah tersalin.
    }
    setTersalin(true);
    setTimeout(() => setTersalin(false), 1800);
  }

  return (
    <button
      type="button"
      onClick={salin}
      aria-label={label}
      title={label}
      className="ml-auto inline-flex size-9 shrink-0 cursor-pointer items-center justify-center border border-transparent text-muted transition-colors hover:border-rule hover:bg-chip hover:text-accent"
    >
      <svg
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth={tersalin ? 2 : 1.6}
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        {tersalin ? (
          <path d="M5 12.5l4.5 4.5L19 7.5" />
        ) : (
          <>
            <rect x="8.5" y="8.5" width="11" height="11" rx="1.5" />
            <path d="M15.5 8.5v-3A1.5 1.5 0 0 0 14 4H6a1.5 1.5 0 0 0-1.5 1.5V14A1.5 1.5 0 0 0 6 15.5h2.5" />
          </>
        )}
      </svg>
      <span className="sr-only" aria-live="polite">
        {tersalin ? "Tersalin ke papan klip" : ""}
      </span>
    </button>
  );
}
