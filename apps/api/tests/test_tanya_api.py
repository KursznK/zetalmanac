from fastapi.testclient import TestClient

from app import tanya as modul
from app.main import app

client = TestClient(app)
BODY = {"pertanyaan": "Kapan tahun kabisat hisab urfi?", "turnstile": "token"}


def pasang(monkeypatch, secret="rahasia", lolos=True, hasil=None):
    dipanggil = {}
    monkeypatch.setattr(modul, "secret_turnstile", lambda: secret)

    def verifikasi(token, secret, ip):
        dipanggil["verifikasi"] = (token, ip)
        return lolos

    def tanya(pertanyaan):
        dipanggil["tanya"] = pertanyaan
        return hasil or {"status": "dijawab", "jawaban": "Jawaban [1].", "sumber": []}

    monkeypatch.setattr(modul, "verifikasi_turnstile", verifikasi)
    monkeypatch.setattr(modul, "jalankan_tanya", tanya)
    return dipanggil


def test_tanpa_secret_503(monkeypatch):
    dipanggil = pasang(monkeypatch, secret=None)
    r = client.post("/v1/tanya", json=BODY)
    assert r.status_code == 503
    assert "tanya" not in dipanggil


def test_turnstile_gagal_403_dan_tidak_memanggil_llm(monkeypatch):
    dipanggil = pasang(monkeypatch, lolos=False)
    r = client.post(
        "/v1/tanya", json=BODY, headers={"x-forwarded-for": "203.0.113.7, 10.0.0.1"}
    )
    assert r.status_code == 403
    assert dipanggil["verifikasi"] == ("token", "203.0.113.7")
    assert "tanya" not in dipanggil


def test_berhasil_tanpa_cache_dan_tanpa_field_internal(monkeypatch):
    pasang(
        monkeypatch,
        hasil={
            "status": "ditolak_keluaran",
            "pesan": "Ditolak.",
            "teks_mentah": "rahasia",
        },
    )
    r = client.post("/v1/tanya", json=BODY)
    assert r.status_code == 200
    assert r.headers["cache-control"] == "no-store"
    assert r.json() == {"status": "ditolak_keluaran", "pesan": "Ditolak."}


def test_body_tidak_valid_422(monkeypatch):
    pasang(monkeypatch)
    assert client.post("/v1/tanya", json={"pertanyaan": "x"}).status_code == 422
    assert client.post("/v1/tanya", json={**BODY, "turnstile": ""}).status_code == 422
    assert (
        client.post("/v1/tanya", json={**BODY, "pertanyaan": "a" * 2001}).status_code
        == 422
    )


def test_get_tidak_diizinkan():
    assert client.get("/v1/tanya").status_code == 405


def test_indeks_zrag_menunjuk_folder_data_api():
    import os
    from pathlib import Path

    folder = Path(os.environ["ZRAG_INDEX_DIR"])
    assert folder.parts[-3:] == ("api", "data", "index")
    assert (folder / "chunks.jsonl").exists()
    assert (folder / "vectors-bge-m3.f16").exists()
