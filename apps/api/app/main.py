from fastapi import FastAPI

app = FastAPI(title="Zetalmanac API", version="0.0.1")


@app.get("/v1/health")
def health() -> dict[str, str]:
    """Cek apakah API hidup. Dipakai oleh monitoring dan oleh kita saat debug."""
    return {"status": "ok", "service": "zetalmanac-api", "version": app.version}
