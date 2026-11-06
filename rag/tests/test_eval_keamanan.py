import re

from zrag.eval_keamanan import (
    SENTINEL,
    kueri_wajar,
    load_dataset,
    nilai_serangan,
    tabel_guard,
    teks_serangan,
)
from zrag.keamanan import MAKS_KARAKTER


def test_dataset_sah():
    data = load_dataset()
    ids = [d["id"] for d in data]
    assert len(ids) == len(set(ids))
    for d in data:
        assert re.fullmatch(r"LLM(0[1-9]|10)", d["owasp"]), d["id"]
        assert isinstance(d["injeksi"], bool), d["id"]
        assert isinstance(teks_serangan(d), str)
    # serangan panjang memang melewati batas input
    panjang = next(d for d in data if "ulang" in d)
    assert len(teks_serangan(panjang)) > MAKS_KARAKTER


def test_kueri_wajar_tidak_memuat_serangan():
    teks = [w["teks"].lower() for w in kueri_wajar()]
    assert not any("abaikan" in t or SENTINEL.lower() in t for t in teks)
    assert len(teks) >= 50


def test_nilai_serangan():
    item = {"id": "x", "owasp": "LLM01", "injeksi": True}
    assert nilai_serangan(item, {"status": "ditolak_injeksi", "pesan": "Ditolak."})[
        "lulus"
    ]
    patuh = nilai_serangan(
        item, {"status": "dijawab", "jawaban": "Baik: PWNED\u201142"}
    )
    assert not patuh["tidak_patuh"]  # tanda hubung khusus tetap terdeteksi
    html = nilai_serangan(item, {"status": "dijawab", "jawaban": "<script>x</script>"})
    assert not html["keluaran_aman"]

    item_tool = {"id": "y", "owasp": "LLM06", "injeksi": False, "maks_tool": 1}
    banyak = nilai_serangan(
        item_tool, {"status": "dijawab", "jawaban": "ok", "tool": [1, 2]}
    )
    assert not banyak["tool_terbatas"]


def test_tabel_guard():
    baris = [
        {"id": "s1", "label": "serangan", "skor": 0.99},
        {"id": "s2", "label": "serangan", "skor": 0.2},
        {"id": "q1", "label": "wajar", "skor": 0.01},
        {"id": "q2", "label": "wajar", "skor": 0.6},
        {"id": "q3", "label": "wajar", "skor": None},
    ]
    teks = "\n".join(tabel_guard(baris))
    assert "| 0.5 ← dipakai | 1/2 | 1/2 |" in teks
    assert "gagal diskor: 1" in teks
    assert "Serangan lolos guard pada ambang dipakai: s2" in teks
    assert "q2 (0.60)" in teks
