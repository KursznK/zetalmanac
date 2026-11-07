# Faithfulness per klaim: label manusia vs LLM penilai

Klaim: 58, berlabel manusia: 58, dinilai penilai: 58. Penilai selalu beda keluarga dengan penjawab.

## Kesepakatan

| penilai | n | setuju (4 label) | kappa (4 label) | kappa aman/bermasalah | klaim bermasalah tertangkap | setuju sitasi_tepat |
|---|---|---|---|---|---|---|
| semua | 58 | 0.81 | 0.53 | 0.50 | 9/13 | 0.82 (n=39) |
| openai/gpt-oss-120b | 35 | 0.86 | 0.49 | 0.46 | 3/6 | 0.84 (n=25) |
| qwen/qwen3.8-27b | 23 | 0.74 | 0.54 | 0.47 | 6/7 | 0.79 (n=14) |

## Faithfulness jawaban menurut label manusia

| model penjawab | didukung | sebagian | tidak_didukung | bukan_klaim | sitasi tidak tepat |
|---|---|---|---|---|---|
| openai/gpt-oss-120b | 16 | 2 | 5 | 0 | 6 |
| qwen/qwen3.8-27b | 29 | 3 | 3 | 0 | 2 |

## Klaim yang dinilai berbeda

| id | manusia | penilai | alasan penilai |
|---|---|---|---|
| gpt-oss-120b/a03/1 | didukung | sebagian | Klaim bahwa tanggal Maya Long Count untuk 21 Desember 2012 adalah 13.0.0.0.0 didukung oleh hasil tool konversi tanggal, tetapi tidak ditemukan dalam sumber sitasi [1] yang hanya membahas siklus piktun dan kutipan ahli tentang makna 2012. |
| gpt-oss-120b/a05/1 | didukung | sebagian | Klaim menyatakan 4 Oktober 1582 Julian setara dengan 14 Oktober 1582 Gregorian (didukung oleh tool), tetapi sitasi [3] secara eksplisit menyatakan 4 Okt 1582 (Julian) + 1 hari = 15 Okt 1582 (Gregorian), sehingga sitasi yang dikutip tidak mendukung klaim tersebut. |
| gpt-oss-120b/a06/1 | didukung | sebagian | Sumber [1] hanya menyebutkan tanggal 1 Januari 2000 dalam konteks perhitungan Julian Date, tetapi tidak menyatakan bahwa hari tersebut adalah hari Sabtu; informasi hari Sabtu hanya tersedia dari hasil tool konversi_tanggal. |
| gpt-oss-120b/a17/1 | didukung | tidak_didukung | Sumber sitasi [1] membahas kalender Tiongkok dan tidak memuat informasi tentang konversi tanggal 17 Maret 1987 ke kalender Hijriah, yang hanya tersedia pada hasil tool. |
| gpt-oss-120b/a09/1 | sebagian | didukung | Bukti [3] secara eksplisit menyatakan bahwa kalender China adalah kalender lunisolar yang memiliki bulan interkalasi (kabisat) yang disisipkan sesuai kebutuhan untuk menjaga sinkronisasi dengan musim, yang sesuai dengan inti klaim. |
| gpt-oss-120b/a12/2 | didukung | sebagian | Bukti menyatakan hisab dilakukan untuk membantu sebelum rukyat, tetapi tidak secara eksplisit menyebutkan bahwa hisab bertujuan memperkirakan 'kemungkinan visibilitas' atau bahwa rukyat memberikan 'konfirmasi nyata' sebagaimana diformulasikan dalam klaim. |
| qwen3.8-27b/a03/2 | didukung | tidak_didukung | Bukti tidak menyebutkan bahwa tanggal tersebut 'sering dikaitkan' dengan penyelesaian 13th bʼakʼtun |
| qwen3.8-27b/a04/1 | sebagian | didukung | Bukti menunjukkan 1 Januari 2027 dalam kalender China (tahun 丁未/Kambing Api) jatuh pada Sabtu, 6 Februari 2027 Masehi, sesuai klaim |
| qwen3.8-27b/a07/2 | didukung | tidak_didukung | Bukti menunjukkan epoch astronomis satu hari lebih awal, bukan lebih maju, sehingga klaim tidak didukung |
| qwen3.8-27b/a07/4 | sebagian | didukung | Bukti [2] menyatakan bahwa epoch civil dipetakan ke ICU islamic-civil dan epoch astronomical ke ICU islamic-tbla, sesuai klaim. |
| qwen3.8-27b/a08/4 | sebagian | didukung | Bukti menyebutkan penghilangan hari kabisat pada tahun abad yang tidak kelipatan 400, rata-rata tahun 365.2425 hari, dan bahwa ini lebih mendekati tahun surya serta mencegah drift kalender |
