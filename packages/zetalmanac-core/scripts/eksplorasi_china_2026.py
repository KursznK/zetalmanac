"""Eksplorasi Sesi 2.1: bulan baru dan 24 jieqi tahun 2026 (waktu Beijing),
dibandingkan dengan tabel Hong Kong Observatory 2026.

Jalankan dari packages/zetalmanac-core:
    uv run --group ephem python scripts/eksplorasi_china_2026.py
Efemeris DE440s (~31 MB) diunduh sekali ke ~/.skyfield-data.
"""

from datetime import timedelta
from pathlib import Path

from skyfield import almanac
from skyfield.api import Loader
from skyfield.framelib import ecliptic_frame

DATA_DIR = Path.home() / ".skyfield-data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
load = Loader(str(DATA_DIR))
ts = load.timescale()
eph = load("de440s.bsp")
earth, sun = eph["earth"], eph["sun"]

BEIJING = timedelta(hours=8)

# 24 jieqi, indeks = floor(bujur ekliptika Matahari / 15°); indeks genap = zhongqi
JIEQI = (
    "春分",
    "清明",
    "谷雨",
    "立夏",
    "小满",
    "芒种",
    "夏至",
    "小暑",
    "大暑",
    "立秋",
    "处暑",
    "白露",
    "秋分",
    "寒露",
    "霜降",
    "立冬",
    "小雪",
    "大雪",
    "冬至",
    "小寒",
    "大寒",
    "立春",
    "雨水",
    "惊蛰",
)

# Tanggal dari tabel HKO 2026 (hko.gov.hk, T2026e.txt)
HKO_BULAN_BARU = [
    "2026-01-19",
    "2026-02-17",
    "2026-03-19",
    "2026-04-17",
    "2026-05-17",
    "2026-06-15",
    "2026-07-14",
    "2026-08-13",
    "2026-09-11",
    "2026-10-10",
    "2026-11-09",
    "2026-12-09",
]
HKO_JIEQI = {
    "小寒": "2026-01-05",
    "大寒": "2026-01-20",
    "立春": "2026-02-04",
    "雨水": "2026-02-18",
    "惊蛰": "2026-03-05",
    "春分": "2026-03-20",
    "清明": "2026-04-05",
    "谷雨": "2026-04-20",
    "立夏": "2026-05-05",
    "小满": "2026-05-21",
    "芒种": "2026-06-05",
    "夏至": "2026-06-21",
    "小暑": "2026-07-07",
    "大暑": "2026-07-23",
    "立秋": "2026-08-07",
    "处暑": "2026-08-23",
    "白露": "2026-09-07",
    "秋分": "2026-09-23",
    "寒露": "2026-10-08",
    "霜降": "2026-10-23",
    "立冬": "2026-11-07",
    "小雪": "2026-11-22",
    "大雪": "2026-12-07",
    "冬至": "2026-12-22",
}

# Rentang: 1 Jan 2026 00.00 sampai 1 Jan 2027 00.00 waktu Beijing (= 16.00 UTC hari sebelumnya)
t0 = ts.utc(2025, 12, 31, 16)
t1 = ts.utc(2026, 12, 31, 16)


def beijing(t):
    """Waktu Skyfield -> datetime waktu Beijing (UTC+8)."""
    return t.utc_datetime() + BEIJING


def indeks_jieqi(t):
    """Indeks jieqi (0–23) dari bujur ekliptika semu Matahari (ekuinoks tanggal itu)."""
    _, lon, _ = earth.at(t).observe(sun).apparent().frame_latlon(ecliptic_frame)
    return (lon.degrees // 15).astype(int)


indeks_jieqi.step_days = 7  # jieqi berjarak ~15 hari, jadi cek tiap 7 hari aman

cocok = 0
total = 0

print("BULAN BARU (waktu Beijing)")
times, phases = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
bulan_baru = [beijing(t) for t, p in zip(times, phases) if p == 0]
for dt, hko in zip(bulan_baru, HKO_BULAN_BARU):
    ok = dt.strftime("%Y-%m-%d") == hko
    cocok += ok
    total += 1
    print(f"  {dt:%Y-%m-%d %H:%M}   HKO {hko}   {'✓' if ok else '✗'}")

print("\nJIEQI (waktu Beijing; * = zhongqi)")
times, indices = almanac.find_discrete(t0, t1, indeks_jieqi)
for t, i in zip(times, indices):
    nama = JIEQI[i]
    dt = beijing(t)
    hko = HKO_JIEQI[nama]
    ok = dt.strftime("%Y-%m-%d") == hko
    cocok += ok
    total += 1
    tanda = "*" if i % 2 == 0 else " "
    print(f"  {tanda} {nama}  {dt:%Y-%m-%d %H:%M}   HKO {hko}   {'✓' if ok else '✗'}")

print(f"\nCocok dengan HKO: {cocok}/{total}")
