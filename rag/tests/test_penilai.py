import math

import pytest

from zrag.penilai import baca_putusan, kappa, penilai_untuk, pesan, ringkasan


def test_penilai_selalu_beda_keluarga():
    assert penilai_untuk("openai/gpt-oss-120b") == "qwen/qwen3.8-27b"
    assert penilai_untuk("qwen/qwen3.8-27b") == "openai/gpt-oss-120b"


def test_kappa():
    assert kappa(["a", "b", "a", "b"], ["a", "b", "a", "b"]) == 1.0
    # setuju 50% padahal kebetulan saja sudah 50% → kappa 0
    assert kappa(["a", "a", "b", "b"], ["a", "b", "a", "b"]) == pytest.approx(0.0)
    # contoh buku teks: 20 setuju-ya, 15 setuju-tidak, 5 dan 10 tidak setuju dari 50
    a = ["y"] * 20 + ["y"] * 5 + ["n"] * 10 + ["n"] * 15
    b = ["y"] * 20 + ["n"] * 5 + ["y"] * 10 + ["n"] * 15
    assert kappa(a, b) == pytest.approx(0.4)
    assert math.isnan(kappa([], []))


def test_baca_putusan():
    p = baca_putusan(
        'teks {"label": "sebagian", "sitasi_tepat": "tidak", "alasan": "x"} ekor'
    )
    assert p == {"label": "sebagian", "sitasi_tepat": "tidak", "alasan": "x"}
    assert (
        baca_putusan('{"label": "mungkin", "sitasi_tepat": "entah"}')["label"] is None
    )


def test_pesan_memuat_klaim_dan_bukti():
    k = {"klaim": "Klaim X.", "sitasi": [1], "bukti": ["[1] doc › bagian\nisi"]}
    isi = pesan(k)[1]["content"]
    assert "Klaim X." in isi and "isi" in isi and "[1]" in isi


def test_ringkasan_menghitung_klaim_bermasalah_yang_tertangkap():
    def pas(manusia, mesin, sm=None, sp=None):
        return (
            {"label": manusia, "sitasi_tepat": sm},
            {"label": mesin, "sitasi_tepat": sp},
        )

    data = [
        pas("didukung", "didukung", "ya", "ya"),
        pas("tidak_didukung", "sebagian", "tidak", "ya"),
        pas("sebagian", "didukung"),
        pas("bukan_klaim", "bukan_klaim"),
    ]
    s = ringkasan(data)
    assert s["n"] == 4 and s["setuju"] == 0.5
    assert (s["bermasalah_tertangkap"], s["bermasalah_manusia"]) == (1, 2)
    assert (s["sitasi_n"], s["sitasi_setuju"]) == (2, 0.5)
