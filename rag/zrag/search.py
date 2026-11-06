"""Pencarian BM25 per bahasa di atas chunks.jsonl.

uv run python -m zrag.search "kapan tahun kabisat hisab urfi"
"""

import json
import sys
from functools import lru_cache
from pathlib import Path

from zrag.bm25 import BM25
from zrag.ingest import OUT
from zrag.text import detect_lang, words


def load_chunks(path: Path = OUT) -> list[dict]:
    return [
        json.loads(baris)
        for baris in path.read_text(encoding="utf-8").splitlines()
        if baris
    ]


@lru_cache(maxsize=1)
def indexes() -> dict[str, BM25]:
    chunks = load_chunks()
    return {
        lang: BM25([c for c in chunks if c["lang"] == lang], lang)
        for lang in ("id", "en")
    }


@lru_cache(maxsize=1)
def kosakata() -> dict[str, set[str]]:
    """Semua kata mentah per bahasa, untuk menebak bahasa kueri berupa kata kunci."""
    return {
        lang: {k for c in idx.chunks for k in words(f"{c['section']} {c['text']}")}
        for lang, idx in indexes().items()
    }


def search(query: str, k: int = 5, lang: str | None = None) -> list[tuple[dict, float]]:
    """Cari di indeks berbahasa sama dengan kueri (dideteksi otomatis kalau `lang` kosong)."""
    return indexes()[lang or detect_lang(query, kosakata())].search(query, k)


def search_per_bahasa(query: str, k: int) -> dict[str, list[dict]]:
    """Hasil BM25 dari setiap indeks bahasa, tanpa deteksi bahasa (skornya tidak sebanding)."""
    return {
        lang: [c for c, _ in idx.search(query, k)] for lang, idx in indexes().items()
    }


def main() -> None:
    query = " ".join(sys.argv[1:])
    if not query:
        sys.exit('Contoh: uv run python -m zrag.search "julian day epoch"')
    print(f"Bahasa kueri: {detect_lang(query, kosakata())}\n")
    for i, (c, skor) in enumerate(search(query), start=1):
        print(f"{i}. [{skor:.2f}] {c['id']} · {c['section']}")
        print(f"   {c['text'][:160]}…\n")


if __name__ == "__main__":
    main()
