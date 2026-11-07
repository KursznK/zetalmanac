"""Alur tanya-jawab lengkap untuk situs: validasi → guard → retrieval → LLM berantai → cek keluaran.

    uv run python -m zrag.tanya "kapan tahun kabisat hisab urfi?"

Mode web gagal cepat: setiap panggilan API paling banyak dicoba 2 kali dengan jeda ≤ 3 detik,
karena pengunjung tidak mau menunggu lama (batas teknis fungsi Vercel Hobby dengan fluid compute
jauh lebih longgar: 300 detik). Kalau semua model gagal (mis. kuota harian habis), situs tetap
menampilkan potongan sumber teratas dari retrieval, tanpa jawaban LLM.
"""

import json
import sys
from dataclasses import asdict

from zrag.embed import GalatHTTP
from zrag.jawab import MODEL_UTAMA, ambil_sumber, info_dokumen, jawab
from zrag.keamanan import (
    AMBANG_INJEKSI,
    InputDitolak,
    bersihkan,
    masalah_keluaran,
    skor_injeksi,
)

# Hanya model yang sudah dievaluasi (eval/reports/jawaban.md) yang boleh masuk rantai.
RANTAI_MODEL = (MODEL_UTAMA, "qwen/qwen3.8-27b")
PERCOBAAN_WEB = 2
MAKS_JEDA_WEB = 3.0

PESAN = {
    "ditolak_input": "Pertanyaan kosong atau terlalu panjang (maksimal 500 karakter).",
    "ditolak_injeksi": (
        "Pertanyaan ini terdeteksi sebagai upaya mengubah aturan asisten, jadi tidak diproses. "
        "Silakan ajukan pertanyaan tentang kalender."
    ),
    "ditolak_keluaran": (
        "Jawaban yang dihasilkan tidak lolos pemeriksaan keamanan, jadi tidak ditampilkan. "
        "Silakan ajukan pertanyaan dengan kalimat lain."
    ),
    "cadangan": (
        "Asisten AI sedang tidak tersedia (kuota harian mungkin habis). Berikut potongan sumber "
        "yang paling relevan dengan pertanyaanmu."
    ),
}


def _sumber_tampil(sumber: list[dict], nomor: list[int] | None = None) -> list[dict]:
    """Daftar sumber untuk ditampilkan: judul, bagian, URL, atribusi lisensi."""
    dok = info_dokumen()
    hasil = []
    for i, s in enumerate(sumber, start=1):
        if nomor is not None and i not in nomor:
            continue
        d = dok[s["doc_id"]]
        hasil.append(
            {
                "nomor": i,
                "judul": d["judul"],
                "bagian": s["section"],
                "url": d["url"],
                "atribusi": d["atribusi"],
                **({"cuplikan": s["text"][:300]} if "text" in s else {}),
            }
        )
    return hasil


def tanya(pertanyaan: str, rantai: tuple[str, ...] = RANTAI_MODEL) -> dict:
    """Satu permintaan dari pengunjung. Selalu mengembalikan dict (tidak melempar galat)."""
    try:
        teks = bersihkan(pertanyaan)
    except InputDitolak as e:
        return {
            "status": "ditolak_input",
            "pesan": PESAN["ditolak_input"],
            "alasan": str(e),
        }

    skor = skor_injeksi(teks)
    if skor is not None and skor >= AMBANG_INJEKSI:
        return {
            "status": "ditolak_injeksi",
            "pesan": PESAN["ditolak_injeksi"],
            "skor_injeksi": skor,
        }

    sumber, retrieval = ambil_sumber(teks)
    galat = []
    for model in rantai:
        try:
            j = jawab(
                teks,
                model=model,
                sumber=sumber,
                retrieval=retrieval,
                percobaan=PERCOBAAN_WEB,
                maks_jeda=MAKS_JEDA_WEB,
            )
        except GalatHTTP as e:
            galat.append(f"{model}: HTTP {e.kode}")
            continue
        masalah = masalah_keluaran(j.teks)
        if masalah:
            return {
                "status": "ditolak_keluaran",
                "pesan": PESAN["ditolak_keluaran"],
                "masalah": masalah,
                "skor_injeksi": skor,
                "model": model,
                "teks_mentah": j.teks,  # hanya untuk evaluasi; API tidak boleh meneruskannya
                "token": j.token,
            }
        return {
            "status": "dijawab" if j.ditemukan else "tidak_ditemukan",
            "jawaban": j.teks,
            "sumber": _sumber_tampil(sumber, j.sitasi),
            "tool": j.tool,
            "model": model,
            "retrieval": retrieval,
            "skor_injeksi": skor,
            "token": j.token,
            "detik": j.detik,
            "galat_sebelumnya": galat,
        }
    return {
        "status": "cadangan",
        "pesan": PESAN["cadangan"],
        "sumber": _sumber_tampil(sumber[:3]),
        "retrieval": retrieval,
        "skor_injeksi": skor,
        "galat_sebelumnya": galat,
    }


def main() -> None:
    pertanyaan = " ".join(sys.argv[1:])
    if not pertanyaan:
        sys.exit(
            'Contoh: uv run python -m zrag.tanya "kapan tahun kabisat hisab urfi?"'
        )
    print(json.dumps(tanya(pertanyaan), ensure_ascii=False, indent=1, default=asdict))


if __name__ == "__main__":
    main()
