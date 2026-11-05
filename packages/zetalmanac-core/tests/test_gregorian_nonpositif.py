import pytest

from zetalmanac_core.gregorian import days_in_month, from_rd, to_rd, validate


@pytest.mark.parametrize("year", [1700, 1800, 1900, 2100, -100])
def test_29_februari_tahun_abad_ditolak(year):
    with pytest.raises(ValueError):
        validate(year, 2, 29)


@pytest.mark.parametrize("year", [1600, 2000, 2024, 0, -4, -400])
def test_29_februari_yang_memang_ada(year):
    validate(year, 2, 29)


def test_jangkar_jd_nol():
    # JD 0 = 1 Januari 4713 SM (Julian) = 24 November -4713 (Gregorian, tahun astronomis)
    assert from_rd(-1721425) == (-4713, 11, 24)
    assert to_rd(-4713, 11, 24) == -1721425


def test_jangkar_tahun_nol():
    assert from_rd(0) == (0, 12, 31)
    assert to_rd(0, 1, 1) == -365  # tahun 0 kabisat, jadi 366 hari


def _besok(year, month, day):
    if day < days_in_month(year, month):
        return (year, month, day + 1)
    if month < 12:
        return (year, month + 1, 1)
    return (year + 1, 1, 1)


def test_hari_berurutan_melewati_rd_nol():
    # 400 tahun sebelum 1 M sampai 1 Januari 2 M: setiap RD + 1 harus jadi "besok"
    awal = to_rd(-400, 1, 1)
    akhir = to_rd(2, 1, 1)
    tanggal = from_rd(awal)
    for rd in range(awal + 1, akhir + 1):
        tanggal = _besok(*tanggal)
        assert from_rd(rd) == tanggal
        assert to_rd(*tanggal) == rd
