from zrag.chunking import bagian, chunk_document, potong


def test_bagian_mengikuti_judul_markdown_dan_wikipedia():
    teks = (
        "# Kalender Uji\n\nPembuka.\n\n== Sejarah ==\nIsi sejarah.\n\n=== Awal ===\nIsi awal.\n\n"
        "== Lihat pula ==\nTautan.\n\n## Aturan\nIsi aturan.\n"
    )
    hasil = [(" › ".join(j), isi) for j, isi in bagian(teks)]
    assert hasil == [
        ("Kalender Uji", "Pembuka."),
        ("Kalender Uji › Sejarah", "Isi sejarah."),
        ("Kalender Uji › Sejarah › Awal", "Isi awal."),
        ("Kalender Uji › Aturan", "Isi aturan."),  # "Lihat pula" dibuang
    ]


def test_potongan_tidak_melebihi_batas_dan_bertumpang_tindih():
    paragraf = " ".join(f"k{i}" for i in range(700))
    potongan = potong(paragraf, max_kata=300, tumpang=40)
    assert all(len(p.split()) <= 300 for p in potongan)
    assert (
        potongan[1].split()[0] == "k260"
    )  # mulai 40 kata sebelum akhir potongan pertama
    semua = {k for p in potongan for k in p.split()}
    assert semua == {f"k{i}" for i in range(700)}  # tidak ada kata yang hilang


def test_paragraf_pendek_digabung():
    assert potong("satu dua\n\ntiga empat", max_kata=10) == ["satu dua tiga empat"]


def test_id_potongan_unik_dan_berurutan():
    chunks = chunk_document("doc", "# A\n\nsatu\n\n== B ==\ndua\n")
    assert [c["id"] for c in chunks] == ["doc#0", "doc#1"]
    assert chunks[1]["section"] == "A › B"
