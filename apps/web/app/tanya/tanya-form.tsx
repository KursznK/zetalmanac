"use client";

import Script from "next/script";
import { type FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { MAKS_KARAKTER, kirimPertanyaan, type HasilTanya, type Sumber } from "@/lib/tanya";
import TeksJawaban from "./teks-jawaban";

// Cloudflare Turnstile, dirender secara eksplisit supaya bisa di-reset setelah setiap
// pertanyaan (token hanya berlaku sekali dan selama 5 menit).
type Turnstile = {
  render: (
    el: HTMLElement,
    opsi: {
      sitekey: string;
      callback: (token: string) => void;
      "expired-callback": () => void;
      "error-callback": () => void;
      theme: "auto";
      language: string;
    },
  ) => string;
  reset: (id: string) => void;
  remove: (id: string) => void;
};

declare global {
  interface Window {
    turnstile?: Turnstile;
  }
}

const CONTOH = [
  "Kapan tahun kabisat dalam hisab urfi?",
  "1 Ramadan 1448 H jatuh pada tanggal berapa Masehi?",
  "Bagaimana bulan kabisat ditentukan dalam kalender China?",
  "What is the Maya Calendar Round?",
];

function DaftarSumber({ sumber }: { sumber: Sumber[] }) {
  if (sumber.length === 0) return null;
  return (
    <div className="flex flex-col gap-2 border-t border-rule pt-4">
      <h3 className="font-caps text-sm tracking-[0.14em] text-muted">sumber</h3>
      <ol className="flex flex-col gap-3 text-sm">
        {sumber.map((s) => (
          <li key={s.nomor} id={`sumber-${s.nomor}`} className="flex flex-col gap-0.5">
            <span>
              [{s.nomor}]{" "}
              <a href={s.url} target="_blank" rel="noopener noreferrer nofollow" className="underline underline-offset-2">
                {s.judul}
              </a>
              <span className="text-muted"> › {s.bagian.split(" › ").slice(1).join(" › ") || "pembuka"}</span>
            </span>
            {s.cuplikan && <span className="text-muted">{s.cuplikan}…</span>}
            <span className="text-xs text-muted">{s.atribusi}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}

function Hasil({ hasil }: { hasil: HasilTanya }) {
  switch (hasil.status) {
    case "dijawab":
    case "tidak_ditemukan": {
      const nomorSah = new Set(hasil.sumber.map((s) => s.nomor));
      const pakaiTool = hasil.tool.some((t) => t.nama === "konversi_tanggal");
      return (
        <div className="flex flex-col gap-4">
          <TeksJawaban teks={hasil.jawaban} nomorSah={nomorSah} />
          {pakaiTool && (
            <p className="text-sm text-muted">
              Tanggal dihitung oleh mesin konversi Zetalmanac, bukan oleh model AI.
            </p>
          )}
          <DaftarSumber sumber={hasil.sumber} />
          <p className="text-xs text-muted">
            Dijawab oleh model AI ({hasil.model}) dari sumber di atas dalam {hasil.detik.toFixed(1)} detik. Periksa
            sumbernya untuk hal penting.
          </p>
        </div>
      );
    }
    case "cadangan":
      return (
        <div className="flex flex-col gap-4">
          <p>{hasil.pesan}</p>
          <DaftarSumber sumber={hasil.sumber} />
        </div>
      );
    default:
      return <p>{hasil.pesan}</p>;
  }
}

export default function TanyaForm({ siteKey }: { siteKey: string }) {
  const [pertanyaan, setPertanyaan] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [memuat, setMemuat] = useState(false);
  const [hasil, setHasil] = useState<HasilTanya | null>(null);
  const [galat, setGalat] = useState<string | null>(null);
  const wadah = useRef<HTMLDivElement>(null);
  const widgetId = useRef<string | null>(null);

  // Dipanggil next/script setiap kali skrip siap, termasuk saat kembali ke halaman ini.
  const pasangWidget = useCallback(() => {
    if (!window.turnstile || !wadah.current || widgetId.current) return;
    widgetId.current = window.turnstile.render(wadah.current, {
      sitekey: siteKey,
      callback: setToken,
      "expired-callback": () => setToken(null),
      "error-callback": () => setToken(null),
      theme: "auto",
      language: "id",
    });
  }, [siteKey]);

  // Pasang widget kalau skrip sudah ada (mis. Strict Mode memasang efek dua kali di mode dev),
  // dan lepas widget saat meninggalkan halaman.
  useEffect(() => {
    pasangWidget();
    return () => {
      if (widgetId.current) window.turnstile?.remove(widgetId.current);
      widgetId.current = null;
    };
  }, [pasangWidget]);

  const kirim = useCallback(
    async (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      if (!token || memuat) return;
      setMemuat(true);
      setGalat(null);
      const resp = await kirimPertanyaan(pertanyaan, token);
      // Token sudah terpakai: minta token baru untuk pertanyaan berikutnya.
      setToken(null);
      if (widgetId.current) window.turnstile?.reset(widgetId.current);
      if (resp.ok) setHasil(resp.data);
      else {
        setHasil(null);
        setGalat(resp.pesan);
      }
      setMemuat(false);
    },
    [pertanyaan, token, memuat],
  );

  const sisa = MAKS_KARAKTER - pertanyaan.length;

  return (
    <div className="flex flex-col gap-8">
      <Script
        src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"
        strategy="afterInteractive"
        onReady={pasangWidget}
      />
      <form onSubmit={kirim} className="border-[3px] border-double border-rule bg-surface p-1.5">
        <div className="flex flex-col gap-4 p-5">
          <label className="flex flex-col gap-1.5 text-sm text-muted">
            Pertanyaanmu tentang kalender
            <textarea
              value={pertanyaan}
              onChange={(e) => setPertanyaan(e.target.value)}
              maxLength={MAKS_KARAKTER}
              rows={3}
              required
              placeholder={CONTOH[0]}
              className="border border-rule bg-bg p-3 text-base text-ink"
            />
          </label>
          <div className="flex flex-wrap gap-2">
            {CONTOH.map((c) => (
              <button
                key={c}
                type="button"
                onClick={() => setPertanyaan(c)}
                className="min-h-11 border border-rule bg-chip px-3 text-left text-sm hover:underline"
              >
                {c}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div ref={wadah} />
            <div className="flex items-center gap-4">
              <span className="text-sm text-muted" aria-live="polite">
                {sisa} karakter tersisa
              </span>
              <button
                type="submit"
                disabled={!token || memuat || !pertanyaan.trim()}
                className="min-h-11 bg-btn-bg px-5 text-btn-ink disabled:opacity-50"
              >
                {memuat ? "Mencari jawaban…" : "Tanya"}
              </button>
            </div>
          </div>
        </div>
      </form>

      <section aria-live="polite" className="flex flex-col gap-4">
        {galat && <p className="border border-rule bg-surface p-4">{galat}</p>}
        {hasil && (
          <div className="border border-rule bg-surface p-6">
            <Hasil hasil={hasil} />
          </div>
        )}
      </section>
    </div>
  );
}
