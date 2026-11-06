import json

import pytest

from zrag.eval_jawaban import JENIS, argumen_tepat, load_dataset, memuat, nilai_item
from zrag.evaluate import cocok
from zrag.search import load_chunks
from zrag.tools import konversi_tanggal


def test_dataset_sah():
    data = load_dataset()
    ids = [d["id"] for d in data]
    assert len(ids) == len(set(ids))
    chunks = load_chunks()
    for d in data:
        assert d["jenis"] in JENIS, d["id"]
        # YAML memecah "February 8, 2027" tanpa tanda kutip dan mengubah 2027 jadi angka
        assert all(isinstance(p, str) for p in d.get("harus_memuat", [])), d["id"]
        if d["jenis"] == "konversi":
            # harapan dataset harus benar menurut core, bukan menurut ingatan penulisnya
            hasil = json.dumps(konversi_tanggal(**d["tool"]), ensure_ascii=False)
            assert memuat(hasil, d["harus_memuat"]), d["id"]
        if d["jenis"] == "fakta":
            for t in d["relevan"]:
                assert any(cocok(c, t) for c in chunks), (d["id"], t)


def test_argumen_tepat_dibandingkan_lewat_rd():
    harapan = {"kalender": "hijri", "tanggal": "1448-09-01"}
    assert argumen_tepat(harapan, {"kalender": "hijri", "tanggal": "1448-9-1"})
    assert not argumen_tepat(harapan, {"kalender": "hijri", "tanggal": "1448-09-02"})
    assert not argumen_tepat(
        harapan, {"kalender": "gregorian", "tanggal": "1448-09-01"}
    )
    assert not argumen_tepat(harapan, {"kalender": "hijri", "tanggal": "bukan tanggal"})
    assert not argumen_tepat(
        harapan, {"kalender": "hijri", "tanggal": "1448-09-01", "bulan_kabisat": True}
    )


CHUNKS = {
    "a#0": {"id": "a#0", "doc_id": "a", "section": "A › Aturan"},
    "b#0": {"id": "b#0", "doc_id": "b", "section": "B"},
}


def run(**kw):
    dasar = {
        "teks": "",
        "ditemukan": True,
        "sumber": [
            {"nomor": 1, "id": "a#0", "doc_id": "a", "section": "A › Aturan"},
            {"nomor": 2, "id": "b#0", "doc_id": "b", "section": "B"},
        ],
        "sitasi": [],
        "sitasi_tidak_sah": [],
        "tool": [],
    }
    return dasar | kw


def test_nilai_fakta():
    item = {
        "jenis": "fakta",
        "relevan": [{"doc": "a", "section": "Aturan"}],
        "harus_memuat": ["400"],
    }
    ok = nilai_item(item, run(teks="Siklus 400 tahun [1].", sitasi=[1]), CHUNKS)
    assert ok["lulus"]
    salah = nilai_item(item, run(teks="Siklus 400 tahun [2].", sitasi=[2]), CHUNKS)
    assert not salah["sitasi_relevan"] and not salah["lulus"]


def test_nilai_konversi_dan_tolak():
    item = {
        "jenis": "konversi",
        "tool": {"kalender": "gregorian", "tanggal": "2000-01-01"},
        "harus_memuat": ["Sabtu"],
    }
    tool = [
        {
            "nama": "konversi_tanggal",
            "argumen": {"kalender": "gregorian", "tanggal": "2000-1-1"},
        }
    ]
    assert nilai_item(item, run(teks="Hari Sabtu.", tool=tool), CHUNKS)["lulus"]
    tanpa_tool = nilai_item(item, run(teks="Hari Sabtu."), CHUNKS)
    assert not tanpa_tool["tool_dipanggil"] and not tanpa_tool["lulus"]

    tolak = {"jenis": "tolak"}
    assert nilai_item(tolak, run(ditemukan=False), CHUNKS)["lulus"]
    assert not nilai_item(tolak, run(ditemukan=True), CHUNKS)["lulus"]


def test_galat_dihitung_tidak_lulus():
    item = {"jenis": "tolak"}
    assert nilai_item(item, {"galat": "HTTP 400"}, CHUNKS) == {
        "tanpa_galat": False,
        "lulus": False,
    }


def test_memuat_menyamakan_spasi_dan_tanda_hubung_khusus():
    assert memuat("jatuh pada **8\u202fFebruari\u202f2027**", ["8 Februari 2027"])
    assert memuat("berbeda 1\u20112 hari", ["1-2 hari"])
    assert memuat("tanggal 8\u00a0Ramadan", ["8 Ramadan"])


@pytest.mark.parametrize("teks", ["SABTU", "hari sabtu"])
def test_memuat_tanpa_peduli_huruf(teks):
    assert memuat(teks, ["Sabtu"])
