# Evaluasi retrieval

Dataset: 36 kueri, label diperiksa manusia.

## Ringkasan

| sistem | recall@5 semua | id | en | lintas | recall@10 semua | mrr@10 |
|---|---|---|---|---|---|---|
| BM25 | 0.64 | 0.79 | 0.92 | 0.34 | 0.69 | 0.64 |
| BM25 dua bahasa | 0.66 | 0.79 | 0.96 | 0.36 | 0.75 | 0.45 |
| bge-m3 | 0.77 | 0.93 | 1.00 | 0.52 | 0.82 | 0.76 |
| BM25 dua bahasa + bge-m3 (RRF) | 0.74 | 0.93 | 1.00 | 0.44 | 0.80 | 0.71 |
| gemini-embedding-2 | 0.87 | 0.93 | 1.00 | 0.74 | 0.92 | 0.92 |
| BM25 dua bahasa + gemini-embedding-2 (RRF) | 0.76 | 0.93 | 1.00 | 0.49 | 0.81 | 0.79 |

## Uji tanda berpasangan terhadap bge-m3 (recall@5)

Per kueri: siapa yang lebih tinggi; seri diabaikan. p kecil (< 0,05) berarti selisihnya sulit dijelaskan sebagai kebetulan.

| sistem | sistem menang | bge-m3 menang | p (dua sisi) |
|---|---|---|---|
| BM25 | 2 | 9 | 0.07 |
| BM25 dua bahasa | 1 | 7 | 0.07 |
| BM25 dua bahasa + bge-m3 (RRF) | 2 | 4 | 0.69 |
| gemini-embedding-2 | 7 | 2 | 0.18 |
| BM25 dua bahasa + gemini-embedding-2 (RRF) | 3 | 3 | 1.00 |

## BM25

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.41 | 0.59 | 0.64 | 0.69 | 0.64 |
| id | 7 | 0.71 | 0.79 | 0.79 | 0.93 | 0.81 |
| en | 13 | 0.62 | 0.92 | 0.92 | 0.92 | 0.81 |
| lintas | 16 | 0.11 | 0.24 | 0.34 | 0.40 | 0.43 |

## BM25 dua bahasa

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.17 | 0.52 | 0.66 | 0.75 | 0.45 |
| id | 7 | 0.43 | 0.71 | 0.79 | 0.93 | 0.63 |
| en | 13 | 0.15 | 0.81 | 0.96 | 1.00 | 0.53 |
| lintas | 16 | 0.06 | 0.21 | 0.36 | 0.47 | 0.30 |

## bge-m3

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.52 | 0.71 | 0.77 | 0.82 | 0.76 |
| id | 7 | 0.64 | 0.93 | 0.93 | 0.93 | 0.81 |
| en | 13 | 0.77 | 0.96 | 1.00 | 1.00 | 0.92 |
| lintas | 16 | 0.26 | 0.41 | 0.52 | 0.64 | 0.60 |

## BM25 dua bahasa + bge-m3 (RRF)

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.47 | 0.67 | 0.74 | 0.80 | 0.71 |
| id | 7 | 0.71 | 0.79 | 0.93 | 0.93 | 0.82 |
| en | 13 | 0.77 | 0.96 | 1.00 | 1.00 | 0.92 |
| lintas | 16 | 0.11 | 0.39 | 0.44 | 0.57 | 0.48 |

## gemini-embedding-2

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.66 | 0.82 | 0.87 | 0.92 | 0.92 |
| id | 7 | 0.93 | 0.93 | 0.93 | 0.93 | 1.00 |
| en | 13 | 0.88 | 1.00 | 1.00 | 1.00 | 1.00 |
| lintas | 16 | 0.35 | 0.62 | 0.74 | 0.84 | 0.82 |

## BM25 dua bahasa + gemini-embedding-2 (RRF)

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.55 | 0.72 | 0.76 | 0.81 | 0.79 |
| id | 7 | 0.71 | 0.93 | 0.93 | 0.93 | 0.83 |
| en | 13 | 0.85 | 0.96 | 1.00 | 1.00 | 0.96 |
| lintas | 16 | 0.24 | 0.44 | 0.49 | 0.60 | 0.63 |

## recall@5 per kueri

| id | kategori | kueri | BM25 | BM25 dua bahasa | bge-m3 | BM25 dua bahasa + bge-m3 (RRF) | gemini-embedding-2 | BM25 dua bahasa + gemini-embedding-2 (RRF) |
|---|---|---|---|---|---|---|---|---|
| q01 | lintas | kapan tahun kabisat hisab urfi | 0.50 | 0.50 | 0.50 | 0.50 | 1.00 | 0.50 |
| q02 | lintas | skema kabisat urfi I II III IV | 0.00 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
| q03 | id | apa beda epoch sipil dan astronomis kalender hijriah | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q04 | id | perbedaan hisab dan rukyat | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q05 | id | nama-nama bulan hijriah | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q06 | id | bagaimana tahun 1 kalender islam ditentukan | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q07 | lintas | julian day epoch noon | 0.50 | 0.50 | 0.00 | 0.50 | 0.50 | 0.50 |
| q08 | en | modified julian date MJD | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q09 | lintas | convert gregorian date to julian day number | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| q10 | lintas | why was the gregorian calendar introduced | 0.67 | 0.33 | 1.00 | 0.67 | 0.67 | 1.00 |
| q11 | lintas | gregorian leap year rule for century years | 0.33 | 0.00 | 0.33 | 0.33 | 0.67 | 0.33 |
| q12 | en | difference between julian and gregorian calendar dates | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q13 | lintas | selisih tanggal kalender julius dan gregorius | 0.00 | 0.00 | 1.00 | 0.00 | 1.00 | 0.00 |
| q14 | lintas | mengapa kalender julius diperkenalkan | 0.50 | 0.00 | 0.00 | 0.00 | 1.00 | 0.50 |
| q15 | en | julian calendar leap year error | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q16 | en | proleptic gregorian calendar | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q17 | en | what is a solar term jieqi | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q18 | en | how are solar terms determined by ecliptic longitude | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q19 | lintas | aturan bulan kabisat kalender china | 0.50 | 0.50 | 0.50 | 0.50 | 1.00 | 0.50 |
| q20 | lintas | kapan tahun baru imlek | 0.00 | 0.00 | 0.50 | 0.00 | 0.50 | 0.00 |
| q21 | id | dua belas shio | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q22 | id | zona waktu beijing kalender china sebelum 1929 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q23 | lintas | chinese calendar leap month without major solar term | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
| q24 | en | sexagenary cycle heavenly stems earthly branches | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q25 | en | maya long count baktun katun tun winal kin | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q26 | lintas | GMT correlation constant 584283 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q27 | en | tzolkin 260 day calendar | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q28 | en | haab months and wayeb | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q29 | lintas | kalender maya baktun | 0.50 | 0.50 | 1.00 | 0.50 | 1.00 | 0.50 |
| q30 | lintas | korelasi kalender maya dengan kalender masehi | 0.50 | 0.50 | 0.50 | 0.50 | 1.00 | 0.50 |
| q31 | en | 2012 end of baktun 13 | 1.00 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 |
| q32 | en | lords of the night G1 to G9 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q33 | en | calendar round 52 years | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q34 | lintas | mengapa calendar round berisi 52 tahun haab dan jarang dinyatakan sebagai 73 tahun tzolkin | 0.50 | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 |
| q35 | lintas | bagaimana bulan tambahan ditempatkan di tahun kabisat kalender china | 0.00 | 0.00 | 0.00 | 0.50 | 1.00 | 0.50 |
| q36 | id | mengapa hari di kalender hijriyah dimulai saat matahari terbenam | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
