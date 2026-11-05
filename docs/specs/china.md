# Spesifikasi: Kalender China (农历)

## Aturan (pasca-1645)
1. Hari dimulai tengah malam waktu Beijing: UTC+8 sejak 1 Januari 1929; sebelumnya waktu
   lokal Beijing (bujur 116°25' T = UTC+7:45:40). Diuji terhadap HKO di Sesi 2.3: aturan ini
   memberi 1 awal bulan + 3 zhongqi berbeda pada 1901–1928, sedangkan UTC+8 untuk semua
   tahun memberi 90 hari (sekitar 3 bulan) + 3 zhongqi berbeda. Jadi aturan historis dipertahankan.
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

## Hasil validasi terhadap HKO (Sesi 2.3)
- 73.048 hari 1901–2100 (satu baris hilang di sumber: 30 Des 2069) dan 2.400 zhongqi dibandingkan.
- Cocok seluruhnya kecuali yang tercatat di `tests/test_china_hko_golden.py`:
  - 1906–1913: 1 awal bulan (24 Apr 1906) dan 3 zhongqi (1909, 1912, 1913). HKO mencatat hari
    berikutnya walaupun momennya 4–27 menit sebelum tengah malam waktu lokal. Dugaan: HKO
    mengikuti kalender resmi masa itu yang dihitung dengan teori lama. Belum dipastikan.
  - 2 awal bulan (28 Sep 2057, 7 Agu 2097) dan 1 zhongqi (春分 2084): momennya 0–2 menit
    setelah tengah malam; HKO sendiri menandai tanggal-tanggal ini tidak pasti.
  - 2 zhongqi (冬至 1951, 大寒 1979): kurang dari 30 detik sebelum tengah malam.
- Tampilan situs nanti memberi peringatan bila bulan baru atau zhongqi berjarak kurang dari
  15 menit dari tengah malam.

## Sumber
R4 (Aslaksen, *The Mathematics of the Chinese Calendar*), R5 (tabel HKO, oracle),
R6 (Skyfield + DE440s), R1/R17 (Reingold & Dershowitz, aturan bulan kabisat).
