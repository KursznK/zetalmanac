"""Membuat tabel bulan baru dan zhongqi untuk kalender China (data/china_astro.json).

Momen disimpan dalam UTC; aturan zona waktu (UTC+8, atau waktu lokal Beijing sebelum 1929)
diterapkan oleh china.py. Rentang data: November 1899 sampai Maret 2102, cukup untuk
mengonversi tanggal 1900–2100.

Jalankan dari packages/zetalmanac-core (butuh internet sekali untuk efemeris):
    uv run --group ephem python scripts/gen_china_astro.py
"""

import json
from pathlib import Path

import skyfield
from skyfield import almanac
from skyfield.api import Loader
from skyfield.framelib import ecliptic_frame

DATA_DIR = Path.home() / ".skyfield-data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
load = Loader(str(DATA_DIR))
ts = load.timescale()
eph = load("de440s.bsp")
earth, sun = eph["earth"], eph["sun"]

OUT = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "zetalmanac_core"
    / "data"
    / "china_astro.json"
)
FMT = "%Y-%m-%dT%H:%M:%S"

t0 = ts.utc(1899, 11, 1)
t1 = ts.utc(2102, 3, 1)


def zhongqi_index(t):
    """0–11: bujur ekliptika semu Matahari (ekuinoks tanggal itu) dibagi 30°."""
    _, lon, _ = earth.at(t).observe(sun).apparent().frame_latlon(ecliptic_frame)
    return (lon.degrees // 30).astype(int)


zhongqi_index.step_days = 14  # zhongqi berjarak ~30 hari

times, phases = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
new_moons = [t.utc_strftime(FMT) for t, p in zip(times, phases) if p == 0]

times, indices = almanac.find_discrete(t0, t1, zhongqi_index)
zhongqi = [[t.utc_strftime(FMT), int(i) * 30] for t, i in zip(times, indices)]

meta = {
    "sumber": "Skyfield + JPL DE440s; bulan baru = konjungsi bujur ekliptika semu; "
    "zhongqi = bujur ekliptika semu Matahari kelipatan 30 derajat (ekuinoks tanggal itu)",
    "skyfield": skyfield.__version__,
    "waktu": "UTC",
}

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8") as f:
    f.write("{\n")
    for key, value in meta.items():
        f.write(f"  {json.dumps(key)}: {json.dumps(value, ensure_ascii=False)},\n")
    f.write(
        '  "new_moons": [\n'
        + ",\n".join(f"    {json.dumps(t)}" for t in new_moons)
        + "\n  ],\n"
    )
    f.write(
        '  "zhongqi": [\n'
        + ",\n".join(f"    {json.dumps(z)}" for z in zhongqi)
        + "\n  ]\n}\n"
    )

print(f"{len(new_moons)} bulan baru, {len(zhongqi)} zhongqi -> {OUT}")
