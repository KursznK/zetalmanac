import Link from "next/link";
import HealthBadge from "./health-badge";

export default function Home() {
  return (
    <main className="mx-auto flex max-w-5xl flex-col gap-6 px-6 py-20">
      <p className="font-caps tracking-[0.14em] text-accent">konverter kalender · almanak terbuka</p>
      <h1 className="font-display text-6xl leading-tight">Satu hari, lima cara menghitungnya.</h1>
      <p className="max-w-[34em] text-lg text-muted">
        Ubah tanggal antara Gregorian, Julian, Hijriah (hisab urfi), China, dan Maya, lengkap dengan
        varian dan sumbernya.
      </p>
      <Link
        href="/konversi"
        className="inline-flex h-12 items-center self-start bg-btn-bg px-6 font-bold text-btn-ink"
      >
        Buka konverter
      </Link>
      <HealthBadge />
    </main>
  );
}
