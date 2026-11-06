# Evaluasi retrieval

Dataset: 36 kueri, label diperiksa manusia.

## Ringkasan

| sistem | recall@5 semua | id | en | lintas | recall@10 semua | mrr@10 |
|---|---|---|---|---|---|---|
| BM25 | 0.62 | 0.79 | 0.92 | 0.31 | 0.68 | 0.64 |
| bge-m3 | 0.76 | 0.93 | 1.00 | 0.50 | 0.82 | 0.73 |
| BM25 + bge-m3 (RRF) | 0.69 | 0.93 | 0.92 | 0.41 | 0.79 | 0.71 |
| gemini-embedding-2 | 0.86 | 0.93 | 1.00 | 0.72 | 0.92 | 0.90 |
| BM25 + gemini-embedding-2 (RRF) | 0.69 | 0.93 | 0.92 | 0.41 | 0.79 | 0.75 |

## BM25

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.42 | 0.60 | 0.62 | 0.68 | 0.64 |
| id | 7 | 0.71 | 0.79 | 0.79 | 0.93 | 0.81 |
| en | 13 | 0.62 | 0.92 | 0.92 | 0.92 | 0.81 |
| lintas | 16 | 0.12 | 0.25 | 0.31 | 0.38 | 0.42 |

## bge-m3

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.51 | 0.69 | 0.76 | 0.82 | 0.73 |
| id | 7 | 0.64 | 0.93 | 0.93 | 0.93 | 0.81 |
| en | 13 | 0.77 | 0.96 | 1.00 | 1.00 | 0.92 |
| lintas | 16 | 0.25 | 0.38 | 0.50 | 0.62 | 0.55 |

## BM25 + bge-m3 (RRF)

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.47 | 0.64 | 0.69 | 0.79 | 0.71 |
| id | 7 | 0.79 | 0.79 | 0.93 | 0.93 | 0.89 |
| en | 13 | 0.69 | 0.88 | 0.92 | 1.00 | 0.86 |
| lintas | 16 | 0.16 | 0.38 | 0.41 | 0.56 | 0.51 |

## gemini-embedding-2

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.65 | 0.81 | 0.86 | 0.92 | 0.90 |
| id | 7 | 0.93 | 0.93 | 0.93 | 0.93 | 1.00 |
| en | 13 | 0.88 | 1.00 | 1.00 | 1.00 | 1.00 |
| lintas | 16 | 0.34 | 0.59 | 0.72 | 0.84 | 0.77 |

## BM25 + gemini-embedding-2 (RRF)

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.50 | 0.69 | 0.69 | 0.79 | 0.75 |
| id | 7 | 0.79 | 0.93 | 0.93 | 0.93 | 0.90 |
| en | 13 | 0.69 | 0.92 | 0.92 | 1.00 | 0.86 |
| lintas | 16 | 0.22 | 0.41 | 0.41 | 0.56 | 0.59 |

## recall@5 per kueri

| id | kategori | kueri | BM25 | bge-m3 | BM25 + bge-m3 (RRF) | gemini-embedding-2 | BM25 + gemini-embedding-2 (RRF) |
|---|---|---|---|---|---|---|---|
| q01 | lintas | kapan tahun kabisat hisab urfi | 0.50 | 0.50 | 0.50 | 1.00 | 0.50 |
| q02 | lintas | skema kabisat urfi I II III IV | 0.00 | 0.50 | 0.50 | 0.50 | 0.50 |
| q03 | id | apa beda epoch sipil dan astronomis kalender hijriah | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q04 | id | perbedaan hisab dan rukyat | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q05 | id | nama-nama bulan hijriah | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q06 | id | bagaimana tahun 1 kalender islam ditentukan | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q07 | lintas | julian day epoch noon | 0.50 | 0.00 | 0.50 | 0.50 | 0.50 |
| q08 | en | modified julian date MJD | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q09 | lintas | convert gregorian date to julian day number | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| q10 | lintas | why was the gregorian calendar introduced | 0.50 | 1.00 | 0.50 | 0.50 | 0.50 |
| q11 | lintas | gregorian leap year rule for century years | 0.00 | 0.00 | 0.00 | 0.50 | 0.00 |
| q12 | en | difference between julian and gregorian calendar dates | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q13 | lintas | selisih tanggal kalender julius dan gregorius | 0.00 | 1.00 | 0.00 | 1.00 | 0.00 |
| q14 | lintas | mengapa kalender julius diperkenalkan | 0.50 | 0.00 | 0.50 | 1.00 | 0.50 |
| q15 | en | julian calendar leap year error | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q16 | en | proleptic gregorian calendar | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q17 | en | what is a solar term jieqi | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q18 | en | how are solar terms determined by ecliptic longitude | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q19 | lintas | aturan bulan kabisat kalender china | 0.50 | 0.50 | 0.50 | 1.00 | 0.50 |
| q20 | lintas | kapan tahun baru imlek | 0.00 | 0.50 | 0.00 | 0.50 | 0.00 |
| q21 | id | dua belas shio | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q22 | id | zona waktu beijing kalender china sebelum 1929 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q23 | lintas | chinese calendar leap month without major solar term | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
| q24 | en | sexagenary cycle heavenly stems earthly branches | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q25 | en | maya long count baktun katun tun winal kin | 0.00 | 1.00 | 0.00 | 1.00 | 0.00 |
| q26 | lintas | GMT correlation constant 584283 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 |
| q27 | en | tzolkin 260 day calendar | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q28 | en | haab months and wayeb | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q29 | lintas | kalender maya baktun | 0.50 | 1.00 | 0.50 | 1.00 | 0.50 |
| q30 | lintas | korelasi kalender maya dengan kalender masehi | 0.50 | 0.50 | 0.50 | 1.00 | 0.50 |
| q31 | en | 2012 end of baktun 13 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q32 | en | lords of the night G1 to G9 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q33 | en | calendar round 52 years | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| q34 | lintas | mengapa calendar round berisi 52 tahun haab dan jarang dinyatakan sebagai 73 tahun tzolkin | 0.50 | 1.00 | 0.50 | 0.50 | 0.50 |
| q35 | lintas | bagaimana bulan tambahan ditempatkan di tahun kabisat kalender china | 0.00 | 0.00 | 0.50 | 1.00 | 0.50 |
| q36 | id | mengapa hari di kalender hijriyah dimulai saat matahari terbenam | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
