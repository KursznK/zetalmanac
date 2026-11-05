import pytest

from zetalmanac_core import gregorian, julian, maya


def _tzolkin(rd, correlation=maya.GMT):
    angka, nama = maya.tzolkin_from_rd(rd, correlation)
    return f"{angka} {maya.TZOLKIN_NAMES[nama - 1]}"


def _haab(rd, correlation=maya.GMT):
    bulan, tanggal = maya.haab_from_rd(rd, correlation)
    return f"{tanggal} {maya.HAAB_MONTHS[bulan - 1]}"


def test_hari_nol():
    rd = maya.epoch_rd()
    assert maya.long_count_from_rd(rd) == (0, 0, 0, 0, 0)
    assert _tzolkin(rd) == "4 Ajaw"
    assert _haab(rd) == "8 Kumk'u"
    assert maya.lord_of_night_from_rd(rd) == 9
    # GMT 584283: 11 Agustus 3114 SM (Gregorian) = 6 September 3114 SM (Julian)
    assert gregorian.from_rd(rd) == (-3113, 8, 11)
    assert julian.from_rd(rd) == (-3113, 9, 6)


def test_akhir_baktun_13_tahun_2012():
    rd = maya.rd_from_long_count(13, 0, 0, 0, 0)
    assert gregorian.from_rd(rd) == (2012, 12, 21)
    assert _tzolkin(rd) == "4 Ajaw"
    assert _haab(rd) == "3 K'ank'in"
    assert maya.lord_of_night_from_rd(rd) == 9


@pytest.mark.parametrize(
    ("correlation", "tanggal"),
    [(584283, (2012, 12, 21)), (584285, (2012, 12, 23)), (584286, (2012, 12, 24))],
)
def test_korelasi_menggeser_tanggal_gregorian(correlation, tanggal):
    rd = maya.rd_from_long_count(13, 0, 0, 0, 0, correlation)
    assert gregorian.from_rd(rd) == tanggal


def test_hari_ini():
    rd = gregorian.to_rd(2026, 11, 5)
    assert maya.long_count_from_rd(rd) == (13, 0, 14, 1, 7)
    assert _tzolkin(rd) == "1 Manik'"
    assert _haab(rd) == "0 Keh"


def test_hari_ini_korelasi_584285():
    rd = gregorian.to_rd(2026, 11, 5)
    assert maya.long_count_from_rd(rd, 584285) == (13, 0, 14, 1, 5)
    assert _tzolkin(rd, 584285) == "12 Chikchan"
    assert _haab(rd, 584285) == "18 Sak'"


@pytest.mark.parametrize(
    ("long_count", "tzolkin", "haab"),
    [
        (
            (9, 9, 2, 4, 8),
            "5 Lamat",
            "1 Mol",
        ),  # Palenque: K'inich Janaab Pakal naik takhta
        ((9, 12, 11, 5, 18), "6 Etz'nab'", "11 Yax"),  # Palenque: Pakal wafat
    ],
)
def test_prasasti_cocok_dengan_calendar_round_sendiri(long_count, tzolkin, haab):
    # Tidak bergantung pada korelasi: Tzolk'in dan Haab' dihitung dari Hitungan Panjang saja
    rd = maya.rd_from_long_count(*long_count)
    assert _tzolkin(rd) == tzolkin
    assert _haab(rd) == haab


def test_wayeb_hanya_5_hari():
    # 0.0.0.0.0 = 8 Kumk'u; 12 hari kemudian masuk Wayeb', 5 hari kemudian 0 Pop
    rd = maya.epoch_rd() + 12
    assert _haab(rd) == "0 Wayeb'"
    assert _haab(rd + 4) == "4 Wayeb'"
    assert _haab(rd + 5) == "0 Pop"


def test_siklus():
    rd = gregorian.to_rd(2026, 11, 5)
    assert maya.tzolkin_from_rd(rd + 260) == maya.tzolkin_from_rd(rd)
    assert maya.haab_from_rd(rd + 365) == maya.haab_from_rd(rd)
    assert maya.lord_of_night_from_rd(rd + 9) == maya.lord_of_night_from_rd(rd)
    # Calendar Round: kombinasi Tzolk'in + Haab' berulang tiap 18.980 hari (~52 tahun)
    assert maya.tzolkin_from_rd(rd + 18980) == maya.tzolkin_from_rd(rd)
    assert maya.haab_from_rd(rd + 18980) == maya.haab_from_rd(rd)


def test_bolak_balik():
    for rd in range(maya.epoch_rd() - 400_000, maya.epoch_rd() + 2_400_000, 997):
        assert maya.rd_from_long_count(*maya.long_count_from_rd(rd)) == rd


@pytest.mark.parametrize(
    "long_count",
    [
        (13, 20, 0, 0, 0),
        (13, 0, 20, 0, 0),
        (13, 0, 0, 18, 0),
        (13, 0, 0, 0, 20),
        (13, -1, 0, 0, 0),
    ],
)
def test_hitungan_panjang_tidak_valid(long_count):
    with pytest.raises(ValueError):
        maya.rd_from_long_count(*long_count)


def test_korelasi_tidak_dikenal_ditolak():
    with pytest.raises(ValueError):
        maya.epoch_rd(584280)
