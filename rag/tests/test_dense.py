import pytest

from zrag import dense
from zrag.dense import cari, kueri_eval, rrf, tersedia, usang, vektor_kueri_eval
from zrag.embed import EMBEDDERS
from zrag.evaluate import load_dataset
from zrag.search import load_chunks
from zrag.vectors import sha256

A, B, C = ({"id": i} for i in ("a", "b", "c"))


def test_rrf_menaikkan_yang_tinggi_di_kedua_daftar():
    # b peringkat 2 dan 1; a peringkat 1 dan tidak ada; c peringkat 3 dan 2
    hasil = rrf([[A, B, C], [B, C]])
    assert [c["id"] for c in hasil] == ["b", "c", "a"]


def test_rrf_rumus():
    hasil = rrf([[A], [B, A]], k=60)
    # a: 1/61 + 1/62, b: 1/61 → a di atas
    assert [c["id"] for c in hasil] == ["a", "b"]


def test_cari_mengurutkan_dengan_cosine(monkeypatch):
    chunks = [{"id": "x"}, {"id": "y"}, {"id": "z"}]
    rows = [[1.0, 0.0], [0.0, 1.0], [0.6, 0.8]]
    monkeypatch.setattr(dense, "indeks", lambda nama: (chunks, rows))
    hasil = cari("uji", [0.0, 1.0], 2)
    assert [c["id"] for c, _ in hasil] == ["y", "z"]
    assert hasil[0][1] == pytest.approx(1.0)


@pytest.mark.parametrize("nama", list(EMBEDDERS))
def test_vektor_tersimpan_tidak_usang(nama):
    """Kalau korpus atau kueri berubah, vektor harus dibuat ulang (zrag.embed_index)."""
    if not tersedia(nama):
        pytest.skip(f"vektor {nama} belum dibuat")
    assert usang(nama, load_chunks()) == []
    tabel = vektor_kueri_eval(nama)
    for q in load_dataset():
        assert sha256(EMBEDDERS[nama].teks_kueri(q["query"])) in tabel, q["id"]
        assert len(kueri_eval(nama, q["query"])) == len(next(iter(tabel.values())))


def test_vektor_produksi_ada_di_api():
    assert dense.lokasi_chunks(dense.PRODUKSI).parent.name == "index"
    assert dense.lokasi_chunks("gemini-embedding-2").parent.name == "vectors"
