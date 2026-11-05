# Spesifikasi: Kalender China (农历)

## Aturan (pasca-1645)
1. Hari dimulai tengah malam waktu Beijing: UTC+8 sejak 1 Januari 1929; sebelumnya waktu
   lokal Beijing (bujur 116°25' T = UTC+7:45:40). Aturan sebelum 1929 masih hipotesis yang
   diuji terhadap HKO di Sesi 2.3.
2. Bulan dimulai pada hari (waktu Beijing) terjadinya bulan baru.
3. 冬至 (bujur semu Matahari 270°) selalu berada di bulan 11.
4. Kalau dari bulan 11 ke bulan 11 berikutnya ada 13 bulan, bulan pertama tanpa zhongqi
   (bujur Matahari kelipatan 30°) menjadi bulan kabisat dengan nomor bulan sebelumnya.
5. Tahun = tahun Gregorian saat Imlek-nya. Ganzhi tahun: (tahun − 4) mod 60.
   Ganzhi hari: (JDN − 11) mod 60, dengan 0 = 甲子.

## Arsitektur
- `scripts/gen_china_astro.py` (Skyfield + JPL DE440s, dijalankan offline) menulis momen UTC
  semua bulan baru dan zhongqi Nov 1899–Mar 2102 ke `src/zetalmanac_core/data/china_astro.json`.
- `china.py` hanya menerapkan aturan di atas pada tabel itu (tanpa efemeris saat runtime).
- `ChineseCalendar` menerima daftar hari, sehingga aturan bisa diuji dengan data salinan HKO
  tanpa bergantung pada hitungan astronomi.

## Rentang
1 Januari 1901 – 31 Desember 2100 (sama dengan tabel HKO). Di luar data → `ValueError`.

## Kasus tepi yang diawasi
- Bulan baru/zhongqi dekat tengah malam, mis. bulan baru 10 Okt 2026 pukul 23.50 waktu Beijing.
- "Masalah 2033": bulan 8/2033 tanpa zhongqi tetapi bukan kabisat; kabisat jatuh di bulan 11.
- HKO mencatat tanggal yang bisa meleset 1 hari karena ketidakpastian: bulan baru 28 Sep 2057,
  4 Sep 2089, 7 Agu 2097; 冬至 2021; 春分 2051 dan 2084; 立春 2083.

## Sumber
R4 (Aslaksen, *The Mathematics of the Chinese Calendar*), R5 (tabel HKO, oracle),
R6 (Skyfield + DE440s), R1/R17 (Reingold & Dershowitz, aturan bulan kabisat).
