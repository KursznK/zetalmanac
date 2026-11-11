import type { Metadata } from "next";
import TanyaForm from "./tanya-form";

export const metadata: Metadata = { title: "Tanya · Zetalmanac" };

export default function TanyaPage() {
  const siteKey = process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY ?? "";

  return (
    <main className="mx-auto flex max-w-3xl flex-col gap-10 px-6 py-14">
      <div className="flex flex-col gap-3">
        <p className="font-caps tracking-[0.14em] text-accent">Tanya</p>
        <h1 className="font-display text-5xl leading-tight">Tanya tentang kalender</h1>
        <p className="text-muted">
          Jawaban disusun oleh model AI hanya dari sumber Zetalmanac (spesifikasi kalender dan artikel Wikipedia
          berlisensi), dengan nomor sumber di setiap fakta. Tanggal dihitung oleh mesin konversi yang sama dengan
          halaman Konversi. Tanggal Hijriah memakai hisab urfi, jadi tanggal resmi bisa berbeda 1–2 hari.
        </p>
        <p className="text-sm text-muted">
          Jangan menulis data pribadi. Pertanyaan diproses oleh Groq dan Cloudflare tanpa disimpan untuk melatih
          model, dan tidak dicatat oleh Zetalmanac.
        </p>
      </div>
      {siteKey ? (
        <TanyaForm siteKey={siteKey} />
      ) : (
        <p className="border border-rule bg-surface p-4">Fitur tanya-jawab belum dikonfigurasi.</p>
      )}
    </main>
  );
}
