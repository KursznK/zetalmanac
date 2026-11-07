from zrag.klaim import BERKAS, ekstrak, load, pecah_kalimat, periksa, rapikan


def test_pecah_kalimat_dan_daftar():
    teks = "Kalimat pertama yang cukup panjang [1]. Kalimat kedua juga panjang.\n1. Butir daftar yang panjang\n- ok"
    assert pecah_kalimat(teks) == [
        "Kalimat pertama yang cukup panjang [1].",
        "Kalimat kedua juga panjang.",
        "Butir daftar yang panjang",
    ]


def test_rapikan_spasi_khusus_dan_sitasi_kosong():
    assert rapikan("8 Februari 2027 (urfi)【】.") == "8 Februari 2027 (urfi)."
    assert rapikan("tetap [1]") == "tetap [1]"


def test_berkas_label_sesuai_hasil_run():
    """klaim.yaml dibuat dari eval/runs/; kalau run diulang, klaim (dan labelnya) harus dibuat ulang."""
    tersimpan = [(k["id"], k["klaim"], k["sitasi"]) for k in load()]
    assert tersimpan == [(k["id"], k["klaim"], k["sitasi"]) for k in ekstrak()]


def test_berkas_label_sah():
    klaim = load()
    assert len({k["id"] for k in klaim}) == len(klaim)
    assert periksa(klaim) == []
    for k in klaim:
        assert len(k["bukti"]) >= len(k["sitasi"]), k["id"]


def test_periksa_menangkap_isian_salah():
    k = {"id": "x", "label": "benar", "sitasi_tepat": "ya", "sitasi": []}
    assert len(periksa([k])) == 2
    assert BERKAS.name == "klaim.yaml"
