"""Endpoint tanya-jawab: verifikasi Turnstile, lalu alur zrag.tanya (pengaman + RAG + LLM).

Kontrol keamanan lapisan web (lihat docs/security/threat-model.md):
- Cloudflare Turnstile: setiap pertanyaan butuh token sekali-pakai dari halaman web (LLM10).
- Rate limit per IP: aturan Vercel WAF pada proyek web (path /api/v1/tanya), diatur di dashboard.
- Respons tidak di-cache dan teks pertanyaan tidak dicatat ke log (LLM02).
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

# zrag membaca indeks dari folder data milik API ini (harus diatur sebelum zrag diimpor).
os.environ.setdefault(
    "ZRAG_INDEX_DIR", str(Path(__file__).resolve().parents[1] / "data" / "index")
)

router = APIRouter()

SITEVERIFY = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
# Disimpan untuk evaluasi saja; tidak boleh sampai ke pengunjung.
FIELD_INTERNAL = ("teks_mentah",)


class Permintaan(BaseModel):
    # Batas longgar di sini hanya penjaga ukuran body; aturan 500 karakter ada di zrag.
    pertanyaan: Annotated[str, Field(max_length=2000)]
    turnstile: Annotated[str, Field(min_length=1, max_length=2048)]


def secret_turnstile() -> str | None:
    from zrag.embed import baca_env

    return os.environ.get("TURNSTILE_SECRET_KEY") or baca_env().get(
        "TURNSTILE_SECRET_KEY"
    )


def verifikasi_turnstile(token: str, secret: str, ip: str | None) -> bool:
    """Tanya Cloudflare apakah token Turnstile sah. Token hanya bisa diverifikasi sekali."""
    data = {"secret": secret, "response": token}
    if ip:
        data["remoteip"] = ip
    req = urllib.request.Request(
        SITEVERIFY,
        data=urllib.parse.urlencode(data).encode(),
        method="POST",
        headers={"User-Agent": "zetalmanac-api/0.1"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return bool(json.loads(resp.read()).get("success"))
    except (urllib.error.URLError, OSError, ValueError):
        return False


def ip_pengunjung(request: Request) -> str | None:
    diteruskan = request.headers.get("x-forwarded-for", "")
    return diteruskan.split(",")[0].strip() or None


def jalankan_tanya(pertanyaan: str) -> dict:
    # Diimpor saat dipakai, supaya endpoint konversi tidak ikut memuat zrag (cold start lebih cepat).
    from zrag.tanya import tanya

    return tanya(pertanyaan)


@router.post("/v1/tanya")
def tanya_endpoint(body: Permintaan, request: Request, response: Response) -> dict:
    """Jawab pertanyaan tentang kalender dari sumber Zetalmanac.

    Status di body: dijawab, tidak_ditemukan, ditolak_input, ditolak_injeksi,
    ditolak_keluaran, atau cadangan. Semuanya HTTP 200; galat verifikasi 403/503.
    """
    response.headers["Cache-Control"] = "no-store"
    secret = secret_turnstile()
    if not secret:
        raise HTTPException(
            status_code=503, detail="Fitur tanya-jawab belum dikonfigurasi."
        )
    if not verifikasi_turnstile(body.turnstile, secret, ip_pengunjung(request)):
        raise HTTPException(
            status_code=403,
            detail="Verifikasi anti-bot gagal atau kedaluwarsa. Muat ulang halaman lalu coba lagi.",
        )
    hasil = jalankan_tanya(body.pertanyaan)
    return {k: v for k, v in hasil.items() if k not in FIELD_INTERNAL}
