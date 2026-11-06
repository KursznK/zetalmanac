# ADR 0001: Retrieval situs memakai dense bge-m3, bukan hybrid

- **Status:** diterima
- **Tanggal:** 6 November 2026 (Sesi 4.4)
- **Bukti:** `eval/reports/retrieval.md` (36 kueri berlabel, diperiksa manusia)

## Konteks

Korpus berisi 256 potongan dalam dua bahasa (65 id, 191 en). Sekitar separuh kueri evaluasi
(16 dari 36) bersifat lintas bahasa: jawabannya hanya ada di dokumen berbahasa lain. Baseline BM25
memakai deteksi bahasa lalu hanya mencari di indeks bahasa itu, sehingga lemah di kategori ini
(recall@5 lintas ≈ 0,31).

Kandidat yang dievaluasi:

| Sistem | Boleh dipakai situs? |
|---|---|
| BM25 (deteksi bahasa), BM25 dua bahasa | ya |
| Dense bge-m3 (Cloudflare Workers AI, kuota gratis harian) | ya |
| Dense Gemini Embedding 2 (kuota gratis Gemini API) | tidak, hanya pembanding offline |
| Hybrid BM25 + dense dengan Reciprocal Rank Fusion (RRF, k = 60) | ya, untuk bge-m3 |

Gemini tidak dipakai di situs karena syarat layanan Gemini API (berlaku 23 Maret 2026) melarang
pemakaian pada aplikasi yang kemungkinan besar diakses pengguna di bawah 18 tahun, dan di kuota
gratis konten yang dikirim dipakai Google untuk mengembangkan produknya.

## Temuan

1. **Dense bge-m3 mengungguli BM25** (recall@5 0,76 vs 0,62; lintas 0,50 vs 0,31).
2. **Hybrid tidak membantu, malah menurunkan hasil.** RRF memberi skor ganda pada potongan yang
   muncul di kedua daftar. Karena BM25 berdeteksi bahasa hanya mengembalikan satu bahasa, sekitar
   95% potongan di 5 besar hybrid berbahasa sama dengan hasil deteksi (dense saja: ±67%). Temuan
   lintas bahasa dari dense tersingkir.
3. **Perbaikan berprinsip (BM25 di kedua bahasa) tidak cukup.** BM25 tetap tidak bisa
   mencocokkan kata lintas bahasa, sehingga "kesepakatan" yang diberi bobot oleh RRF tetap
   condong ke bahasa kueri. Hybrid hasil perbaikan masih di bawah dense saja.
4. **Gemini Embedding 2 unggul ±10 poin recall@5** (lintas ±22 poin) dibanding bge-m3. Ini harga
   yang dibayar demi kepatuhan dan privasi.
5. **Ukuran sampel kecil.** Uji tanda berpasangan per kueri: tidak ada selisih terhadap bge-m3 yang
   mencapai p < 0,05. Angka di atas menunjukkan arah, bukan kepastian.

## Keputusan

- Situs memakai **pencarian dense bge-m3 saja** di seluruh potongan (tanpa deteksi bahasa).
- **BM25 menjadi cadangan** bila Cloudflare tidak bisa dihubungi atau kuota harian habis, supaya
  fitur tanya-jawab tetap jalan dengan kualitas lebih rendah, bukan mati.
- Bobot dan kedalaman RRF **sengaja tidak di-tuning** terhadap 36 kueri yang sama: hasilnya akan
  overfit ke dataset evaluasi.

## Ditinjau ulang bila

- Dataset evaluasi diperbesar (target ≥ 100 kueri) sehingga selisih kecil bisa diuji.
- Korpus bertambah banyak teks berbahasa Indonesia, atau ada kueri berisi istilah/angka persis
  (mis. nomor korelasi, nama bulan) yang lebih cocok dicari secara leksikal.
- Ada model embedding multibahasa gratis lain yang boleh dipakai situs.
