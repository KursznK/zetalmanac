from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_konversi_gregorian():
    r = client.get("/v1/convert", params={"from": "gregorian", "date": "2026-11-05"})
    assert r.status_code == 200
    body = r.json()
    assert body["rd"] == 739925
    assert body["hijri"]["label"] == "24 Jumadilawal 1448 H"
    assert body["china"]["label"] == "九月廿七"
    assert body["maya"]["long_count"] == "13.0.14.1.7"
    assert "s-maxage=86400" in r.headers["cache-control"]


def test_parameter_varian():
    r = client.get(
        "/v1/convert",
        params={
            "from": "gregorian",
            "date": "2026-11-05",
            "scheme": "III",
            "correlation": 584285,
        },
    )
    assert r.status_code == 200
    assert r.json()["hijri"]["label"] == "25 Jumadilawal 1448 H"
    assert r.json()["maya"]["long_count"] == "13.0.14.1.5"


def test_bulan_kabisat_china():
    r = client.get(
        "/v1/convert", params={"from": "china", "date": "2025-06-01", "leap": "true"}
    )
    assert r.status_code == 200
    assert r.json()["gregorian"]["label"] == "25 Juli 2025"


def test_tanggal_tidak_ada_422():
    r = client.get("/v1/convert", params={"from": "gregorian", "date": "2026-02-30"})
    assert r.status_code == 422
    assert "tidak ada" in r.json()["detail"]


def test_parameter_tidak_dikenal_422():
    for params in (
        {"from": "persia", "date": "1405-08-14"},
        {"from": "maya", "date": "13.0.0.0.0", "correlation": 584280},
        {"from": "hijri", "date": "1448-05-24", "scheme": "V"},
        {"from": "gregorian", "date": "1" * 100},
        {"date": "2026-11-05"},
    ):
        assert client.get("/v1/convert", params=params).status_code == 422, params
