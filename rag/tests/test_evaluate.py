import pytest

from zrag.evaluate import cocok, kategori, load_dataset, nilai
from zrag.ingest import build
from zrag.manifest import load

A = {"doc_id": "a", "section": "Judul A"}
A_SEJARAH = {"doc_id": "a", "section": "Judul A › Sejarah"}
A_SEJARAH_AWAL = {"doc_id": "a", "section": "Judul A › Sejarah › Masa awal"}
B = {"doc_id": "b", "section": "Judul B"}


def test_cocok_dokumen_bagian_dan_intro():
    assert cocok(A_SEJARAH, {"doc": "a"})
    assert cocok(A_SEJARAH, {"doc": "a", "section": "Sejarah"})
    assert cocok(A_SEJARAH, {"doc": "a", "section": "Judul A › Sejarah"})
    assert not cocok(A_SEJARAH, {"doc": "a", "section": "(intro)"})
    assert cocok(A, {"doc": "a", "section": "(intro)"})
    assert not cocok(B, {"doc": "a"})


def test_cocok_judul_utuh_dan_bukan_sub_bagian():
    """Label menunjuk satu bagian; sub-bagian dan judul yang hanya mirip tidak ikut dihitung."""
    assert not cocok(A_SEJARAH_AWAL, {"doc": "a", "section": "Sejarah"})
    assert cocok(A_SEJARAH_AWAL, {"doc": "a", "section": "Sejarah › Masa awal"})
    assert not cocok(A_SEJARAH, {"doc": "a", "section": "Sejar"})


def test_nilai_recall_dan_mrr():
    targets = [{"doc": "a", "section": "Sejarah"}, {"doc": "b"}]
    skor = nilai([A, B, A_SEJARAH], targets)
    assert skor["recall@1"] == 0.0
    assert skor["recall@3"] == 1.0
    assert skor["mrr@10"] == pytest.approx(
        1 / 2
    )  # yang relevan pertama: B di peringkat 2


def test_tanpa_hasil_relevan():
    assert nilai([B], [{"doc": "a"}]) == {
        "recall@1": 0.0,
        "recall@3": 0.0,
        "recall@5": 0.0,
        "recall@10": 0.0,
        "mrr@10": 0.0,
    }


def test_kategori_dihitung_dari_bahasa():
    bahasa = {"x": "id", "y": "en"}
    assert kategori({"lang": "id", "relevan": [{"doc": "x"}]}, bahasa) == "id"
    assert (
        kategori({"lang": "id", "relevan": [{"doc": "x"}, {"doc": "y"}]}, bahasa)
        == "lintas"
    )


def test_dataset_sah():
    """Setiap label harus menunjuk dokumen dan bagian yang benar-benar ada (cegah salah ketik)."""
    dataset = load_dataset()
    dokumen = {e["id"] for e in load()}
    chunks = build()
    ids = [item["id"] for item in dataset]
    assert len(ids) == len(set(ids)), "id kueri ganda"
    for item in dataset:
        assert item["lang"] in {"id", "en"}, item["id"]
        assert item["relevan"], item["id"]
        for t in item["relevan"]:
            assert t["doc"] in dokumen, (item["id"], t)
            assert any(cocok(c, t) for c in chunks), (
                item["id"],
                t,
                "bagian tidak ditemukan",
            )


def test_uji_tanda():
    from zrag.evaluate import uji_tanda

    def b(*nilai_r5):
        return [{"recall@5": x} for x in nilai_r5]

    # 9 menang lawan 2 (2 seri diabaikan): p = 2 * (C(11,0)+C(11,1)+C(11,2)) / 2^11
    a = b(*([1.0] * 9 + [0.0] * 2 + [0.5] * 2))
    c = b(*([0.0] * 9 + [1.0] * 2 + [0.5] * 2))
    menang_a, menang_c, p = uji_tanda(a, c)
    assert (menang_a, menang_c) == (9, 2)
    assert p == pytest.approx(2 * (1 + 11 + 55) / 2048)
    assert uji_tanda(b(1.0), b(1.0)) == (0, 0, 1.0)
    assert uji_tanda(b(1.0), b(0.0))[2] == 1.0
