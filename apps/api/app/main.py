from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException, Query, Response
from zetalmanac_core.convert import convert, month_table

app = FastAPI(title="Zetalmanac API", version="0.0.1")

# Hasil konversi tidak pernah berubah untuk input yang sama.
# max-age: cache browser 1 jam; s-maxage: cache CDN Vercel 1 hari.
CACHE_CONTROL = "public, max-age=3600, s-maxage=86400"


@app.get("/v1/health")
def health() -> dict[str, str]:
    """Cek apakah API hidup. Dipakai oleh monitoring dan oleh kita saat debug."""
    return {"status": "ok", "service": "zetalmanac-api", "version": app.version}


@app.get("/v1/convert")
def convert_date(
    response: Response,
    calendar: Annotated[
        Literal["gregorian", "julian", "hijri", "china", "maya"], Query(alias="from")
    ],
    date: Annotated[str, Query(max_length=20)],
    scheme: Literal["I", "II", "III", "IV"] = "II",
    epoch: Literal["civil", "astronomical"] = "civil",
    correlation: int = 584283,  # 584283, 584285, atau 584286; nilai lain ditolak oleh core
    leap: bool = False,
    after_sunset: bool = False,
    steps: bool = False,
) -> dict:
    """Ubah satu tanggal ke semua kalender. steps=true menambahkan langkah hitung.

    Contoh: /v1/convert?from=gregorian&date=2026-11-05
    """
    try:
        hasil = convert(
            calendar,
            date,
            scheme=scheme,
            epoch=epoch,
            correlation=correlation,
            leap=leap,
            after_sunset=after_sunset,
            steps=steps,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    response.headers["Cache-Control"] = CACHE_CONTROL
    return hasil


@app.get("/v1/month")
def month_calendar(
    response: Response,
    year: Annotated[int, Query(ge=-9999, le=9999)],
    month: Annotated[int, Query(ge=1, le=12)],
    scheme: Literal["I", "II", "III", "IV"] = "II",
    epoch: Literal["civil", "astronomical"] = "civil",
) -> dict:
    """Satu bulan Gregorian, hari demi hari, dengan tanggal Hijriah urfi dan China.

    Contoh: /v1/month?year=2026&month=11
    """
    try:
        hasil = month_table(year, month, scheme=scheme, epoch=epoch)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    response.headers["Cache-Control"] = CACHE_CONTROL
    return hasil
