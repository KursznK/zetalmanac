"""Aturan kalender China diuji dengan data buatan dari tabel HKO.

Hari bulan baru dan hari zhongqi di sini disalin dari tabel HKO (hko.gov.hk, T2024e–T2034e),
jadi tes ini menguji ATURAN penomoran bulan dan bulan kabisat, terlepas dari hitungan astronomi.
"""

import pytest

from zetalmanac_core import gregorian
from zetalmanac_core.china import ChineseCalendar, day_ganzhi, year_ganzhi, year_label


def _rd(text):
    y, m, d = (int(x) for x in text.split("-"))
    return gregorian.to_rd(y, m, d)


NEW_MOONS = [
    # 2024
    "2024-01-11",
    "2024-02-10",
    "2024-03-10",
    "2024-04-09",
    "2024-05-08",
    "2024-06-06",
    "2024-07-06",
    "2024-08-04",
    "2024-09-03",
    "2024-10-03",
    "2024-11-01",
    "2024-12-01",
    "2024-12-31",
    # 2025 (bulan 6 kabisat mulai 25 Juli)
    "2025-01-29",
    "2025-02-28",
    "2025-03-29",
    "2025-04-28",
    "2025-05-27",
    "2025-06-25",
    "2025-07-25",
    "2025-08-23",
    "2025-09-22",
    "2025-10-21",
    "2025-11-20",
    "2025-12-20",
    # 2026
    "2026-01-19",
    "2026-02-17",
    "2026-03-19",
    "2026-04-17",
    "2026-05-17",
    "2026-06-15",
    "2026-07-14",
    "2026-08-13",
    "2026-09-11",
    "2026-10-10",
    "2026-11-09",
    "2026-12-09",
    "2027-01-08",  # perkiraan, hanya batas data (tidak diuji)
    # 2032
    "2032-01-13",
    "2032-02-11",
    "2032-03-12",
    "2032-04-10",
    "2032-05-09",
    "2032-06-08",
    "2032-07-07",
    "2032-08-06",
    "2032-09-05",
    "2032-10-04",
    "2032-11-03",
    "2032-12-03",
    # 2033 (bulan 11 kabisat mulai 22 Desember: "masalah 2033")
    "2033-01-01",
    "2033-01-31",
    "2033-03-01",
    "2033-03-31",
    "2033-04-29",
    "2033-05-28",
    "2033-06-27",
    "2033-07-26",
    "2033-08-25",
    "2033-09-23",
    "2033-10-23",
    "2033-11-22",
    "2033-12-22",
    # 2034
    "2034-01-20",
    "2034-02-19",
    "2034-03-20",
    "2034-04-19",
    "2034-05-18",
    "2034-06-16",
    "2034-07-16",
    "2034-08-14",
    "2034-09-13",
    "2034-10-12",
    "2034-11-11",
    "2034-12-11",
    "2035-01-09",  # perkiraan, hanya batas data (tidak diuji)
]

# Urutan zhongqi dalam setahun Gregorian: bujur Matahari 300 (大寒), 330 (雨水), 0 (春分), ..., 270 (冬至)
_LON = (300, 330, 0, 30, 60, 90, 120, 150, 180, 210, 240, 270)
ZHONGQI_PER_YEAR = {
    2024: [
        "01-20",
        "02-19",
        "03-20",
        "04-19",
        "05-20",
        "06-21",
        "07-22",
        "08-22",
        "09-22",
        "10-23",
        "11-22",
        "12-21",
    ],
    2025: [
        "01-20",
        "02-18",
        "03-20",
        "04-20",
        "05-21",
        "06-21",
        "07-22",
        "08-23",
        "09-23",
        "10-23",
        "11-22",
        "12-21",
    ],
    2026: [
        "01-20",
        "02-18",
        "03-20",
        "04-20",
        "05-21",
        "06-21",
        "07-23",
        "08-23",
        "09-23",
        "10-23",
        "11-22",
        "12-22",
    ],
    2032: [
        "01-20",
        "02-19",
        "03-20",
        "04-19",
        "05-20",
        "06-21",
        "07-22",
        "08-22",
        "09-22",
        "10-23",
        "11-22",
        "12-21",
    ],
    2033: [
        "01-20",
        "02-18",
        "03-20",
        "04-20",
        "05-21",
        "06-21",
        "07-22",
        "08-23",
        "09-23",
        "10-23",
        "11-22",
        "12-21",
    ],
    2034: [
        "01-20",
        "02-18",
        "03-20",
        "04-20",
        "05-21",
        "06-21",
        "07-23",
        "08-23",
        "09-23",
        "10-23",
        "11-22",
        "12-22",
    ],
}


@pytest.fixture(scope="module")
def cal():
    zhongqi = [
        (_rd(f"{year}-{md}"), lon)
        for year, dates in ZHONGQI_PER_YEAR.items()
        for md, lon in zip(dates, _LON)
    ]
    return ChineseCalendar([_rd(t) for t in NEW_MOONS], zhongqi)


@pytest.mark.parametrize(
    ("masehi", "imlek"),
    [
        ("2026-11-05", (2026, 9, False, 27)),
        ("2026-02-17", (2026, 1, False, 1)),  # Imlek 2026
        ("2026-02-16", (2025, 12, False, 29)),  # malam Imlek
        ("2025-01-29", (2025, 1, False, 1)),  # Imlek 2025
        ("2025-07-24", (2025, 6, False, 30)),
        ("2025-07-25", (2025, 6, True, 1)),  # bulan 6 kabisat
        ("2025-08-23", (2025, 7, False, 1)),
        ("2033-01-01", (2032, 12, False, 1)),
        ("2033-01-31", (2033, 1, False, 1)),
        ("2033-08-25", (2033, 8, False, 1)),  # bulan tanpa zhongqi, tapi BUKAN kabisat
        ("2033-11-22", (2033, 11, False, 1)),
        ("2033-12-22", (2033, 11, True, 1)),  # bulan 11 kabisat
        ("2034-01-20", (2033, 12, False, 1)),
        ("2034-02-19", (2034, 1, False, 1)),
    ],
)
def test_cocok_dengan_hko(cal, masehi, imlek):
    assert cal.from_rd(_rd(masehi)) == imlek
    assert cal.to_rd(*imlek) == _rd(masehi)


@pytest.mark.parametrize(
    ("dari", "sampai"), [("2025-01-01", "2026-12-08"), ("2033-01-01", "2034-12-10")]
)
def test_bolak_balik_dan_berurutan(cal, dari, sampai):
    prev = None
    for rd in range(_rd(dari), _rd(sampai) + 1):
        tanggal = cal.from_rd(rd)
        assert cal.to_rd(*tanggal) == rd
        if prev is not None and tanggal[3] != 1:
            assert tanggal[:3] == prev[:3] and tanggal[3] == prev[3] + 1
        prev = tanggal


@pytest.mark.parametrize(
    "imlek",
    [
        (2026, 6, True, 1),
        (2026, 13, False, 1),
        (2026, 8, False, 30),
    ],  # bulan 8/2026 cuma 29 hari
)
def test_tanggal_tidak_ada_ditolak(cal, imlek):
    with pytest.raises(ValueError):
        cal.to_rd(*imlek)


def test_di_luar_rentang_data_ditolak(cal):
    with pytest.raises(ValueError):
        cal.from_rd(_rd("2020-01-01"))


def test_ganzhi():
    assert year_ganzhi(2026) == "丙午"
    assert year_label(2026) == "Kuda Api"
    assert year_ganzhi(2025) == "乙巳"
    assert year_label(2025) == "Ular Kayu"
    assert day_ganzhi(_rd("2026-11-05")) == "癸未"
    assert day_ganzhi(_rd("2000-01-01")) == "戊午"
