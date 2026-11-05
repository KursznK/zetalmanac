"""Kalender China (农历, aturan pasca-1645) <-> RD.

Aturan:
1. Hari dimulai tengah malam waktu Beijing (UTC+8 sejak 1929; sebelumnya waktu lokal
   Beijing, bujur 116°25' T = UTC+7:45:40).
2. Bulan dimulai pada hari terjadinya bulan baru.
3. Titik balik musim dingin (冬至, bujur Matahari 270°) selalu berada di bulan 11.
4. Kalau dari bulan 11 ke bulan 11 berikutnya ada 13 bulan, bulan pertama yang tidak
   memuat zhongqi (bujur Matahari kelipatan 30°) menjadi bulan kabisat.

Momen bulan baru dan zhongqi tidak dihitung di sini. Keduanya dibaca dari tabel
data/china_astro.json yang dibuat oleh scripts/gen_china_astro.py (Skyfield + DE440s).
"""

import json
from bisect import bisect_right
from functools import lru_cache
from importlib.resources import files
from math import floor

from zetalmanac_core import gregorian

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
SHIO = (
    "Tikus",
    "Kerbau",
    "Macan",
    "Kelinci",
    "Naga",
    "Ular",
    "Kuda",
    "Kambing",
    "Monyet",
    "Ayam",
    "Anjing",
    "Babi",
)
ELEMEN = (
    "Kayu",
    "Kayu",
    "Api",
    "Api",
    "Tanah",
    "Tanah",
    "Logam",
    "Logam",
    "Air",
    "Air",
)

RD_1929 = gregorian.to_rd(1929, 1, 1)
OFFSET_SEBELUM_1929 = (7 + 45 / 60 + 40 / 3600) / 24  # dalam hari
OFFSET_SEJAK_1929 = 8 / 24


def beijing_day(utc_moment: float) -> int:
    """Momen UTC (RD pecahan) -> hari (RD) menurut waktu Beijing."""
    offset = OFFSET_SEJAK_1929 if utc_moment >= RD_1929 else OFFSET_SEBELUM_1929
    return floor(utc_moment + offset)


def moment_from_iso(text: str) -> float:
    """'2026-10-10T15:50:12' (UTC) -> RD pecahan."""
    tanggal, jam = text.split("T")
    y, m, d = (int(x) for x in tanggal.split("-"))
    hh, mm, ss = (int(x) for x in jam.split(":"))
    return gregorian.to_rd(y, m, d) + (hh * 3600 + mm * 60 + ss) / 86400


class ChineseCalendar:
    """Aturan kalender di atas daftar hari bulan baru dan hari zhongqi (waktu Beijing)."""

    def __init__(self, new_moon_days: list[int], zhongqi: list[tuple[int, int]]):
        # zhongqi: pasangan (hari, bujur Matahari dalam derajat: 0, 30, ..., 330)
        self.new_moons = sorted(new_moon_days)
        self.zhongqi_days = sorted(day for day, _ in zhongqi)
        self.solstices = sorted(day for day, lon in zhongqi if lon == 270)

    # ---- pencarian di tabel ----
    def _new_moon_on_or_before(self, day: int) -> int:
        i = bisect_right(self.new_moons, day) - 1
        if i < 0 or i + 1 >= len(self.new_moons):
            raise ValueError(f"RD {day} di luar rentang data kalender China")
        return self.new_moons[i]

    def _next_new_moon(self, day: int) -> int:
        i = bisect_right(self.new_moons, day)
        if i >= len(self.new_moons):
            raise ValueError(f"RD {day} di luar rentang data kalender China")
        return self.new_moons[i]

    def _solstice_on_or_before(self, day: int) -> int:
        i = bisect_right(self.solstices, day) - 1
        if i < 0:
            raise ValueError(f"RD {day} di luar rentang data kalender China")
        return self.solstices[i]

    def _has_zhongqi(self, start: int, end: int) -> bool:
        """Apakah ada zhongqi pada hari start <= hari < end."""
        i = bisect_right(self.zhongqi_days, start - 1)
        return i < len(self.zhongqi_days) and self.zhongqi_days[i] < end

    def _month11_start(self, day: int) -> int:
        """Hari pertama bulan 11 yang memuat 冬至 terakhir pada atau sebelum `day`."""
        return self._new_moon_on_or_before(self._solstice_on_or_before(day))

    # ---- satu "sui": dari bulan 11 sampai sebelum bulan 11 berikutnya ----
    def _sui(self, m11: int) -> tuple[list[tuple[int, int, bool]], int]:
        """Daftar (hari pertama, nomor bulan, kabisat?) dan hari pertama bulan 11 berikutnya."""
        i = bisect_right(
            self.solstices, m11 - 1
        )  # 冬至 pertama pada/setelah m11 (ada di bulan 11 ini)
        if i + 1 >= len(self.solstices):
            raise ValueError(f"RD {m11} di luar rentang data kalender China")
        next_m11 = self._new_moon_on_or_before(self.solstices[i + 1])
        starts = [m11]
        while starts[-1] < next_m11:
            starts.append(self._next_new_moon(starts[-1]))
        starts.pop()  # buang next_m11
        leap_year = len(starts) == 13

        months = []
        number = 11
        leap_found = False
        for k, start in enumerate(starts):
            if k == 0:
                months.append((start, 11, False))
                continue
            end = starts[k + 1] if k + 1 < len(starts) else next_m11
            if leap_year and not leap_found and not self._has_zhongqi(start, end):
                leap_found = True
                months.append((start, number, True))
            else:
                number = number % 12 + 1
                months.append((start, number, False))
        return months, next_m11

    # ---- konversi ----
    def from_rd(self, rd: int) -> tuple[int, int, bool, int]:
        """RD -> (tahun, bulan, kabisat?, tanggal). Tahun = tahun Gregorian saat Imlek-nya."""
        m11 = self._month11_start(rd)
        months, next_m11 = self._sui(m11)
        if rd >= next_m11:  # sudah masuk bulan 11 berikutnya, sebelum 冬至-nya
            months, _ = self._sui(next_m11)
        start, number, leap = [m for m in months if m[0] <= rd][-1]
        g_year, g_month, _ = gregorian.from_rd(rd)
        year = g_year - 1 if (number >= 11 and g_month <= 2) else g_year
        return (year, number, leap, rd - start + 1)

    def to_rd(self, year: int, month: int, leap: bool, day: int) -> int:
        """(tahun, bulan, kabisat?, tanggal) -> RD."""
        if not 1 <= month <= 12:
            raise ValueError(f"Bulan harus 1–12, didapat {month}")
        # Bulan 1–10 ada di sui yang dimulai bulan 11 tahun sebelumnya; bulan 11–12 di sui tahun itu
        sui_year = year - 1 if month <= 10 else year
        m11 = self._month11_start(gregorian.to_rd(sui_year, 12, 31))
        months, next_m11 = self._sui(m11)
        for k, (start, number, is_leap) in enumerate(months):
            if number == month and is_leap == leap:
                end = months[k + 1][0] if k + 1 < len(months) else next_m11
                if not 1 <= day <= end - start:
                    raise ValueError(
                        f"Bulan ini hanya {end - start} hari, didapat tanggal {day}"
                    )
                return start + day - 1
        raise ValueError(
            f"Tahun {year} tidak punya bulan {month}{' kabisat' if leap else ''}"
        )


def year_ganzhi(year: int) -> str:
    """Tahun -> nama ganzhi, misalnya 2026 -> 丙午."""
    i = (year - 4) % 60
    return STEMS[i % 10] + BRANCHES[i % 12]


def year_label(year: int) -> str:
    """Tahun -> label Indonesia, misalnya 2026 -> 'Kuda Api'."""
    i = (year - 4) % 60
    return f"{SHIO[i % 12]} {ELEMEN[i % 10]}"


def day_ganzhi(rd: int) -> str:
    """RD -> ganzhi hari, misalnya 5 Nov 2026 -> 癸未."""
    i = (rd + 1721425 - 11) % 60  # dari JDN; JDN 11 = 甲子
    return STEMS[i % 10] + BRANCHES[i % 12]


@lru_cache(maxsize=1)
def default_calendar() -> ChineseCalendar:
    """Kalender dari tabel data/china_astro.json (dibaca sekali)."""
    raw = json.loads(
        files("zetalmanac_core").joinpath("data", "china_astro.json").read_text("utf-8")
    )
    new_moons = [beijing_day(moment_from_iso(t)) for t in raw["new_moons"]]
    zhongqi = [(beijing_day(moment_from_iso(t)), lon) for t, lon in raw["zhongqi"]]
    return ChineseCalendar(new_moons, zhongqi)


def from_rd(rd: int) -> tuple[int, int, bool, int]:
    return default_calendar().from_rd(rd)


def to_rd(year: int, month: int, leap: bool, day: int) -> int:
    return default_calendar().to_rd(year, month, leap, day)
