from zrag.embed import (
    CloudflareBgeM3,
    GeminiEmbedding2,
    baca_env,
    baca_respons_cloudflare,
)
from zrag.embed_index import perbarui
from zrag.vectors import muat, sha256

CHUNK = {"id": "d#0", "section": "Judul › Bagian", "text": "Isi potongan."}


def test_baca_env(tmp_path):
    f = tmp_path / ".env"
    f.write_text('# komentar\n\nA=1\nB = "dua"\nRUSAK\nC=x=y\n', encoding="utf-8")
    assert baca_env(f) == {"A": "1", "B": "dua", "C": "x=y"}
    assert baca_env(tmp_path / "tidak-ada") == {}


def test_format_teks_per_model():
    assert CloudflareBgeM3.teks_dokumen(CHUNK) == "Judul › Bagian\nIsi potongan."
    assert CloudflareBgeM3.teks_kueri("halo") == "halo"
    assert GeminiEmbedding2.teks_dokumen(CHUNK) == (
        "title: Judul › Bagian | text: Isi potongan."
    )
    assert GeminiEmbedding2.teks_kueri("halo") == "task: search result | query: halo"


def test_badan_permintaan_gemini():
    body = GeminiEmbedding2.body(GeminiEmbedding2, ["a", "b"])
    assert body == {
        "requests": [
            {
                "model": "models/gemini-embedding-2",
                "content": {"parts": [{"text": "a"}]},
            },
            {
                "model": "models/gemini-embedding-2",
                "content": {"parts": [{"text": "b"}]},
            },
        ]
    }


def test_respons_cloudflare():
    ok = {"success": True, "result": {"shape": [1, 2], "data": [[0.1, 0.2]]}}
    assert baca_respons_cloudflare(ok) == [[0.1, 0.2]]
    try:
        baca_respons_cloudflare({"success": False, "errors": [{"message": "x"}]})
    except RuntimeError as e:
        assert "x" in str(e)
    else:
        raise AssertionError("seharusnya gagal")


class Palsu:
    nama = "palsu"
    ukuran_batch = 2
    jeda_antar_batch = 0.0

    def __init__(self):
        self.dikirim: list[str] = []

    def embed(self, teks):
        self.dikirim += teks
        return [[float(len(t)), 1.0] for t in teks]


def test_perbarui_hanya_mengirim_teks_baru(tmp_path):
    prefix = tmp_path / "v"
    e = Palsu()
    assert perbarui(prefix, e, [("a", "x"), ("b", "yy"), ("c", "zzz")]) == (3, 0)
    assert e.dikirim == ["x", "yy", "zzz"]

    e2 = Palsu()
    # "yy" berubah jadi "baru", "c" dihapus, "d" ditambah dengan teks sama dengan "a"
    assert perbarui(prefix, e2, [("a", "x"), ("b", "baru"), ("d", "x")]) == (1, 2)
    assert e2.dikirim == ["baru"]
    vs = muat(prefix)
    assert vs.ids == ["a", "b", "d"]
    assert vs.shas == [sha256("x"), sha256("baru"), sha256("x")]
