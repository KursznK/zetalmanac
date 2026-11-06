# Indeks korpus

`chunks.jsonl` dibuat oleh `rag/` (`uv run python -m zrag.ingest`) dari dokumen yang tercatat di
`corpus/sources.yaml`. Jangan disunting manual: tes di `rag/tests/test_index.py` memastikan berkas
ini sama persis dengan hasil membangun ulang dari korpus.

Setiap baris adalah satu potongan teks beserta lisensi dan atribusi dokumen asalnya. Karena sebagian
potongan berasal dari Wikipedia (CC BY-SA 4.0), berkas ini berlisensi **CC BY-SA 4.0**. Lihat
`corpus/LICENSE-CORPUS.md`.

## Vektor embedding

`vectors-bge-m3.f16` + `vectors-bge-m3.json` berisi vektor bge-m3 (Cloudflare Workers AI) untuk
setiap potongan, dibuat dengan `uv run python -m zrag.embed_index bge-m3` dari folder `rag/`.
Format: float16 little-endian, sudah dinormalisasi; metadata menyimpan sha256 teks yang di-embed.
Tes `rag/tests/test_dense.py` gagal kalau `chunks.jsonl` berubah tetapi vektornya belum dibuat ulang.
