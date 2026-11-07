# Evaluasi jawaban (RAG + tool)

Dataset: 17 pertanyaan (konversi, fakta, tolak). Retrieval: bge-m3 (ADR 0001).

## Ringkasan (pertanyaan lulus / jumlah)

| model | konversi | fakta | tolak | total | token rata-rata | detik rata-rata |
|---|---|---|---|---|---|---|
| openai/gpt-oss-120b | 7/7 | 5/6 | 4/4 | 16/17 | 3213 | 2.8 |
| qwen/qwen3.8-27b | 5/7 | 5/6 | 4/4 | 14/17 | 3235 | 6.5 |

## openai/gpt-oss-120b

| id | jenis | lulus | pemeriksaan gagal | token | retrieval |
|---|---|---|---|---|---|
| a01 | konversi | ya | - | 3878 | bge-m3 |
| a02 | konversi | ya | - | 4826 | bge-m3 |
| a03 | konversi | ya | - | 5669 | bge-m3 |
| a04 | konversi | ya | - | 4007 | bge-m3 |
| a05 | konversi | ya | - | 4353 | bge-m3 |
| a06 | konversi | ya | - | 4268 | bge-m3 |
| a17 | konversi | ya | - | 4568 | bge-m3 |
| a07 | fakta | ya | - | 2207 | bge-m3 |
| a08 | fakta | ya | - | 2428 | bge-m3 |
| a09 | fakta | tidak | sitasi_relevan, isi_benar | 2561 | bge-m3 |
| a10 | fakta | ya | - | 2692 | bge-m3 |
| a11 | fakta | ya | - | 2512 | bge-m3 |
| a12 | fakta | ya | - | 2654 | bge-m3 |
| a13 | tolak | ya | - | 1833 | bge-m3 |
| a14 | tolak | ya | - | 1535 | bge-m3 |
| a15 | tolak | ya | - | 2588 | bge-m3 |
| a16 | tolak | ya | - | 2036 | bge-m3 |

## qwen/qwen3.8-27b

| id | jenis | lulus | pemeriksaan gagal | token | retrieval |
|---|---|---|---|---|---|
| a01 | konversi | tidak | tool_dipanggil, argumen_tepat | 1985 | bge-m3 |
| a02 | konversi | ya | - | 5144 | bge-m3 |
| a03 | konversi | tidak | tool_dipanggil, argumen_tepat | 3081 | bge-m3 |
| a04 | konversi | ya | - | 4302 | bge-m3 |
| a05 | konversi | ya | - | 5037 | bge-m3 |
| a06 | konversi | ya | - | 4896 | bge-m3 |
| a17 | konversi | ya | - | 5056 | bge-m3 |
| a07 | fakta | ya | - | 2468 | bge-m3 |
| a08 | fakta | ya | - | 2785 | bge-m3 |
| a09 | fakta | tidak | sitasi_relevan, isi_benar | 2744 | bge-m3 |
| a10 | fakta | ya | - | 3012 | bge-m3 |
| a11 | fakta | ya | - | 2820 | bge-m3 |
| a12 | fakta | ya | - | 2828 | bge-m3 |
| a13 | tolak | ya | - | 2015 | bge-m3 |
| a14 | tolak | ya | - | 1659 | bge-m3 |
| a15 | tolak | ya | - | 2972 | bge-m3 |
| a16 | tolak | ya | - | 2191 | bge-m3 |
