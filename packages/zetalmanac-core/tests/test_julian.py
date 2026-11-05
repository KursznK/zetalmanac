import pytest

from zetalmanac_core import gregorian, julian


def test_epoch_julian():
    # 1 Januari 1 M (Julian) = 30 Desember tahun 0 (Gregorian)
    assert julian.to_rd(1, 1, 1) == -1
    assert gregorian.from_rd(-1) == (0, 12, 30)


def test_reformasi_gregorian_1582():
    # Kamis 4 Oktober 1582 (Julian) langsung disusul Jumat 15 Oktober 1582 (Gregorian)
    assert julian.to_rd(1582, 10, 4) + 1 == gregorian.to_rd(1582, 10, 15)


def test_hari_ini_selisih_13_hari():
    rd = gregorian.to_rd(2026, 11, 5)
    assert julian.from_rd(rd) == (2026, 10, 23)


def test_abad_ketiga_kedua_kalender_sama():
    # Antara 1 Maret 200 dan 28 Februari 300 kedua kalender menunjuk hari yang sama
    assert julian.to_rd(250, 6, 1) == gregorian.to_rd(250, 6, 1)


@pytest.mark.parametrize("year", [1700, 1800, 1900, 2100, 0, -4])
def test_29_februari_ada_di_julian(year):
    julian.validate(year, 2, 29)


@pytest.mark.parametrize(
    ("year", "month", "day"), [(2026, 2, 29), (-1, 2, 29), (2026, 4, 31), (2026, 13, 1)]
)
def test_tanggal_tidak_ada_ditolak(year, month, day):
    with pytest.raises(ValueError):
        julian.validate(year, month, day)


def _besok(year, month, day):
    if day < julian.days_in_month(year, month):
        return (year, month, day + 1)
    if month < 12:
        return (year, month + 1, 1)
    return (year + 1, 1, 1)


def test_hari_berurutan():
    # Dari 1 Januari 4713 SM (tahun -4712) sampai 1 Januari 2101: setiap RD + 1 = besok
    awal = julian.to_rd(-4712, 1, 1)
    akhir = julian.to_rd(2101, 1, 1)
    tanggal = julian.from_rd(awal)
    for rd in range(awal + 1, akhir + 1):
        tanggal = _besok(*tanggal)
        assert julian.from_rd(rd) == tanggal
        assert julian.to_rd(*tanggal) == rd


@pytest.mark.parametrize("rd", [-(10**9), 10**9])
def test_bolak_balik_rd_sangat_jauh(rd):
    assert julian.to_rd(*julian.from_rd(rd)) == rd
