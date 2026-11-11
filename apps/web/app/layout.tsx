import type { Metadata } from "next";
import localFont from "next/font/local";
import Link from "next/link";
import SiteHeader from "./site-header";
import "./globals.css";

const lmRoman17 = localFont({
  src: "./fonts/lmroman17-regular.otf",
  variable: "--font-lm-roman17",
  display: "swap",
});
const lmRoman = localFont({
  src: [
    { path: "./fonts/lmroman10-regular.otf", weight: "400", style: "normal" },
    { path: "./fonts/lmroman10-italic.otf", weight: "400", style: "italic" },
  ],
  variable: "--font-lm-roman",
  display: "swap",
});
const lmCaps = localFont({
  src: "./fonts/lmromancaps10-regular.otf",
  variable: "--font-lm-caps",
  display: "swap",
});
const lmSans = localFont({
  src: [
    { path: "./fonts/lmsans10-regular.otf", weight: "400", style: "normal" },
    { path: "./fonts/lmsans10-oblique.otf", weight: "400", style: "italic" },
    { path: "./fonts/lmsans10-bold.otf", weight: "700", style: "normal" },
  ],
  variable: "--font-lm-sans",
  display: "swap",
});
const lmMono = localFont({
  src: "./fonts/lmmono10-regular.otf",
  variable: "--font-lm-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Zetalmanac",
  description: "Konverter tanggal Gregorian, Julian, Hijriah urfi, China, dan Maya",
};

// Dijalankan sebelum halaman tampil, supaya tema pilihan pengguna langsung berlaku
// (tanpa kedipan tema terang). Teksnya tetap, tidak memuat input dari pengguna.
const SKRIP_TEMA = `(function(){try{var t=localStorage.getItem("tema");if(t==="light"||t==="dark")document.documentElement.dataset.theme=t;}catch(e){}})();`;

export default function RootLayout({ children }: LayoutProps<"/">) {
  const fonts = [lmRoman17, lmRoman, lmCaps, lmSans, lmMono].map((f) => f.variable).join(" ");
  return (
    <html lang="id" className={`${fonts} h-full antialiased`} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: SKRIP_TEMA }} />
      </head>
      <body className="flex min-h-full flex-col bg-bg font-sans text-[17px] leading-relaxed text-ink">
        <SiteHeader />
        <div className="flex-1">{children}</div>
        <footer className="mx-auto w-full max-w-5xl px-6">
          <div className="flex flex-wrap justify-between gap-x-6 gap-y-2 border-t border-rule pt-7 pb-8 text-sm text-muted">
            <p>Zetalmanac · Proyek Non-komersial · Kode sumber berlisensi MIT</p>
            <p className="flex flex-wrap gap-5">
              <a className="tautan" href="https://github.com/KursznK/zetalmanac">
                GitHub
              </a>
              <Link className="tautan" href="/validasi">
                Status validasi
              </Link>
              <Link className="tautan" href="/tanya">
                Tanya
              </Link>
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
