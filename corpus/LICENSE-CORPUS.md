# Lisensi korpus Zetalmanac

Korpus (folder `corpus/` dan dokumen yang dirujuk `corpus/sources.yaml`) dilisensikan
**terpisah** dari kode program (MIT). Setiap dokumen memakai lisensinya sendiri seperti
tercatat di manifest, beserta atribusinya.

| Jenis | Lisensi | Keterangan |
|---|---|---|
| Spesifikasi dan catatan karya sendiri (`docs/specs/`, catatan penulis) | CC BY 4.0 | © 2026 Muhamad Zaky Kurniawan |
| Artikel Wikipedia | CC BY-SA 4.0 | Atribusi ke kontributor Wikipedia, dengan nomor revisi |

Turunan korpus (potongan teks, indeks pencarian) yang memuat bagian dari dokumen
CC BY-SA 4.0 ikut berlisensi **CC BY-SA 4.0** (*ShareAlike*).

Hanya lisensi berikut yang boleh masuk korpus: `CC-BY-4.0`, `CC-BY-SA-4.0`, `CC0-1.0`,
`public-domain`. Aturan ini diperiksa otomatis oleh ``uv run python -m zrag.check_corpus` (folder `rag/`)` di CI.
Buku dan karya berhak cipta lain tidak dimasukkan ke korpus; cukup disebut sebagai bacaan lanjut.
