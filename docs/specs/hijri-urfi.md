# Spesifikasi: Hijriah hisab urfi

## Aturan
- Bulan ganjil 30 hari, bulan genap 29 hari; Zulhijah 30 hari di tahun kabisat.
- Siklus 30 tahun = 10.631 hari, 11 tahun kabisat.
- Tahun memakai penomoran astronomis (ada tahun 0 dan negatif); label "sebelum Hijriah" diurus tampilan.
- Nama bulan mengikuti KBBI: Muharam, Safar, Rabiulawal, Rabiulakhir, Jumadilawal, Jumadilakhir,
  Rajab, Syakban, Ramadan, Syawal, Zulkaidah, Zulhijah.

## Parameter
- `scheme` (bawaan II): letak tahun kabisat dalam siklus (posisi 1–30):
  - I:   2, 5, 7, 10, 13, 15, 18, 21, 24, 26, 29
  - II:  2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29
  - III: 2, 5, 8, 10, 13, 16, 19, 21, 24, 27, 29
  - IV:  2, 5, 8, 11, 13, 16, 19, 21, 24, 27, 30
  Penamaan I–IV berbeda antar-literatur; yang mengikat adalah daftar di atas.
- `epoch` (bawaan civil): civil = Jumat 16 Juli 622 (Julian) = RD 227015;
  astronomical = Kamis 15 Juli 622 (Julian) = RD 227014.
- `after_sunset` (bawaan False): True berarti waktu setelah magrib, jadi tanggal Hijriah = milik hari sipil berikutnya.

## Kesetaraan
- II + civil = ICU `islamic-civil`; II + astronomical = ICU `islamic-tbla`.
- Golden file `tests/data/hijri_icu.csv` (54.937 baris: setiap pergantian bulan 1–2000 H
  untuk kedua epoch, dan setiap hari 1440–1460 H), dibuat oleh `scripts/gen_hijri_icu.mjs`.
- Skema I, III, IV belum punya pembanding independen; baru diuji lewat sifat strukturalnya.

## Jangkar uji
- 5 Nov 2026: 24 Jumadilawal 1448 (II, civil); 25 (II, astronomical); 25 (III/IV, civil).
- 1 Ramadan 1448 = 8 Feb 2027; 1 Muharam 1449 = 6 Jun 2027 (II, civil).

## Sumber
R13 (Dershowitz & Reingold 1990), R17 (CALENDRICA 4.0, fixed-from-islamic), ICU (pembanding).
Perluasan ke skema I, III, IV dan parameter after_sunset adalah bagian dari Zetalmanac.
