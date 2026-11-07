# Tinjauan manual jawaban LLM (Sesi 4.5)

Pemeriksaan otomatis di `jawaban.md` hanya mengecek tool, kata kunci, dan nomor sitasi. Catatan ini
berisi masalah yang **lolos** pemeriksaan otomatis tetapi terlihat saat jawaban dibaca manusia
(`eval/runs/*.jsonl`, 6 November 2026).

| id | model | masalah | jenis |
|---|---|---|---|
| a04 | qwen/qwen3.8-27b | Menyebut Tahun Baru Imlek sebagai "1 Muharam Imlek"; Muharam adalah bulan Hijriah. | istilah salah |
| a07 | openai/gpt-oss-120b | Mengaitkan beda epoch dengan aturan `after_sunset`; sumber [1] menyebut keduanya sebagai parameter terpisah. | klaim tidak didukung sumber |
| a09 | openai/gpt-oss-120b | Menjelaskan penempatan bulan kabisat secara spekulatif ("bila siklus bulan terlalu maju…") dan mengutip [1] untuk kalimat yang isinya dari sumber lain. | klaim tidak didukung, sitasi keliru |
| a09 | keduanya | Retrieval tidak mengambil aturan "bulan tanpa zhongqi" (spec-china › Aturan, Solar year and solar terms), jadi jawaban tidak memuat aturan intinya. | retrieval meleset |

## Pelajaran

- Lulus pemeriksaan otomatis tidak sama dengan benar. Perlu pemeriksaan kesetiaan pada sumber
  (*faithfulness*) per klaim, oleh manusia atau oleh LLM penilai yang berbeda dari model penjawab.
- Kalimat yang terdengar meyakinkan dan diberi sitasi tetap bisa tidak didukung sumbernya (a07).

## Run ulang 7 November 2026 (prompt dengan aturan keamanan dan kanari)

- **gpt-oss-120b: tidak turun** (15/16, gagal yang sama: a09). Aturan keamanan tidak mengganggu
  pertanyaan wajar.
- **qwen3.8-27b: 15/16 → 13/16.** a01 dan a03 gagal hanya karena tool tidak dipanggil; isinya benar
  dan sitasinya sah. Tanggal keduanya memang tercantum di korpus (*Jangkar uji* spesifikasi Hijriah dan
  artikel Long Count), jadi Qwen menjawab dari sumber. Dengan satu kali run dan temperature 0,7, tidak
  bisa dibedakan apakah ini akibat aturan baru atau keacakan.
- **Kelemahan dataset:** a01 dan a03 bukan uji tool yang tegas karena jawabannya ada di korpus.
  Ditambahkan **a17** (17 Maret 1987) yang hasilnya tidak ada di korpus.
