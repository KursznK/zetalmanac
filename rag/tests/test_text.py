from zrag.text import detect_lang, tokens


def test_stopword_dibuang_dan_huruf_kecil():
    assert "yang" not in tokens("Kalender yang dipakai", "id")
    assert all(t == t.lower() for t in tokens("The Julian Calendar", "en"))


def test_deteksi_bahasa_dari_stopword():
    assert detect_lang("kapan tahun baru yang berikutnya") == "id"
    assert detect_lang("when is the next new year") == "en"


def test_deteksi_bahasa_dari_kosakata_kalau_seri():
    kosakata = {"id": {"kalender", "kabisat"}, "en": {"calendar", "leap", "epoch"}}
    assert detect_lang("leap epoch", kosakata) == "en"
    assert detect_lang("kabisat", kosakata) == "id"
