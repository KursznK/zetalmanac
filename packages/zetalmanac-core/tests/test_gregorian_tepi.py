import pytest

from zetalmanac_core.gregorian import from_rd, to_rd, validate


@pytest.mark.parametrize(
    ("year", "month", "day"),
    [
        (2026, 0, 1),  # bulan 0
        (2026, 13, 1),  # bulan 13
        (2026, 1, 0),  # tanggal 0
        (2026, 1, 32),  # Januari cuma 31 hari
        (2026, 4, 31),  # April cuma 30 hari
        (2026, 2, 30),  # Februari tidak pernah 30 hari
        (-1, 2, 29),  # tahun -1 (2 SM) bukan kabisat
    ],
)
def test_tanggal_tidak_ada_ditolak(year, month, day):
    with pytest.raises(ValueError):
        validate(year, month, day)


@pytest.mark.parametrize("rd", [-(10**9), -(10**7), 10**7, 10**9])
def test_bolak_balik_rd_sangat_jauh(rd):
    assert to_rd(*from_rd(rd)) == rd
