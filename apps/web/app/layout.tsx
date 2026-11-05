import type { Metadata } from "next";
import localFont from "next/font/local";
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

export default function RootLayout({ children }: LayoutProps<"/">) {
  const fonts = [lmRoman17, lmRoman, lmCaps, lmSans, lmMono].map((f) => f.variable).join(" ");
  return (
    <html lang="id" className={`${fonts} h-full antialiased`}>
      <body className="flex min-h-full flex-col bg-bg font-sans text-[17px] leading-relaxed text-ink">
        <SiteHeader />
        <div className="flex-1">{children}</div>
        <footer className="mx-auto w-full max-w-5xl border-t border-rule px-6 py-8 text-sm text-muted">
          Zetalmanac · proyek nonkomersial · kode sumber berlisensi MIT
        </footer>
      </body>
    </html>
  );
}
