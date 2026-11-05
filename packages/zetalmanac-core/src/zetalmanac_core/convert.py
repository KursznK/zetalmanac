"""Satu pintu untuk konversi: teks tanggal dari satu kalender -> semua kalender.

Dipakai oleh API (apps/api) supaya lapisan web tetap tipis dan semua logika teruji di sini.
"""

import re

from zetalmanac_core import china, gregorian, hijri_urfi, jd, julian, maya
from zetalmanac_core.steps import gregorian_steps, hijri_steps, maya_steps

CALENDARS = ("gregorian", "julian", "hijri", "china", "maya")

MIN_RD = gregorian.to_rd(-9999, 1, 1)
MAX_RD = gregorian.to_rd(9999, 12, 31)
CHINA_MIN_RD = gregorian.to_rd(1901, 1, 1)
CHINA_MAX_RD = gregorian.to_rd(2100, 12, 31)

HARI = ("Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu")
BULAN = (
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
)
CN_BULAN = (
    "正月",
    "二月",
    "三月",
    "四月",
    "五月",
    "六月",
    "七月",
    "八月",
    "九月",
    "十月",
    "十一月",
    "十二月",
)
CN_HARI = (
    "",
    "初一",
    "初二",
    "初三",
    "初四",
    "初五",
    "初六",
    "初七",
    "初八",
    "初九",
    "初十",
    "十一",
    "十二",
    "十三",
    "十四",
    "十五",
    "十六",
    "十七",
    "十八",
    "十九",
    "二十",
    "廿一",
    "廿二",
    "廿三",
    "廿四",
    "廿五",
    "廿六",
    "廿七",
    "廿八",
    "廿九",
    "三十",
)

_YMD = re.compile(r"^(-?\d{1,5})-(\d{1,2})-(\d{1,2})$")
_LONG_COUNT = re.compile(r"^(-?\d{1,3})\.(\d{1,2})\.(\d{1,2})\.(\d{1,2})\.(\d{1,2})$")


def _ymd(text: str) -> tuple[int, int, int]:
    match = _YMD.match(text.strip())
    if not match:
        raise ValueError(
            f"Format tanggal harus TAHUN-BULAN-TANGGAL, misalnya 2026-11-05; didapat {text!r}"
        )
    return tuple(int(x) for x in match.groups())


def _tahun(year: int) -> str:
    """Tahun astronomis -> label: 2026 -> '2026', 0 -> '1 SM', -43 -> '44 SM'."""
    return str(year) if year > 0 else f"{1 - year} SM"


def to_rd(
    calendar: str,
    text: str,
    *,
    scheme="II",
    epoch="civil",
    correlation=maya.GMT,
    leap=False,
) -> int:
    """Teks tanggal dalam `calendar` -> RD."""
    if calendar == "gregorian":
        rd = gregorian.to_rd(*_ymd(text))
    elif calendar == "julian":
        rd = julian.to_rd(*_ymd(text))
    elif calendar == "hijri":
        rd = hijri_urfi.to_rd(*_ymd(text), scheme=scheme, epoch=epoch)
    elif calendar == "china":
        y, m, d = _ymd(text)
        rd = china.to_rd(y, m, leap, d)
    elif calendar == "maya":
        match = _LONG_COUNT.match(text.strip())
        if not match:
            raise ValueError(
                f"Format Hitungan Panjang harus b.k.t.w.k, misalnya 13.0.14.1.7; didapat {text!r}"
            )
        rd = maya.rd_from_long_count(
            *(int(x) for x in match.groups()), correlation=correlation
        )
    else:
        raise ValueError(
            f"Kalender harus salah satu dari {CALENDARS}, didapat {calendar!r}"
        )
    if not MIN_RD <= rd <= MAX_RD:
        raise ValueError(
            "Tanggal di luar rentang yang didukung (tahun 10000 SM sampai 9999 M)"
        )
    return rd


def describe(
    rd: int, *, scheme="II", epoch="civil", correlation=maya.GMT, after_sunset=False
) -> dict:
    """RD -> tanggal di semua kalender, siap dikirim sebagai JSON."""
    gy, gm, gd = gregorian.from_rd(rd)
    jy, jm, jdd = julian.from_rd(rd)
    hy, hm, hd = hijri_urfi.from_rd(rd, scheme, epoch, after_sunset)
    lc = maya.long_count_from_rd(rd, correlation)
    tz_num, tz_name = maya.tzolkin_from_rd(rd, correlation)
    hb_month, hb_day = maya.haab_from_rd(rd, correlation)

    hasil = {
        "rd": rd,
        "jdn": jd.jdn_from_rd(rd),
        "hari": HARI[rd % 7],
        "gregorian": {
            "year": gy,
            "month": gm,
            "day": gd,
            "label": f"{gd} {BULAN[gm - 1]} {_tahun(gy)}",
        },
        "julian": {
            "year": jy,
            "month": jm,
            "day": jdd,
            "label": f"{jdd} {BULAN[jm - 1]} {_tahun(jy)}",
        },
        "hijri": {
            "year": hy,
            "month": hm,
            "day": hd,
            "scheme": scheme,
            "epoch": epoch,
            "after_sunset": after_sunset,
            "label": f"{hd} {hijri_urfi.MONTHS[hm - 1]} {hy} H",
        },
        "maya": {
            "long_count": ".".join(str(x) for x in lc),
            "correlation": correlation,
            "tzolkin": f"{tz_num} {maya.TZOLKIN_NAMES[tz_name - 1]}",
            "haab": f"{hb_day} {maya.HAAB_MONTHS[hb_month - 1]}",
            "lord_of_night": f"G{maya.lord_of_night_from_rd(rd, correlation)}",
        },
    }
    if CHINA_MIN_RD <= rd <= CHINA_MAX_RD:
        cy, cm, leap, cd = china.from_rd(rd)
        hasil["china"] = {
            "year": cy,
            "month": cm,
            "leap": leap,
            "day": cd,
            "year_ganzhi": china.year_ganzhi(cy),
            "year_label": china.year_label(cy),
            "day_ganzhi": china.day_ganzhi(rd),
            "label": f"{'闰' if leap else ''}{CN_BULAN[cm - 1]}{CN_HARI[cd]}",
        }
    else:
        hasil["china"] = None  # di luar rentang data 1901–2100
    return hasil


def convert(
    calendar: str,
    text: str,
    *,
    scheme="II",
    epoch="civil",
    correlation=maya.GMT,
    leap=False,
    after_sunset=False,
    steps=False,
) -> dict:
    """Teks tanggal dalam `calendar` -> tanggal di semua kalender.

    after_sunset hanya berlaku kalau input bukan Hijriah: tanggal Hijriah yang diketik
    sudah menunjuk harinya sendiri. steps=True menambahkan langkah hitung.
    """
    if calendar == "hijri":
        after_sunset = False
    rd = to_rd(
        calendar, text, scheme=scheme, epoch=epoch, correlation=correlation, leap=leap
    )
    hasil = describe(
        rd,
        scheme=scheme,
        epoch=epoch,
        correlation=correlation,
        after_sunset=after_sunset,
    )
    if steps:
        langkah = {
            "hijri": hijri_steps(rd, scheme, epoch, after_sunset),
            "maya": maya_steps(rd, correlation),
        }
        if calendar == "gregorian":
            g = hasil["gregorian"]
            langkah["gregorian"] = gregorian_steps(g["year"], g["month"], g["day"])
        hasil["steps"] = langkah
    return hasil


ZHONGQI = {
    0: "春分",
    30: "谷雨",
    60: "小满",
    90: "夏至",
    120: "大暑",
    150: "处暑",
    180: "秋分",
    210: "霜降",
    240: "小雪",
    270: "冬至",
    300: "大寒",
    330: "雨水",
}


def month_table(year: int, month: int, *, scheme="II", epoch="civil") -> dict:
    """Satu bulan Gregorian, hari demi hari, dengan tanggal Hijriah urfi dan China."""
    first = gregorian.to_rd(year, month, 1)
    if not MIN_RD <= first <= MAX_RD:
        raise ValueError("Tahun di luar rentang yang didukung (10000 SM sampai 9999 M)")
    cal = china.default_calendar()
    days = []
    for day in range(1, gregorian.days_in_month(year, month) + 1):
        rd = first + day - 1
        hy, hm, hd = hijri_urfi.from_rd(rd, scheme, epoch)
        entry = {
            "day": day,
            "rd": rd,
            "weekday": rd % 7,  # 0 = Minggu
            "hijri": {
                "year": hy,
                "month": hm,
                "day": hd,
                "month_name": hijri_urfi.MONTHS[hm - 1],
            },
            "china": None,
        }
        if CHINA_MIN_RD <= rd <= CHINA_MAX_RD:
            cy, cm, leap, cd = cal.from_rd(rd)
            lon = cal.zhongqi_by_day.get(rd)
            entry["china"] = {
                "year": cy,
                "month": cm,
                "leap": leap,
                "day": cd,
                "label": f"{'闰' if leap else ''}{CN_BULAN[cm - 1]}"
                if cd == 1
                else CN_HARI[cd],
                "zhongqi": ZHONGQI[lon] if lon is not None else None,
            }
        days.append(entry)
    return {
        "year": year,
        "month": month,
        "month_name": BULAN[month - 1],
        "scheme": scheme,
        "epoch": epoch,
        "days": days,
    }


def _label_masehi(rd: int) -> str:
    y, m, d = gregorian.from_rd(rd)
    return f"{HARI[rd % 7]}, {d} {BULAN[m - 1]} {_tahun(y)}"


def upcoming(rd: int, *, scheme="II", epoch="civil") -> list[dict]:
    """Hari-hari penting berikutnya (termasuk hari ini), diurutkan dari yang terdekat."""
    if not MIN_RD <= rd <= MAX_RD:
        raise ValueError(
            "Tanggal di luar rentang yang didukung (tahun 10000 SM sampai 9999 M)"
        )
    acara = []

    hy, _, _ = hijri_urfi.from_rd(rd, scheme, epoch)
    for bulan_h, nama in ((1, "1 Muharam"), (9, "1 Ramadan"), (10, "1 Syawal")):
        target = hijri_urfi.to_rd(hy, bulan_h, 1, scheme, epoch)
        tahun_h = hy
        if target < rd:
            tahun_h = hy + 1
            target = hijri_urfi.to_rd(tahun_h, bulan_h, 1, scheme, epoch)
        acara.append(
            {"nama": f"{nama} {tahun_h} H (urfi)", "kalender": "hijri", "rd": target}
        )

    if CHINA_MIN_RD <= rd <= CHINA_MAX_RD:
        cy, _, _, _ = china.from_rd(rd)
        try:
            target = china.to_rd(cy, 1, False, 1)
            tahun_c = cy
            if target < rd:
                tahun_c = cy + 1
                target = china.to_rd(tahun_c, 1, False, 1)
            if target <= CHINA_MAX_RD:
                label = f"Imlek {tahun_c} · {china.year_ganzhi(tahun_c)} ({china.year_label(tahun_c)})"
                acara.append({"nama": label, "kalender": "china", "rd": target})
        except ValueError:
            pass  # Imlek berikutnya di luar rentang data

    for item in acara:
        item["hari_lagi"] = item["rd"] - rd
        item["label"] = _label_masehi(item["rd"])
    return sorted(acara, key=lambda item: item["rd"])
