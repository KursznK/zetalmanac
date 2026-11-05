from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hari_penting_berikutnya():
    r = client.get("/v1/upcoming", params={"date": "2026-11-05"})
    assert r.status_code == 200
    acara = r.json()
    assert acara[0]["nama"].startswith("Imlek 2027")
    assert acara[0]["hari_lagi"] == 93
    assert "s-maxage=86400" in r.headers["cache-control"]


def test_tanggal_tidak_valid_422():
    for params in ({"date": "2026-02-30"}, {"date": "kemarin"}, {}):
        assert client.get("/v1/upcoming", params=params).status_code == 422, params
