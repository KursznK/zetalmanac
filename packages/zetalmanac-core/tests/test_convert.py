import pytest

from zetalmanac_core.convert import convert


def test_gregorian_ke_semua_kalender():
    hasil = convert("gregorian", "2026-11-05")
    assert hasil["rd"] == 739925
    assert hasil["jdn"] == 2461350
    assert hasil["hari"] == "Kamis"
    assert hasil["gregorian"]["label"] == "5 November 2026"
    assert hasil["julian"]["label"] == "23 Oktober 2026"
    assert hasil["hijri"]["label"] == "24 Jumadilawal 1448 H"
    assert hasil["maya"]["long_count"] == "13.0.14.1.7"
    assert hasil["maya"]["tzolkin"] == "1 Manik'"
    assert hasil["maya"]["haab"] == "0 Keh"


def test_china():
    hasil = convert("gregorian", "2026-11-05")
    assert hasil["china"]["label"] == "九月廿七"
    assert hasil["china"]["year_ganzhi"] == "丙午"
    assert hasil["china"]["year_label"] == "Kuda Api"
    assert hasil["china"]["day_ganzhi"] == "癸未"


def test_china_di_luar_rentang_bernilai_none():
    assert convert("gregorian", "1800-01-01")["china"] is None


@pytest.mark.parametrize(
    ("calendar", "text", "opsi"),
    [
        ("julian", "2026-10-23", {}),
        ("hijri", "1448-05-24", {}),
        ("hijri", "1448-05-25", {"epoch": "astronomical"}),
        ("maya", "13.0.14.1.7", {}),
        ("maya", "13.0.14.1.5", {"correlation": 584285}),
        ("china", "2026-09-27", {}),
    ],
)
def test_semua_input_menuju_hari_yang_sama(calendar, text, opsi):
    assert convert(calendar, text, **opsi)["rd"] == 739925


def test_bulan_kabisat_china():
    assert (
        convert("china", "2025-06-01", leap=True)["gregorian"]["label"]
        == "25 Juli 2025"
    )


def test_setelah_magrib():
    hasil = convert("gregorian", "2026-11-05", after_sunset=True)
    assert hasil["hijri"]["label"] == "25 Jumadilawal 1448 H"
    assert hasil["gregorian"]["label"] == "5 November 2026"  # Masehi tidak ikut berubah


def test_after_sunset_diabaikan_untuk_input_hijriah():
    assert (
        convert("hijri", "1448-05-24", after_sunset=True)["hijri"]["label"]
        == "24 Jumadilawal 1448 H"
    )


def test_label_tahun_sebelum_masehi():
    assert convert("gregorian", "-43-03-15")["gregorian"]["label"] == "15 Maret 44 SM"


@pytest.mark.parametrize(
    ("calendar", "text"),
    [
        ("gregorian", "2026-02-30"),  # tanggal tidak ada
        ("gregorian", "5 November 2026"),  # format salah
        ("gregorian", "10000-01-01"),  # di luar rentang
        ("maya", "13.0.14.1"),  # kurang satu angka
        ("maya", "13.0.14.18.0"),  # winal maksimal 17
        ("china", "2026-08-30"),  # bulan 8/2026 hanya 29 hari
        ("persia", "1405-08-14"),  # kalender tidak dikenal
    ],
)
def test_input_tidak_valid_ditolak(calendar, text):
    with pytest.raises(ValueError):
        convert(calendar, text)
