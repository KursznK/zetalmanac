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


def test_kalender_bulanan_november_2026():
    from zetalmanac_core.convert import month_table

    tabel = month_table(2026, 11)
    hari = tabel["days"]
    assert tabel["month_name"] == "November"
    assert len(hari) == 30
    assert hari[0]["weekday"] == 0  # 1 Nov 2026 hari Minggu
    assert hari[4]["hijri"] == {
        "year": 1448,
        "month": 5,
        "day": 24,
        "month_name": "Jumadilawal",
    }
    assert hari[4]["china"]["label"] == "廿七"
    assert hari[8]["china"]["label"] == "十月"  # 9 Nov: awal bulan 10
    assert hari[11]["hijri"]["day"] == 1  # 12 Nov: 1 Jumadilakhir
    assert hari[21]["china"]["zhongqi"] == "小雪"  # 22 Nov
    assert [h["china"]["zhongqi"] for h in hari].count(None) == 29


def test_kalender_bulanan_kabisat_dan_rentang():
    from zetalmanac_core.convert import month_table

    juli = month_table(2025, 7)["days"]
    assert juli[24]["china"]["label"] == "闰六月"  # 25 Jul 2025
    assert month_table(1800, 1)["days"][0]["china"] is None
    with pytest.raises(ValueError):
        month_table(2026, 13)


def test_convert_dengan_langkah():
    hasil = convert("gregorian", "2026-11-05", steps=True)
    assert set(hasil["steps"]) == {"gregorian", "hijri", "maya"}
    assert "steps" not in convert("gregorian", "2026-11-05")
    assert set(convert("maya", "13.0.14.1.7", steps=True)["steps"]) == {"hijri", "maya"}


def test_hari_penting_berikutnya():
    from zetalmanac_core.convert import upcoming

    acara = upcoming(739925)  # 5 Nov 2026
    ringkas = [(a["nama"], a["label"], a["hari_lagi"]) for a in acara]
    assert ringkas == [
        ("Imlek 2027 · 丁未 (Kambing Api)", "Sabtu, 6 Februari 2027", 93),
        ("1 Ramadan 1448 H (urfi)", "Senin, 8 Februari 2027", 95),
        ("1 Syawal 1448 H (urfi)", "Rabu, 10 Maret 2027", 125),
        ("1 Muharam 1449 H (urfi)", "Minggu, 6 Juni 2027", 213),
    ]


def test_hari_penting_hari_ini_ikut_dihitung():
    from zetalmanac_core import gregorian
    from zetalmanac_core.convert import upcoming

    imlek_2026 = gregorian.to_rd(2026, 2, 17)
    assert upcoming(imlek_2026)[0]["hari_lagi"] == 0
    assert all("Imlek" not in a["nama"] for a in upcoming(gregorian.to_rd(2100, 6, 1)))
