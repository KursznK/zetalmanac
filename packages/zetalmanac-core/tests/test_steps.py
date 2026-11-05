import pytest

from zetalmanac_core import gregorian
from zetalmanac_core.steps import gregorian_steps, hijri_steps, maya_steps

RD_HARI_INI = 739925  # 5 Nov 2026


def test_langkah_gregorian():
    langkah = gregorian_steps(2026, 11, 5)
    assert langkah[-1]["baris"][-1] == "RD = 739125 + 491 + 306 + (-2) + 5 = 739925"


def test_langkah_hijriah():
    langkah = hijri_steps(RD_HARI_INI)
    semua = [baris for item in langkah for baris in item["baris"]]
    assert "n = 739925 − 227015 = 512910" in semua
    assert "512910 = 48 × 10631 + 2622" in semua
    assert "jumlah 2481 hari → sisa p = 141 hari di tahun 1448" in semua
    assert "m = ⌊(11 × 141 + 330) / 325⌋ = ⌊1881/325⌋ = 5 → Jumadilawal" in semua
    assert langkah[-1]["baris"][-1] == "d = 141 − 118 + 1 = 24"


def test_langkah_hijriah_setelah_magrib():
    langkah = hijri_steps(RD_HARI_INI, after_sunset=True)
    assert langkah[0]["judul"] == "Setelah magrib"
    assert langkah[-1]["baris"][-1].endswith("= 25")


def test_langkah_maya():
    semua = [baris for item in maya_steps(RD_HARI_INI) for baris in item["baris"]]
    assert "n = 2461350 − 584283 = 1877067" in semua
    assert "1877067 = 13 × 144000 + 5067 → baktun 13" in semua
    assert "nama = (n + 19) mod 20 = 6 → Manik'" in semua


@pytest.mark.parametrize("scheme", ["I", "II", "III", "IV"])
@pytest.mark.parametrize("epoch", ["civil", "astronomical"])
def test_langkah_selalu_sama_dengan_jawaban(scheme, epoch):
    # Setiap fungsi langkah memeriksa dirinya sendiri dengan assert terhadap modul kalendernya.
    for rd in range(gregorian.to_rd(1900, 1, 1), gregorian.to_rd(2100, 1, 1), 97):
        hijri_steps(rd, scheme, epoch)
        maya_steps(rd)
        y, m, d = gregorian.from_rd(rd)
        gregorian_steps(y, m, d)
