import HealthBadge from "./health-badge";

export default function Home() {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col justify-center gap-6 px-6">
      <p className="text-xs uppercase tracking-[0.3em] text-neutral-500">
        Alat · Konversi Kalender
      </p>
      <h1 className="text-5xl font-semibold">Zetalmanac</h1>
      <p className="text-lg text-neutral-600 dark:text-neutral-300">
        Konverter tanggal antar sistem kalender. Sedang dibangun: Gregorian, Julian,
        Hijriah urfi, China, dan Maya.
      </p>
      <HealthBadge />
    </main>
  );
}
