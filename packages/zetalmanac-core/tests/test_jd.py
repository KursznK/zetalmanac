from zetalmanac_core import gregorian, jd, julian


def test_jd_nol_adalah_1_januari_4713_sm_julian():
    rd = jd.rd_from_jd(0.0)
    assert julian.from_rd(rd) == (-4712, 1, 1)  # tahun -4712 = 4713 SM
    assert jd.jdn_from_rd(rd) == 0


def test_j2000():
    # JD 2451545,0 = 1 Januari 2000 pukul 12.00
    rd = gregorian.to_rd(2000, 1, 1)
    assert jd.rd_from_jd(2451545.0) == rd
    assert jd.jd_from_rd(rd) == 2451544.5  # tengah malam awal hari itu
    assert jd.jdn_from_rd(rd) == 2451545


def test_hari_ini():
    rd = gregorian.to_rd(2026, 11, 5)
    assert jd.jdn_from_rd(rd) == 2461350
    assert jd.jd_from_rd(rd) == 2461349.5


def test_batas_tengah_malam():
    rd = gregorian.to_rd(2026, 11, 5)
    assert jd.rd_from_jd(2461349.5) == rd  # tepat tengah malam: hari baru
    assert jd.rd_from_jd(2461349.499) == rd - 1  # sesaat sebelumnya: hari kemarin
    assert jd.rd_from_jd(2461350.499) == rd  # menjelang tengah malam berikutnya


def test_jdn_bolak_balik():
    for rd in (-1721425, -1, 0, 1, 739925):
        assert jd.rd_from_jdn(jd.jdn_from_rd(rd)) == rd
