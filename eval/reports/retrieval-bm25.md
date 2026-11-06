# Evaluasi retrieval: BM25 per bahasa

Dataset: 36 kueri.

| kategori | n | recall@1 | recall@3 | recall@5 | recall@10 | mrr@10 |
|---|---|---|---|---|---|---|
| semua | 36 | 0.42 | 0.60 | 0.62 | 0.68 | 0.64 |
| id | 7 | 0.71 | 0.79 | 0.79 | 0.93 | 0.81 |
| en | 13 | 0.62 | 0.92 | 0.92 | 0.92 | 0.81 |
| lintas | 16 | 0.12 | 0.25 | 0.31 | 0.38 | 0.42 |

## Kueri dengan recall@5 < 1

| id | kategori | recall@5 | kueri | 3 teratas |
|---|---|---|---|---|
| q01 | lintas | 0.50 | kapan tahun kabisat hisab urfi | spec-hijri-urfi#0<br>spec-hijri-urfi#3<br>spec-hijri-urfi#2 |
| q02 | lintas | 0.00 | skema kabisat urfi I II III IV | wiki-en-julian-calendar#10<br>wiki-en-mesoamerican-long-count-calendar#5<br>wiki-en-gregorian-calendar#6 |
| q05 | id | 0.00 | nama-nama bulan hijriah | wiki-id-kalender-hijriah#5<br>wiki-id-kalender-hijriah#6<br>wiki-id-kalender-hijriah#3 |
| q07 | lintas | 0.50 | julian day epoch noon | wiki-en-julian-day#10<br>wiki-en-julian-day#0<br>wiki-en-julian-day#5 |
| q09 | lintas | 0.00 | convert gregorian date to julian day number | wiki-en-gregorian-calendar#14<br>wiki-en-julian-day#17<br>wiki-en-julian-day#21 |
| q10 | lintas | 0.50 | why was the gregorian calendar introduced | wiki-en-gregorian-calendar#5<br>wiki-en-chinese-calendar#37<br>wiki-en-chinese-calendar#10 |
| q11 | lintas | 0.00 | gregorian leap year rule for century years | wiki-en-gregorian-calendar#10<br>wiki-en-julian-calendar#1<br>wiki-en-gregorian-calendar#8 |
| q13 | lintas | 0.00 | selisih tanggal kalender julius dan gregorius | wiki-id-kalender-gregorius#2<br>wiki-id-kalender-gregorius#0<br>wiki-id-kalender-gregorius#1 |
| q14 | lintas | 0.50 | mengapa kalender julius diperkenalkan | wiki-id-kalender-julius#0<br>wiki-id-kalender-julius#1<br>wiki-id-kalender-hijriah#8 |
| q19 | lintas | 0.50 | aturan bulan kabisat kalender china | spec-china#1<br>spec-china#0<br>spec-china#3 |
| q20 | lintas | 0.00 | kapan tahun baru imlek | wiki-id-kalender-tionghoa#11<br>wiki-id-kalender-tionghoa#4<br>wiki-id-kalender-tionghoa#12 |
| q23 | lintas | 0.50 | chinese calendar leap month without major solar term | wiki-en-chinese-calendar#28<br>wiki-en-solar-term#2<br>wiki-en-chinese-calendar#29 |
| q25 | en | 0.00 | maya long count baktun katun tun winal kin | spec-maya#2<br>wiki-id-kalender-maya#1<br>wiki-id-kalender-maya#0 |
| q26 | lintas | 0.50 | GMT correlation constant 584283 | spec-maya#1<br>spec-maya#3 |
| q29 | lintas | 0.50 | kalender maya baktun | wiki-id-kalender-maya#0<br>wiki-id-kalender-maya#1<br>spec-maya#2 |
| q30 | lintas | 0.50 | korelasi kalender maya dengan kalender masehi | spec-maya#1<br>wiki-id-kalender-maya#1<br>wiki-id-kalender-maya#0 |
| q34 | lintas | 0.50 | mengapa calendar round berisi 52 tahun haab dan jarang dinyatakan sebagai 73 tahun tzolkin | spec-maya#0<br>wiki-id-kalender-maya#1<br>wiki-id-kalender-tionghoa#12 |
| q35 | lintas | 0.00 | bagaimana bulan tambahan ditempatkan di tahun kabisat kalender china | spec-china#3<br>wiki-id-kalender-julius#2<br>wiki-id-kalender-julius#0 |
| q36 | id | 0.50 | mengapa hari di kalender hijriyah dimulai saat matahari terbenam | wiki-id-kalender-hijriah#6<br>wiki-id-kalender-hijriah#1<br>wiki-id-kalender-tionghoa#6 |
