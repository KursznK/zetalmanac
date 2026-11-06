"""Buat (atau perbarui) vektor embedding untuk potongan korpus dan kueri evaluasi.

    uv run python -m zrag.embed_index bge-m3
    uv run python -m zrag.embed_index gemini-embedding-2

Inkremental: teks yang sha256-nya sudah ada di berkas lama tidak dikirim ulang, jadi kuota gratis
hanya terpakai untuk potongan atau kueri yang baru/berubah. Butuh internet dan kunci di `.env`.
"""

import sys
import time
from collections.abc import Sequence
from pathlib import Path

from zrag.dense import lokasi_chunks, lokasi_kueri
from zrag.embed import EMBEDDERS, Embedder
from zrag.evaluate import load_dataset
from zrag.manifest import REPO_ROOT
from zrag.search import load_chunks
from zrag.vectors import VectorSet, ada, muat, sha256, simpan


def perbarui(
    prefix: Path, embedder: Embedder, items: Sequence[tuple[str, str]]
) -> tuple[int, int]:
    """Pastikan setiap (id, teks) punya vektor di `prefix`. Kembalikan (baru, dipakai ulang)."""
    lama = muat(prefix).by_sha() if ada(prefix) else {}
    perlu = [teks for _, teks in items if sha256(teks) not in lama]
    perlu = list(dict.fromkeys(perlu))  # buang duplikat, urutan tetap
    baru: dict[str, list[float]] = {}
    ukuran = embedder.ukuran_batch
    for awal in range(0, len(perlu), ukuran):
        batch = perlu[awal : awal + ukuran]
        print(f"  {embedder.nama}: {awal + len(batch)}/{len(perlu)}")
        vektor = embedder.embed(batch)
        if len(vektor) != len(batch):
            raise RuntimeError(f"diminta {len(batch)} vektor, diterima {len(vektor)}")
        baru |= {sha256(t): v for t, v in zip(batch, vektor, strict=True)}
        if awal + ukuran < len(perlu) and embedder.jeda_antar_batch:
            time.sleep(embedder.jeda_antar_batch)
    semua = lama | baru
    shas = [sha256(teks) for _, teks in items]
    rows = [semua[s] for s in shas]
    simpan(
        prefix,
        VectorSet(
            model=embedder.nama,
            dim=len(rows[0]),
            ids=[i for i, _ in items],
            shas=shas,
            rows=rows,
        ),
    )
    return len(baru), len(items) - len(perlu)


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in EMBEDDERS:
        sys.exit(f"Contoh: uv run python -m zrag.embed_index {' | '.join(EMBEDDERS)}")
    embedder: Embedder = EMBEDDERS[sys.argv[1]]()
    chunks = [(c["id"], embedder.teks_dokumen(c)) for c in load_chunks()]
    kueri = [(q["id"], embedder.teks_kueri(q["query"])) for q in load_dataset()]
    for judul, prefix, items in (
        ("potongan korpus", lokasi_chunks(embedder.nama), chunks),
        ("kueri evaluasi", lokasi_kueri(embedder.nama), kueri),
    ):
        print(f"{judul} → {prefix.relative_to(REPO_ROOT)}")
        baru, ulang = perbarui(prefix, embedder, items)
        print(f"  selesai: {baru} di-embed, {ulang} dipakai ulang\n")


if __name__ == "__main__":
    main()
