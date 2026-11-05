"""Kalender China dengan tabel astronomi asli (data/china_astro.json)."""

import pytest

from zetalmanac_core import china, gregorian


def _rd(text):
    y, m, d = (int(x) for x in text.split("-"))
    return gregorian.to_rd(y, m, d)


# Dari tabel HKO (hko.gov.hk, T2024e, T2025e, T2026e, T2033e, T2034e)
@pytest.mark.parametrize(
    ("masehi", "imlek"),
    [
        ("2026-11-05", (2026, 9, False, 27)),
        ("2026-10-10", (2026, 9, False, 1)),  # bulan baru 23.50 waktu Beijing
        ("2026-10-09", (2026, 8, False, 29)),
        ("2026-02-17", (2026, 1, False, 1)),
        ("2025-07-25", (2025, 6, True, 1)),  # bulan 6 kabisat
        ("2025-08-23", (2025, 7, False, 1)),
        ("2024-02-10", (2024, 1, False, 1)),
        ("2033-08-25", (2033, 8, False, 1)),  # tanpa zhongqi, tapi bukan kabisat
        ("2033-12-22", (2033, 11, True, 1)),  # bulan 11 kabisat ("masalah 2033")
        ("2034-02-19", (2034, 1, False, 1)),
    ],
)
def test_cocok_dengan_hko(masehi, imlek):
    assert china.from_rd(_rd(masehi)) == imlek
    assert china.to_rd(*imlek) == _rd(masehi)


def test_tabel_lengkap():
    cal = china.default_calendar()
    assert len(cal.new_moons) > 2400
    assert len(cal.solstices) >= 202


def test_sifat_1900_2100():
    """Untuk setiap hari 1 Jan 1901 sampai 31 Des 2100:
    bolak-balik kembali, tanggal naik satu per hari, bulan 29 atau 30 hari,
    Imlek selalu jatuh 21 Januari–20 Februari, dan setiap tahun punya 12 atau 13 bulan."""
    awal, akhir = _rd("1901-01-01"), _rd("2100-12-31")
    prev = china.from_rd(awal - 1)
    month_length = None
    months_per_year = {}
    for rd in range(awal, akhir + 1):
        tanggal = china.from_rd(rd)
        assert china.to_rd(*tanggal) == rd
        year, month, leap, day = tanggal
        if day == 1:
            if month_length is not None:
                assert prev[3] in (29, 30), f"bulan {prev} panjangnya {prev[3]} hari"
            month_length = 0
            months_per_year[year] = months_per_year.get(year, 0) + 1
            if month == 1 and not leap:
                y, m, d = gregorian.from_rd(rd)
                assert (m, d) >= (1, 21) and (m, d) <= (2, 20), (
                    f"Imlek {year} jatuh {y}-{m}-{d}"
                )
        else:
            assert tanggal[:3] == prev[:3] and day == prev[3] + 1
        prev = tanggal
    for year in range(1902, 2100):
        assert months_per_year[year] in (12, 13), (
            f"tahun {year} punya {months_per_year[year]} bulan"
        )
