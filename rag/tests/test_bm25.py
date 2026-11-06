from zrag.bm25 import BM25

CHUNKS = [
    {"id": "a", "section": "Bulan", "text": "Bulan sinodis rata-rata 29,53 hari."},
    {
        "id": "b",
        "section": "Kabisat",
        "text": "Tahun kabisat Hijriah urfi: 11 dalam siklus 30 tahun.",
    },
    {
        "id": "c",
        "section": "Maya",
        "text": "Hitungan Panjang memakai baktun dan katun.",
    },
]


def test_dokumen_paling_relevan_di_atas():
    hasil = BM25(CHUNKS, "id").search("siklus kabisat urfi", k=3)
    assert hasil[0][0]["id"] == "b"


def test_kueri_tanpa_kata_cocok_kosong():
    assert BM25(CHUNKS, "id").search("zzzz") == []


def test_idf_kata_langka_lebih_tinggi():
    idx = BM25(CHUNKS + [{"id": "d", "section": "", "text": "tahun tahun tahun"}], "id")
    assert idx.idf["baktun"] > idx.idf["tahun"]
