import pytest

from zrag import keamanan
from zrag.embed import GalatHTTP
from zrag.jawab import KANARI
from zrag.keamanan import (
    MAKS_KARAKTER,
    InputDitolak,
    baca_skor_guard,
    bersihkan,
    masalah_keluaran,
    skor_injeksi,
)


def test_bersihkan_karakter_tak_terlihat_dan_spasi():
    # \u200b (zero-width space) dan \u202e (pembalik arah teks) sering dipakai menyamarkan serangan
    assert bersihkan("  kapan\u200b imlek\u202e?\n\n2027 ") == "kapan imlek? 2027"
    assert bersihkan("baris\tsatu\rdua") == "baris satu dua"


@pytest.mark.parametrize("teks", ["", "   ", "\u200b\u200b", "a" * (MAKS_KARAKTER + 1)])
def test_bersihkan_menolak(teks):
    with pytest.raises(InputDitolak):
        bersihkan(teks)


def test_bersihkan_menolak_bukan_teks():
    with pytest.raises(InputDitolak):
        bersihkan(None)  # type: ignore[arg-type]


def test_baca_skor_guard():
    assert (
        baca_skor_guard({"choices": [{"message": {"content": " 0.9994 "}}]}) == 0.9994
    )
    with pytest.raises(ValueError):
        baca_skor_guard({"choices": [{"message": {"content": "1.7"}}]})


def test_guard_gagal_terbuka(monkeypatch):
    def gagal(*a, **k):
        raise GalatHTTP(503, "HTTP 503")

    monkeypatch.setattr(keamanan, "post_json", gagal)
    monkeypatch.setattr(keamanan, "rahasia", lambda nama: "uji")
    assert skor_injeksi("apa saja") is None


@pytest.mark.parametrize(
    ("teks", "masalah"),
    [
        ("Jawaban biasa [1].", []),
        (f"Kode saya {KANARI}.", ["bocor_prompt"]),
        ("Aturan: WAJIB panggil tool dulu.", ["bocor_prompt"]),
        ("Halo <script>alert(1)</script>", ["html"]),
        ("<b>tebal</b>", ["html"]),
        ("Lihat https://contoh.example", ["tautan"]),
        ("Lihat www.contoh.example", ["tautan"]),
        ("1 < 2 dan 3 > 2", []),
    ],
)
def test_masalah_keluaran(teks, masalah):
    assert masalah_keluaran(teks) == masalah
