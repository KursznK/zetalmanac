import Link from "next/link";

const NAV = [
  { href: "/", label: "Beranda" },
  { href: "/konversi", label: "Konversi" },
] as const;

export default function SiteHeader() {
  return (
    <header className="bg-head-bg text-head-ink">
      <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-4 px-6 py-3">
        <Link href="/" className="flex min-h-11 items-center gap-3">
          <svg width="32" height="32" viewBox="0 0 34 34" aria-hidden="true">
            <circle cx="17" cy="17" r="15" fill="none" stroke="currentColor" strokeWidth="1.4" />
            <path d="M17 2 A15 15 0 0 1 17 32 A9 15 0 0 0 17 2 Z" fill="currentColor" />
          </svg>
          <span className="font-display text-2xl">Zetalmanac</span>
        </Link>
        <nav aria-label="Navigasi utama" className="flex flex-wrap gap-1">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="inline-flex min-h-11 items-center px-3 hover:underline hover:underline-offset-4"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
