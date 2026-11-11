"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/", label: "Beranda" },
  { href: "/konversi", label: "Konversi" },
  { href: "/kalender", label: "Kalender" },
  { href: "/validasi", label: "Validasi" },
  { href: "/tanya", label: "Tanya" },
] as const;

// Komponen klien karena perlu tahu alamat halaman yang sedang dibuka (usePathname),
// supaya tautan halaman aktif bisa diberi garis bawah dan aria-current.
export default function NavLinks() {
  const pathname = usePathname();
  return (
    // Di ponsel: baris sendiri di bawah logo, bisa digeser ke samping. Mulai lebar md: sebaris dengan logo.
    <nav
      aria-label="Navigasi utama"
      className="order-3 -mx-2.5 flex basis-full gap-0.5 overflow-x-auto [scrollbar-width:none] md:order-none md:mx-0 md:basis-auto md:gap-1 md:overflow-visible"
    >
      {NAV.map((item) => {
        const aktif = item.href === "/" ? pathname === "/" : pathname.startsWith(item.href);
        return (
          <Link
            key={item.href}
            href={item.href}
            aria-current={aktif ? "page" : undefined}
            className={`inline-flex min-h-11 items-center border-b-2 px-2.5 whitespace-nowrap transition-colors hover:bg-white/10 md:px-3 ${
              aktif ? "border-head-accent" : "border-transparent"
            }`}
          >
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
