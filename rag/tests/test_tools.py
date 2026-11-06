from zetalmanac_core.convert import CALENDARS

from zrag.tools import KALENDER, KONVERSI, jalankan, konversi_tanggal


def test_enum_sama_dengan_core():
    assert set(KALENDER) == set(CALENDARS)
    enum = KONVERSI["function"]["parameters"]["properties"]["kalender"]["enum"]
    assert enum == list(KALENDER)


def test_konversi_ringkas():
    h = konversi_tanggal("hijri", "1448-09-01")
    assert h["gregorian"] == "8 Februari 2027"
    assert h["hari"] == "Senin"
    assert "urfi" in h["catatan"]


def test_china_di_luar_rentang():
    assert "di luar rentang" in konversi_tanggal("gregorian", "1800-01-01")["china"]


def test_galat_dikembalikan_sebagai_data():
    assert "galat" in konversi_tanggal("hijri", "1448-13-01")
    assert "galat" in konversi_tanggal("persia", "1400-01-01")


def test_jalankan_tahan_input_aneh():
    assert jalankan("tidak_ada", "{}")[1] == {"galat": "tool 'tidak_ada' tidak dikenal"}
    assert "galat" in jalankan("konversi_tanggal", "{rusak")[1]
    assert "galat" in jalankan("konversi_tanggal", "[1, 2]")[1]
    assert "galat" in jalankan("konversi_tanggal", "{}")[1]
    argumen, hasil = jalankan(
        "konversi_tanggal", '{"kalender": "maya", "tanggal": "13.0.0.0.0", "lain": 1}'
    )
    assert argumen["lain"] == 1  # dicatat apa adanya, tetapi tidak diteruskan ke fungsi
    assert hasil["gregorian"] == "21 Desember 2012"
