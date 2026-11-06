# Evaluasi jawaban (RAG + tool)

Dataset: 16 pertanyaan (konversi, fakta, tolak). Retrieval: bge-m3 (ADR 0001).

## Ringkasan (pertanyaan lulus / jumlah)

| model | konversi | fakta | tolak | total | token rata-rata | detik rata-rata |
|---|---|---|---|---|---|---|
| openai/gpt-oss-120b | 6/6 | 5/6 | 4/4 | 15/16 | 3055 | 3.1 |
| qwen/qwen3.8-27b | 6/6 | 5/6 | 4/4 | 15/16 | 3383 | 7.7 |

## openai/gpt-oss-120b

| id | jenis | lulus | pemeriksaan gagal | token | retrieval |
|---|---|---|---|---|---|
| a01 | konversi | ya | - | 3727 | bge-m3 |
| a02 | konversi | ya | - | 4693 | bge-m3 |
| a03 | konversi | ya | - | 5568 | bge-m3 |
| a04 | konversi | ya | - | 4033 | bge-m3 |
| a05 | konversi | ya | - | 4223 | bge-m3 |
| a06 | konversi | ya | - | 4150 | bge-m3 |
| a07 | fakta | ya | - | 2134 | bge-m3 |
| a08 | fakta | ya | - | 2377 | bge-m3 |
| a09 | fakta | tidak | sitasi_relevan, isi_benar | 2594 | bge-m3 |
| a10 | fakta | ya | - | 2630 | bge-m3 |
| a11 | fakta | ya | - | 2439 | bge-m3 |
| a12 | fakta | ya | - | 2585 | bge-m3 |
| a13 | tolak | ya | - | 1766 | bge-m3 |
| a14 | tolak | ya | - | 1474 | bge-m3 |
| a15 | tolak | ya | - | 2524 | bge-m3 |
| a16 | tolak | ya | - | 1968 | bge-m3 |

## qwen/qwen3.8-27b

| id | jenis | lulus | pemeriksaan gagal | token | retrieval |
|---|---|---|---|---|---|
| a01 | konversi | ya | - | 4092 | bge-m3 |
| a02 | konversi | ya | - | 5026 | bge-m3 |
| a03 | konversi | ya | - | 6307 | bge-m3 |
| a04 | konversi | ya | - | 4178 | bge-m3 |
| a05 | konversi | ya | - | 4928 | bge-m3 |
| a06 | konversi | ya | - | 4780 | bge-m3 |
| a07 | fakta | ya | - | 2365 | bge-m3 |
| a08 | fakta | ya | - | 2699 | bge-m3 |
| a09 | fakta | tidak | sitasi_relevan | 2758 | bge-m3 |
| a10 | fakta | ya | - | 2974 | bge-m3 |
| a11 | fakta | ya | - | 2770 | bge-m3 |
| a12 | fakta | ya | - | 2688 | bge-m3 |
| a13 | tolak | ya | - | 1946 | bge-m3 |
| a14 | tolak | ya | - | 1595 | bge-m3 |
| a15 | tolak | ya | - | 2904 | bge-m3 |
| a16 | tolak | ya | - | 2122 | bge-m3 |
