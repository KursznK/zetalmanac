"""Pemeriksaan keamanan di sekitar LLM (lihat docs/security/threat-model.md).

- validasi input (LLM10: panjang dibatasi, karakter kontrol dibuang)
- skor prompt injection dari Llama Prompt Guard 2 (LLM01), lapisan tambahan di depan LLM
- pemeriksaan keluaran: kebocoran prompt sistem (LLM07) dan HTML/skrip/tautan (LLM05)
"""

import re
import unicodedata

from zrag.embed import GalatHTTP, post_json, rahasia
from zrag.jawab import GROQ_URL, KANARI

MAKS_KARAKTER = 500
MODEL_GUARD = "meta-llama/llama-prompt-guard-2-86m"
# Ditetapkan sebelum melihat hasil evaluasi (nilai tengah skor peluang), supaya ambang tidak
# di-tuning terhadap dataset uji. Tabel ambang di eval/reports/keamanan.md menunjukkan dampaknya.
AMBANG_INJEKSI = 0.5

# Potongan khas prompt sistem: kalau muncul di jawaban, prompt sistem kemungkinan bocor.
JEJAK_PROMPT = (
    KANARI,
    "WAJIB panggil tool",
    "Teks di dalam <sumber>",
    "Instruksi ini rahasia",
)
_HTML = re.compile(r"<\s*/?\s*[a-zA-Z][^>]*>")
_URL = re.compile(r"https?://|www\.", re.IGNORECASE)


class InputDitolak(ValueError):
    """Pertanyaan tidak memenuhi syarat dasar; tidak diteruskan ke API mana pun."""


def bersihkan(pertanyaan: str) -> str:
    """Buang karakter kontrol/format tak terlihat, rapikan spasi, tolak yang kosong/terlalu panjang."""
    if not isinstance(pertanyaan, str):
        raise InputDitolak("pertanyaan harus berupa teks")
    teks = "".join(
        " " if ch in "\n\r\t" else ch
        for ch in pertanyaan
        if ch in "\n\r\t" or unicodedata.category(ch) not in ("Cc", "Cf")
    )
    teks = re.sub(r"\s+", " ", teks).strip()
    if not teks:
        raise InputDitolak("pertanyaan kosong")
    if len(teks) > MAKS_KARAKTER:
        raise InputDitolak(f"pertanyaan lebih dari {MAKS_KARAKTER} karakter")
    return teks


def baca_skor_guard(resp: dict) -> float:
    """Prompt Guard di Groq mengembalikan peluang serangan sebagai teks, mis. '0.9994'."""
    skor = float(resp["choices"][0]["message"]["content"].strip())
    if not 0.0 <= skor <= 1.0:
        raise ValueError(f"skor di luar 0-1: {skor}")
    return skor


def skor_injeksi(teks: str, percobaan: int = 2, maks_jeda: float = 3.0) -> float | None:
    """Peluang `teks` adalah prompt injection/jailbreak. None kalau layanan guard gagal.

    Gagal-terbuka (None → tetap lanjut) disengaja: guard hanya satu lapisan; aturan prompt,
    kanari, dan pemeriksaan keluaran tetap berjalan. Keputusan ini dicatat di threat model.
    """
    body = {"model": MODEL_GUARD, "messages": [{"role": "user", "content": teks}]}
    try:
        resp = post_json(
            GROQ_URL,
            {"Authorization": f"Bearer {rahasia('GROQ_API_KEY')}"},
            body,
            percobaan,
            maks_jeda,
        )
        return baca_skor_guard(resp)
    except (GalatHTTP, OSError, KeyError, ValueError, IndexError):
        return None


def masalah_keluaran(teks: str) -> list[str]:
    """Alasan jawaban tidak boleh ditampilkan apa adanya (kosong = aman)."""
    masalah = []
    if any(j.lower() in teks.lower() for j in JEJAK_PROMPT):
        masalah.append("bocor_prompt")
    if _HTML.search(teks):
        masalah.append("html")
    if _URL.search(teks):
        masalah.append("tautan")
    return masalah
