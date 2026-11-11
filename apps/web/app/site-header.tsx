import Link from "next/link";
import NavLinks from "./nav-links";
import ThemeToggle from "./theme-toggle";

export default function SiteHeader() {
  return (
    <header className="bg-head-bg text-head-ink">
      <div className="mx-auto flex max-w-5xl flex-wrap items-center gap-x-4 gap-y-0.5 px-6 py-2.5">
        <Link href="/" className="mr-auto flex min-h-11 items-center gap-3">
          <svg width="32" height="32" viewBox="0 0 34 34" aria-hidden="true">
            <circle cx="17" cy="17" r="15" fill="none" stroke="currentColor" strokeWidth="1.4" />
            <path d="M17 2 A15 15 0 0 1 17 32 A9 15 0 0 0 17 2 Z" fill="currentColor" />
          </svg>
          <span className="font-display text-2xl">Zetalmanac</span>
        </Link>
        <NavLinks />
        <ThemeToggle />
      </div>
    </header>
  );
}
