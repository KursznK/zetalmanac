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

## Sumber
- R13: Dershowitz & Reingold (1990), "Calendrical Calculations", *Software—Practice and Experience* 20(9). Implementasi ditulis ulang sendiri.
- R15: Tøndering, *Calendar FAQ* (aturan kabisat).

## Catatan untuk peninjau
- [ ] Rumus di atas cocok dengan paper 1990 (bagian Gregorian)?
- [ ] Ada kasus tepi lain yang perlu diuji?
