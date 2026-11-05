from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_november_2026():
    r = client.get("/v1/month", params={"year": 2026, "month": 11})
    assert r.status_code == 200
    body = r.json()
    assert body["month_name"] == "November"
    assert len(body["days"]) == 30
    assert body["days"][4]["china"]["label"] == "廿七"
    assert "s-maxage=86400" in r.headers["cache-control"]


def test_parameter_tidak_valid_422():
    for params in (
        {"year": 2026, "month": 13},
        {"year": 10000, "month": 1},
        {"month": 1},
    ):
        assert client.get("/v1/month", params=params).status_code == 422, params
