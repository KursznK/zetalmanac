import pytest

from zetalmanac_core import gregorian, hijri_urfi, julian

SCHEMES = ("I", "II", "III", "IV")
EPOCHS = ("civil", "astronomical")


def test_epoch_sipil_jumat_16_juli_622_julian():
    rd = hijri_urfi.to_rd(1, 1, 1)
    assert rd == 227015
    assert julian.from_rd(rd) == (622, 7, 16)
    assert rd % 7 == 5  # 0 = Minggu, jadi 5 = Jumat


def test_epoch_astronomis_kamis_15_juli_622_julian():
    rd = hijri_urfi.to_rd(1, 1, 1, epoch="astronomical")
    assert julian.from_rd(rd) == (622, 7, 15)
    assert rd % 7 == 4  # Kamis


# Nilai acuan dari ICU (Node.js Intl, ICU 78): "islamic-civil" dan "islamic-tbla"
@pytest.mark.parametrize(
    ("masehi", "sipil", "astronomis"),
    [
        ((1936, 3, 24), (1355, 1, 1), (1355, 1, 2)),
        ((2000, 1, 1), (1420, 9, 24), (1420, 9, 25)),
        ((2024, 7, 8), (1446, 1, 1), (1446, 1, 2)),
        ((2026, 11, 5), (1448, 5, 24), (1448, 5, 25)),
        ((2027, 2, 8), (1448, 9, 1), (1448, 9, 2)),
        ((2027, 6, 6), (1449, 1, 1), (1449, 1, 2)),
        ((2052, 8, 26), (1475, 1, 1), (1475, 1, 2)),
        ((2100, 3, 1), (1523, 12, 19), (1523, 12, 20)),
    ],
)
def test_cocok_dengan_icu(masehi, sipil, astronomis):
    rd = gregorian.to_rd(*masehi)
    assert hijri_urfi.from_rd(rd) == sipil
    assert hijri_urfi.from_rd(rd, epoch="astronomical") == astronomis
    assert hijri_urfi.to_rd(*sipil) == rd


@pytest.mark.parametrize("scheme", SCHEMES)
def test_setiap_skema_11_kabisat_per_30_tahun(scheme):
    assert sum(hijri_urfi.is_leap_year(y, scheme) for y in range(1, 31)) == 11
    assert (
        hijri_urfi.to_rd(31, 1, 1, scheme) - hijri_urfi.to_rd(1, 1, 1, scheme) == 10631
    )


@pytest.mark.parametrize("scheme", SCHEMES)
def test_awal_siklus_sama_untuk_semua_skema(scheme):
    # Skema hanya menggeser letak kabisat di dalam siklus, bukan panjang siklusnya
    assert hijri_urfi.to_rd(1441, 1, 1, scheme) == hijri_urfi.to_rd(1441, 1, 1, "II")


@pytest.mark.parametrize(
    ("scheme", "hasil"),
    [
        ("I", (1448, 5, 24)),
        ("II", (1448, 5, 24)),
        ("III", (1448, 5, 25)),
        ("IV", (1448, 5, 25)),
    ],
)
def test_hari_ini_per_skema(scheme, hasil):
    # 1447 kabisat di skema I/II, tidak di skema III/IV, jadi tahun 1448 mulai sehari lebih awal
    rd = gregorian.to_rd(2026, 11, 5)
    assert hijri_urfi.from_rd(rd, scheme) == hasil


def test_setelah_magrib_sudah_tanggal_berikutnya():
    rd = gregorian.to_rd(2026, 11, 5)
    assert hijri_urfi.from_rd(rd, after_sunset=False) == (1448, 5, 24)
    assert hijri_urfi.from_rd(rd, after_sunset=True) == (1448, 5, 25)


def test_panjang_bulan():
    assert hijri_urfi.days_in_month(1448, 1) == 30  # Muharam
    assert hijri_urfi.days_in_month(1448, 2) == 29  # Safar
    assert (
        hijri_urfi.days_in_month(1448, 12) == 29
    )  # Zulhijah, 1448 bukan kabisat (skema II)
    assert hijri_urfi.days_in_month(1447, 12) == 30  # 1447 kabisat (skema II)


@pytest.mark.parametrize(
    ("tanggal", "scheme"),
    [
        ((1448, 2, 30), "II"),
        ((1448, 12, 30), "II"),
        ((1448, 13, 1), "II"),
        ((1448, 1, 0), "II"),
        ((1447, 12, 30), "III"),
    ],
)
def test_tanggal_tidak_ada_ditolak(tanggal, scheme):
    with pytest.raises(ValueError):
        hijri_urfi.validate(*tanggal, scheme)


@pytest.mark.parametrize(("scheme", "epoch"), [("V", "civil"), ("II", "julian")])
def test_parameter_tidak_dikenal_ditolak(scheme, epoch):
    with pytest.raises(ValueError):
        hijri_urfi.from_rd(739925, scheme, epoch)


def _besok(year, month, day, scheme):
    if day < hijri_urfi.days_in_month(year, month, scheme):
        return (year, month, day + 1)
    if month < 12:
        return (year, month + 1, 1)
    return (year + 1, 1, 1)


@pytest.mark.parametrize("epoch", EPOCHS)
@pytest.mark.parametrize("scheme", SCHEMES)
@pytest.mark.parametrize(("dari", "sampai"), [(-30, 30), (1380, 1500)])
def test_hari_berurutan(scheme, epoch, dari, sampai):
    # Setiap RD + 1 = besok, dan bolak-balik selalu kembali.
    # Rentang -30..30 melewati tahun 0; rentang 1380..1500 mencakup masa kini.
    awal = hijri_urfi.to_rd(dari, 1, 1, scheme, epoch)
    akhir = hijri_urfi.to_rd(sampai, 1, 1, scheme, epoch)
    tanggal = hijri_urfi.from_rd(awal, scheme, epoch)
    for rd in range(awal + 1, akhir + 1):
        tanggal = _besok(*tanggal, scheme)
        assert hijri_urfi.from_rd(rd, scheme, epoch) == tanggal
        assert hijri_urfi.to_rd(*tanggal, scheme, epoch) == rd
