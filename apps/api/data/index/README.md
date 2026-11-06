# Indeks korpus

`chunks.jsonl` dibuat oleh `rag/` (`uv run python -m zrag.ingest`) dari dokumen yang tercatat di
`corpus/sources.yaml`. Jangan disunting manual: tes di `rag/tests/test_index.py` memastikan berkas
ini sama persis dengan hasil membangun ulang dari korpus.

Setiap baris adalah satu potongan teks beserta lisensi dan atribusi dokumen asalnya. Karena sebagian
potongan berasal dari Wikipedia (CC BY-SA 4.0), berkas ini berlisensi **CC BY-SA 4.0**. Lihat
`corpus/LICENSE-CORPUS.md`.
