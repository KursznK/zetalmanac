// Pemanggil API konversi. Dipakai di server (Server Component), jadi memanggil API_ORIGIN langsung.
export const API_ORIGIN = process.env.API_ORIGIN ?? "http://127.0.0.1:8000";

export const KALENDER = [
  { id: "gregorian", label: "Gregorian", contoh: "2026-11-05" },
  { id: "julian", label: "Julian", contoh: "2026-10-23" },
  { id: "hijri", label: "Hijriah (urfi)", contoh: "1448-05-24" },
  { id: "china", label: "China", contoh: "2026-09-27" },
  { id: "maya", label: "Maya (Hitungan Panjang)", contoh: "13.0.14.1.7" },
] as const;

export type Kalender = (typeof KALENDER)[number]["id"];

export type Opsi = {
  from: Kalender;
  date: string;
  scheme: string;
  epoch: string;
  correlation: string;
  leap: boolean;
  afterSunset: boolean;
  steps?: boolean;
};

type TanggalBiasa = { year: number; month: number; day: number; label: string };

export type HasilKonversi = {
  rd: number;
  jdn: number;
  hari: string;
  gregorian: TanggalBiasa;
  julian: TanggalBiasa;
  hijri: TanggalBiasa & { scheme: string; epoch: string; after_sunset: boolean };
  china:
    | (TanggalBiasa & { leap: boolean; year_ganzhi: string; year_label: string; day_ganzhi: string })
    | null;
  maya: { long_count: string; correlation: number; tzolkin: string; haab: string; lord_of_night: string };
  steps?: { gregorian?: Langkah[]; hijri: Langkah[]; maya: Langkah[] };
};

export type Langkah = { judul: string; baris: string[] };

export type HasilApi = { ok: true; data: HasilKonversi } | { ok: false; pesan: string };

function pesanGalat(body: unknown): string {
  if (typeof body === "object" && body !== null && "detail" in body) {
    const detail = (body as { detail: unknown }).detail;
    if (typeof detail === "string") return detail;
  }
  return "Input tidak valid. Periksa format tanggal dan pilihan.";
}

export async function konversi(opsi: Opsi): Promise<HasilApi> {
  const params = new URLSearchParams({
    from: opsi.from,
    date: opsi.date,
    scheme: opsi.scheme,
    epoch: opsi.epoch,
    correlation: opsi.correlation,
  });
  if (opsi.leap) params.set("leap", "true");
  if (opsi.afterSunset) params.set("after_sunset", "true");
  if (opsi.steps) params.set("steps", "true");

  let res: Response;
  try {
    res = await fetch(`${API_ORIGIN}/v1/convert?${params}`);
  } catch {
    return { ok: false, pesan: "API belum bisa dihubungi. Coba lagi sebentar lagi." };
  }
  const body: unknown = await res.json().catch(() => null);
  if (!res.ok) return { ok: false, pesan: pesanGalat(body) };
  return { ok: true, data: body as HasilKonversi };
}

export type HariBulan = {
  day: number;
  rd: number;
  weekday: number;
  hijri: { year: number; month: number; day: number; month_name: string };
  china: {
    year: number;
    month: number;
    leap: boolean;
    day: number;
    label: string;
    zhongqi: string | null;
  } | null;
};

export type TabelBulan = {
  year: number;
  month: number;
  month_name: string;
  scheme: string;
  epoch: string;
  days: HariBulan[];
};

export async function bulan(
  year: number,
  month: number,
): Promise<{ ok: true; data: TabelBulan } | { ok: false; pesan: string }> {
  const params = new URLSearchParams({ year: String(year), month: String(month) });
  let res: Response;
  try {
    res = await fetch(`${API_ORIGIN}/v1/month?${params}`);
  } catch {
    return { ok: false, pesan: "API belum bisa dihubungi. Coba lagi sebentar lagi." };
  }
  const body: unknown = await res.json().catch(() => null);
  if (!res.ok) return { ok: false, pesan: pesanGalat(body) };
  return { ok: true, data: body as TabelBulan };
}

export type HariPenting = {
  nama: string;
  kalender: string;
  rd: number;
  hari_lagi: number;
  label: string;
};

export async function hariPenting(
  date: string,
): Promise<{ ok: true; data: HariPenting[] } | { ok: false; pesan: string }> {
  let res: Response;
  try {
    res = await fetch(`${API_ORIGIN}/v1/upcoming?${new URLSearchParams({ date })}`);
  } catch {
    return { ok: false, pesan: "API belum bisa dihubungi. Coba lagi sebentar lagi." };
  }
  const body: unknown = await res.json().catch(() => null);
  if (!res.ok) return { ok: false, pesan: pesanGalat(body) };
  return { ok: true, data: body as HariPenting[] };
}

// Rata Die -> tanggal Gregorian "TTTT-BB-HH", untuk tautan ke /konversi.
// RD 719163 adalah 1 Januari 1970, titik nol waktu JavaScript.
export function rdKeIso(rd: number): string {
  return new Date((rd - 719163) * 86_400_000).toISOString().slice(0, 10);
}

export function hariIniDiJakarta(): string {
  // en-CA menghasilkan format TAHUN-BULAN-TANGGAL
  return new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Jakarta" }).format(new Date());
}
