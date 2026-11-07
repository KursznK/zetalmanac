# Tinjauan faithfulness per klaim (Sesi 4.8)

Bahan: 58 klaim dari hasil evaluasi jawaban 7 November 2026 (`eval/datasets/faithfulness/klaim.yaml`),
dilabel oleh satu orang (Zaky), lalu dinilai LLM penilai dari keluarga model berbeda (Qwen menilai
gpt-oss, gpt-oss menilai Qwen). Angka lengkap: `faithfulness.md`.

## Hasil utama

| Ukuran | Nilai |
|---|---|
| Setuju, 4 label | 0,81 |
| Cohen's kappa, 4 label | 0,53 (sedang) |
| Cohen's kappa, aman vs bermasalah | 0,50 |
| Klaim bermasalah (manusia) yang tertangkap penilai | 9/13 |
| Setuju soal `sitasi_tepat` | 0,82 (n = 39) |

Persentase setuju terlihat tinggi karena sebagian besar klaim memang didukung; kappa mengoreksi
kesepakatan yang bisa terjadi karena kebetulan.

## Adjudikasi 11 perbedaan

| Kelompok | Klaim | Keputusan |
|---|---|---|
| **Penilai mencampur label dengan sitasi** (sistematis) | gpt-oss a03/1, a05/1, a06/1, a17/1 | Isi klaim didukung hasil tool, sitasinya keliru. Penilai menurunkan *label*, padahal kesalahan sitasi seharusnya hanya di `sitasi_tepat`. Label manusia benar. |
| **Penilai terlalu longgar** | qwen a04/1 ("1 Muharam" untuk Imlek), gpt-oss a09/1 (mekanisme penempatan bulan kabisat dikarang), qwen a07/4 (syarat "skema II" hilang), qwen a08/4 ("largely corrected" menjadi "prevents") | Label manusia benar; penilai meloloskan pelebih-lebihan dan istilah keliru. |
| **Penilai terlalu ketat atau kasus perbatasan** | gpt-oss a12/2 (parafrase setia), qwen a07/2 (turunan logis; penalaran penilai keliru soal arah epoch), qwen a03/2 ("often associated" tidak tersurat) | Label manusia dipertahankan; a07/2 dan a03/2 bisa diperdebatkan antara *didukung* dan *sebagian*. |

Tidak ada label manusia yang diubah setelah adjudikasi.

## Faithfulness model penjawab (label manusia)

| Model | klaim | bermasalah (sebagian + tidak didukung) | sitasi keliru |
|---|---|---|---|
| gpt-oss-120b | 23 | 7 (30%) | 6 |
| qwen3.8-27b | 35 | 6 (17%) | 2 |

Arah ini berlawanan dengan pilihan model utama (gpt-oss: lebih cepat, lulus lebih banyak
pemeriksaan otomatis). Uji Fisher: p = 0,34, jadi belum bisa disebut selisih nyata. Kesalahan sitasi
gpt-oss hampir semuanya kalimat yang isinya dari hasil tool tetapi diberi nomor sumber, meskipun
prompt menyatakan hasil tool tidak perlu sitasi.

## Kesimpulan

1. **Penilai dipakai sebagai alat saring, bukan hakim akhir.** Ia menandai klaim yang perlu dibaca
   manusia dan cukup untuk memantau tren, tetapi meloloskan 4 dari 13 klaim bermasalah.
2. **Kelemahan sistematisnya spesifik dan bisa diperbaiki**: pisahkan penilaian dukungan isi dari
   ketepatan sitasi. Penilai versi baru wajib diukur pada klaim **baru**, bukan 58 klaim ini, supaya
   tidak overfit ke label yang sudah dilihat.
3. **Keterbatasan:** label dari satu orang (belum ada kesepakatan antar-manusia), 58 klaim dari satu
   kali run, dan pembagian kalimat otomatis kadang menggabungkan beberapa klaim dalam satu kalimat.

## Langkah berikutnya

- Tambah pertanyaan uji dua bagian (pola kegagalan yang ditemukan di produksi), jalankan ulang
  evaluasi jawaban, dan label klaim-klaim barunya.
- Uji penilai v2 di klaim baru tersebut.
- Pertimbangkan perbaikan sitasi pada kalimat dari hasil tool, lalu ukur ulang kedua model.
