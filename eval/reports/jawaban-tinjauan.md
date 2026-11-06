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
