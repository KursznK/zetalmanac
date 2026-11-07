// Pemanggil endpoint tanya-jawab. Dipakai di browser: "/api/..." diteruskan ke API oleh
// rewrite di next.config.ts, jadi tidak perlu CORS dan aturan WAF bisa dipasang di proyek web.

export type Sumber = {
  nomor: number;
  judul: string;
  bagian: string;
  url: string;
  atribusi: string;
  cuplikan?: string;
};

export type HasilTanya =
  | {
      status: "dijawab" | "tidak_ditemukan";
      jawaban: string;
      sumber: Sumber[];
      tool: { nama: string; argumen: Record<string, unknown> }[];
      model: string;
      retrieval: string;
      detik: number;
    }
  | { status: "cadangan"; pesan: string; sumber: Sumber[] }
  | { status: "ditolak_input" | "ditolak_injeksi" | "ditolak_keluaran"; pesan: string };

export type RespTanya = { ok: true; data: HasilTanya } | { ok: false; pesan: string };

export const MAKS_KARAKTER = 500;

export async function kirimPertanyaan(pertanyaan: string, turnstile: string): Promise<RespTanya> {
  try {
    const resp = await fetch("/api/v1/tanya", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pertanyaan, turnstile }),
    });
    const body: unknown = await resp.json().catch(() => null);
    if (!resp.ok) {
      const detail =
        typeof body === "object" && body !== null && "detail" in body && typeof body.detail === "string"
          ? body.detail
          : null;
      if (resp.status === 429) return { ok: false, pesan: "Terlalu banyak pertanyaan. Tunggu sebentar lalu coba lagi." };
      return { ok: false, pesan: detail ?? "Terjadi galat. Coba lagi beberapa saat lagi." };
    }
    return { ok: true, data: body as HasilTanya };
  } catch {
    return { ok: false, pesan: "Tidak bisa menghubungi server. Periksa koneksi internet." };
  }
}
