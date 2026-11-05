"use client";

import { useSyncExternalStore } from "react";

type Tema = "terang" | "gelap";

// Tema yang sedang berlaku: pilihan pengguna (data-theme) atau pengaturan perangkat.
function temaSekarang(): Tema {
  const pilihan = document.documentElement.dataset.theme;
  if (pilihan === "light") return "terang";
  if (pilihan === "dark") return "gelap";
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "gelap" : "terang";
}

function berlangganan(callback: () => void) {
  const media = window.matchMedia("(prefers-color-scheme: dark)");
  media.addEventListener("change", callback);
  const observer = new MutationObserver(callback);
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  return () => {
    media.removeEventListener("change", callback);
    observer.disconnect();
  };
}

export default function ThemeToggle() {
  // Di server tema belum diketahui (null); di browser dibaca dari <html> dan media query.
  const tema = useSyncExternalStore(berlangganan, temaSekarang, () => null);
  const berikutnya: Tema = tema === "gelap" ? "terang" : "gelap";

  function ganti() {
    const nilai = berikutnya === "gelap" ? "dark" : "light";
    document.documentElement.dataset.theme = nilai;
    try {
      localStorage.setItem("tema", nilai);
    } catch {
      // Penyimpanan diblokir browser: tema tetap berlaku sampai halaman ditutup.
    }
  }

  return (
    <button
      type="button"
      onClick={ganti}
      aria-label={tema ? `Ganti ke tema ${berikutnya}` : "Ganti tema"}
      title={tema ? `Ganti ke tema ${berikutnya}` : "Ganti tema"}
      className="inline-flex size-11 items-center justify-center rounded-full border border-current/40"
    >
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        aria-hidden="true"
      >
        {tema === "gelap" ? (
          <>
            <circle cx="12" cy="12" r="4" />
            <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
          </>
        ) : (
          <path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z" />
        )}
      </svg>
    </button>
  );
}
