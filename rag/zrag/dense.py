"""Pencarian vektor (dense) dan penggabungan peringkat dengan Reciprocal Rank Fusion (RRF).

Pencarian dense tidak memakai deteksi bahasa: semua potongan (id dan en) dibandingkan sekaligus,
karena model multibahasa menaruh teks bermakna sama di dekat satu sama lain apa pun bahasanya.
"""

from functools import lru_cache
from pathlib import Path

from zrag.embed import EMBEDDERS
from zrag.ingest import OUT
from zrag.manifest import REPO_ROOT
from zrag.search import load_chunks
from zrag.vectors import ada, dot, muat, sha256

INDEX_DIR = OUT.parent
EVAL_VECTORS = REPO_ROOT / "eval" / "vectors"
PRODUKSI = "bge-m3"  # model yang dipakai situs; vektornya ikut ke apps/api
RRF_K = 60  # konstanta baku dari makalah RRF (Cormack dkk., 2009)


def lokasi_chunks(nama: str) -> Path:
    if nama == PRODUKSI:
        return INDEX_DIR / f"vectors-{nama}"
    return EVAL_VECTORS / f"chunks-{nama}"


def lokasi_kueri(nama: str) -> Path:
    return EVAL_VECTORS / f"queries-{nama}"


def tersedia(nama: str) -> bool:
    return ada(lokasi_chunks(nama)) and ada(lokasi_kueri(nama))


def usang(nama: str, chunks: list[dict]) -> list[str]:
    """Id potongan yang vektornya hilang atau dibuat dari teks yang sudah berubah."""
    vs = muat(lokasi_chunks(nama))
    tersimpan = dict(zip(vs.ids, vs.shas, strict=True))
    teks_dokumen = EMBEDDERS[nama].teks_dokumen
    return [
        c["id"] for c in chunks if tersimpan.get(c["id"]) != sha256(teks_dokumen(c))
    ]


@lru_cache(maxsize=4)
def indeks(nama: str) -> tuple[list[dict], list[list[float]]]:
    """Potongan beserta vektornya, urut sama dengan chunks.jsonl."""
    chunks = load_chunks()
    if salah := usang(nama, chunks):
        raise RuntimeError(
            f"Vektor {nama} usang untuk {len(salah)} potongan (mis. {salah[0]}). "
            f"Jalankan: uv run python -m zrag.embed_index {nama}"
        )
    per_id = muat(lokasi_chunks(nama)).by_id()
    return chunks, [per_id[c["id"]] for c in chunks]


def cari(nama: str, vektor_kueri: list[float], k: int) -> list[tuple[dict, float]]:
    """k potongan dengan cosine similarity tertinggi (vektor sudah dinormalisasi)."""
    chunks, rows = indeks(nama)
    skor = sorted(
        ((dot(vektor_kueri, r), i) for i, r in enumerate(rows)), reverse=True
    )[:k]
    return [(chunks[i], s) for s, i in skor]


@lru_cache(maxsize=4)
def vektor_kueri_eval(nama: str) -> dict[str, list[float]]:
    """Vektor kueri evaluasi yang sudah di-embed, diindeks dengan sha256 teks kuerinya."""
    return muat(lokasi_kueri(nama)).by_sha()


def kueri_eval(nama: str, query: str) -> list[float]:
    teks = EMBEDDERS[nama].teks_kueri(query)
    try:
        return vektor_kueri_eval(nama)[sha256(teks)]
    except KeyError:
        raise RuntimeError(
            f"Kueri {query!r} belum di-embed dengan {nama}. "
            f"Jalankan: uv run python -m zrag.embed_index {nama}"
        ) from None


def rrf(peringkat: list[list[dict]], k: int = RRF_K) -> list[dict]:
    """Gabungkan beberapa daftar peringkat: skor = Σ 1/(k + posisi), posisi mulai dari 1."""
    skor: dict[str, float] = {}
    potongan: dict[str, dict] = {}
    for daftar in peringkat:
        for posisi, c in enumerate(daftar, start=1):
            skor[c["id"]] = skor.get(c["id"], 0.0) + 1 / (k + posisi)
            potongan[c["id"]] = c
    urut = sorted(skor, key=lambda i: (-skor[i], i))
    return [potongan[i] for i in urut]
