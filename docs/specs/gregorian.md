# Spesifikasi: Kalender Gregorian (proleptik)

## Definisi
- **RD (Rata Die):** bilangan bulat hari; RD 1 = 1 Januari tahun 1 (Gregorian proleptik).
- **Proleptik:** aturan Gregorian berlaku juga sebelum 15 Oktober 1582.
- **Penomoran tahun astronomis:** tahun 0 = 1 SM, tahun −1 = 2 SM.

## Aturan
- Tahun kabisat: habis dibagi 4, kecuali habis dibagi 100 tetapi tidak habis dibagi 400.
- Panjang bulan: 31, 28/29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31.
- Siklus 400 tahun = 146.097 hari tepat.

## Rumus (semua pembagian = floor)
**Gregorian → RD:** dengan y' = tahun − 1,
RD = 365·y' + ⌊y'/4⌋ − ⌊y'/100⌋ + ⌊y'/400⌋ + ⌊(367·bulan − 362)/12⌋ + koreksi + tanggal,
koreksi = 0 (bulan ≤ 2), −1 (bulan > 2, kabisat), −2 (bulan > 2, bukan kabisat).

**RD → Gregorian:** uraikan d₀ = RD − 1 menjadi siklus 400 tahun (146.097 hari), 100 tahun (36.524), 4 tahun (1.461), dan 1 tahun (365) untuk mendapatkan tahun; lalu bulan dari jumlah hari sejak 1 Januari, dan tanggal sebagai sisanya.

## Validasi input
- Bulan 1–12; tanggal 1 sampai panjang bulan. Tanggal yang tidak ada (mis. 29 Februari 2025) **ditolak** dengan pesan jelas.

## Rencana uji
| Lapis | Uji |
|---|---|
| L1 jangkar | RD(1-01-01) = 1; RD(2026-11-04) = 739.924; RD(1945-08-17) = 710.260; RD 0 = 31 Des tahun 0 |
| L1 aturan | 1900 bukan kabisat; 2000 kabisat; 2100 bukan kabisat |
| L3 sifat | round-trip; hari berurutan; siklus 400 tahun = 146.097 hari |
| L4 pembanding | `datetime.date.toordinal()` Python (Gregorian proleptik, tahun 1–9999) |

## Sumber dan atribusi

Berdasarkan Dershowitz & Reingold (1990) [R13]. Penentuan tahun dari RD memakai
dekomposisi siklus 400/100/4/1 tahun yang dikoreksi Reingold, Dershowitz & Clamen
(1993) [R14]. Bentuk tertutup untuk bulan mengikuti kode CALENDRICA 4.0
(Reingold & Dershowitz, Apache-2.0) [R17] yang menyertai *Calendrical Calculations*
ed. ke-4 (Cambridge University Press, 2018) [R1]. Dukungan tahun astronomis nol dan
negatif diuji terpisah oleh Zetalmanac.

Catatan: R14 hlm. 386 menulis JD 0 = 24 November −4711 (Gregorian); yang benar −4713.

## Riwayat tinjauan

Ditinjau 5 November 2026 oleh Muhamad Zaky Kurniawan, terhadap R13 (1990) dan R14 (1993).

- [x] Penentuan tahun dari RD sama dengan dekomposisi siklus 400/100/4/1 versi koreksi R14,
      termasuk kasus n100 = 4 atau n1 = 4 (hari ke-366).
- [x] R13 dan R14 tidak menjamin hasil untuk RD ≤ 0. Zetalmanac memakai pembagian floor
      (`//`, `divmod`) dan mengujinya di `tests/test_gregorian_nonpositif.py`.
- [x] 29 Februari 1700, 1800, 1900, 2100 ditolak; 29 Februari 1600, 2000, 0, −400 diterima.
- [x] Salah cetak R14 hlm. 386 (JD 0 = 24 Nov −4711, seharusnya −4713) dicatat di §5.4 rencana.
- [ ] Nomor persamaan rumus ⌊(367m − 362)/12⌋ di buku R1 belum dicek (buku tidak tersedia).
- [x] Kasus tepi tambahan: bulan/tanggal di luar batas ditolak; bolak-balik RD ±10⁹ lolos
      (`tests/test_gregorian_tepi.py`).
