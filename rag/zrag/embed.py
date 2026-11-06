"""Klien embedding: Cloudflare Workers AI (bge-m3) dan Gemini Embedding 2.

Kunci dibaca dari variabel lingkungan, atau dari berkas `.env` di root repo (diabaikan git):
    CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN, GEMINI_API_KEY

Hanya memakai pustaka standar (urllib), tanpa SDK, supaya dependensi tetap kecil.
"""

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Protocol

from zrag.manifest import REPO_ROOT

ENV_FILE = REPO_ROOT / ".env"
COBA_ULANG = (429, 500, 502, 503, 504)
# Beberapa API (mis. Groq, di belakang Cloudflare) menolak User-Agent bawaan urllib (galat 1010).
USER_AGENT = "zetalmanac-rag/0.1 (+https://github.com/KursznK/zetalmanac)"


class Embedder(Protocol):
    nama: str
    ukuran_batch: int
    jeda_antar_batch: float

    @staticmethod
    def teks_dokumen(chunk: dict) -> str:
        """Teks yang dikirim ke model untuk satu potongan korpus."""
        ...

    @staticmethod
    def teks_kueri(query: str) -> str:
        """Teks yang dikirim ke model untuk satu kueri pengguna."""
        ...

    def embed(self, teks: list[str]) -> list[list[float]]: ...


def baca_env(path: Path = ENV_FILE) -> dict[str, str]:
    """Parser .env sederhana: baris KUNCI=nilai; baris kosong dan '#' diabaikan."""
    hasil: dict[str, str] = {}
    if not path.exists():
        return hasil
    for baris in path.read_text(encoding="utf-8").splitlines():
        baris = baris.strip()
        if not baris or baris.startswith("#") or "=" not in baris:
            continue
        kunci, nilai = baris.split("=", 1)
        hasil[kunci.strip()] = nilai.strip().strip("\"'")
    return hasil


def rahasia(nama: str) -> str:
    nilai = os.environ.get(nama) or baca_env().get(nama)
    if not nilai:
        raise SystemExit(f"{nama} belum diisi. Tambahkan ke berkas .env di root repo.")
    return nilai


class GalatHTTP(RuntimeError):
    """Permintaan HTTP gagal setelah semua percobaan; `kode` = status HTTP terakhir."""

    def __init__(self, kode: int, pesan: str) -> None:
        super().__init__(pesan)
        self.kode = kode


def jeda_coba_ulang(retry_after: str | None, ke: int) -> float:
    """Ikuti header Retry-After (detik) kalau ada; kalau tidak, 2, 4, 8, ... detik. Maks 60."""
    try:
        jeda = float(retry_after) if retry_after else 2.0 ** (ke + 1)
    except ValueError:
        jeda = 2.0 ** (ke + 1)
    return min(max(jeda, 1.0), 60.0)


def post_json(
    url: str, headers: dict[str, str], body: dict, percobaan: int = 6
) -> dict:
    """POST JSON dengan coba ulang (jeda 2, 4, 8, ... detik) untuk 429 dan galat server."""
    data = json.dumps(body).encode("utf-8")
    for ke in range(percobaan):
        req = urllib.request.Request(
            url,
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
                **headers,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code not in COBA_ULANG or ke == percobaan - 1:
                pesan = e.read().decode("utf-8", "replace")[:500]
                raise GalatHTTP(
                    e.code, f"HTTP {e.code} dari {url.split('?')[0]}: {pesan}"
                ) from e
            jeda = jeda_coba_ulang(e.headers.get("retry-after"), ke)
            print(f"  HTTP {e.code}, coba lagi dalam {jeda:.0f} detik…")
            time.sleep(jeda)
    raise AssertionError("tidak terjangkau")


class CloudflareBgeM3:
    """BAAI bge-m3 di Cloudflare Workers AI. Multibahasa, 1024 dimensi."""

    nama = "bge-m3"
    ukuran_batch = 50
    jeda_antar_batch = 0.0

    def __init__(self) -> None:
        akun = rahasia("CLOUDFLARE_ACCOUNT_ID")
        self.url = f"https://api.cloudflare.com/client/v4/accounts/{akun}/ai/run/@cf/baai/bge-m3"
        self.headers = {"Authorization": f"Bearer {rahasia('CLOUDFLARE_API_TOKEN')}"}

    @staticmethod
    def teks_dokumen(chunk: dict) -> str:
        return f"{chunk['section']}\n{chunk['text']}"

    @staticmethod
    def teks_kueri(query: str) -> str:
        return query

    def embed(self, teks: list[str]) -> list[list[float]]:
        return baca_respons_cloudflare(
            post_json(self.url, self.headers, {"text": teks})
        )


def baca_respons_cloudflare(resp: dict) -> list[list[float]]:
    if not resp.get("success", False):
        raise RuntimeError(f"Cloudflare menolak permintaan: {resp.get('errors')}")
    return resp["result"]["data"]


class GeminiEmbedding2:
    """Gemini Embedding 2 (pembanding, hanya untuk evaluasi offline). 3072 dimensi.

    Model ini tidak menerima task_type; tugas ditulis di dalam teks (lihat dokumentasi Gemini).
    Jeda antar-batch menjaga pemakaian di bawah kuota gratis (100 request/menit, 30 ribu token/menit).
    """

    nama = "gemini-embedding-2"
    model = "models/gemini-embedding-2"
    ukuran_batch = 10
    jeda_antar_batch = 15.0

    def __init__(self) -> None:
        self.url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"{self.model}:batchEmbedContents"
        )
        self.headers = {"x-goog-api-key": rahasia("GEMINI_API_KEY")}

    @staticmethod
    def teks_dokumen(chunk: dict) -> str:
        return f"title: {chunk['section']} | text: {chunk['text']}"

    @staticmethod
    def teks_kueri(query: str) -> str:
        return f"task: search result | query: {query}"

    def body(self, teks: list[str]) -> dict:
        return {
            "requests": [
                {"model": self.model, "content": {"parts": [{"text": t}]}} for t in teks
            ]
        }

    def embed(self, teks: list[str]) -> list[list[float]]:
        resp = post_json(self.url, self.headers, self.body(teks))
        return [e["values"] for e in resp["embeddings"]]


EMBEDDERS: dict[str, type[CloudflareBgeM3] | type[GeminiEmbedding2]] = {
    CloudflareBgeM3.nama: CloudflareBgeM3,
    GeminiEmbedding2.nama: GeminiEmbedding2,
}
