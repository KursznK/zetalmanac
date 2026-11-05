"""Kalender Julian (proleptik) <-> RD (Rata Die).

Tahun memakai penomoran astronomis, sama seperti modul gregorian:
tahun 0 = 1 SM, tahun -1 = 2 SM. Label "SM" diurus lapisan tampilan.
Algoritma mengikuti Reingold & Dershowitz (fixed-from-julian / julian-from-fixed,
kode CALENDRICA 4.0), disederhanakan karena kita memakai tahun 0.
Implementasi ditulis ulang sendiri.
"""

EPOCH = -1  # RD dari 1 Januari tahun 1 (Julian) = 30 Desember tahun 0 (Gregorian)

_DAYS_IN_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def is_leap_year(year: int) -> bool:
    """Tahun kabisat Julian: setiap tahun yang habis dibagi 4, tanpa pengecualian."""
    return year % 4 == 0


def days_in_month(year: int, month: int) -> int:
    """Jumlah hari dalam bulan tertentu."""
    if not 1 <= month <= 12:
        raise ValueError(f"Bulan harus 1–12, didapat {month}")
    if month == 2 and is_leap_year(year):
        return 29
    return _DAYS_IN_MONTH[month - 1]


def validate(year: int, month: int, day: int) -> None:
    """Tolak tanggal yang tidak ada, misalnya 30 Februari."""
    dim = days_in_month(year, month)
    if not 1 <= day <= dim:
        raise ValueError(
            f"Tanggal Julian {year}-{month:02d}-{day:02d} tidak ada (bulan ini {dim} hari)"
        )


def to_rd(year: int, month: int, day: int) -> int:
    """Julian -> RD."""
    validate(year, month, day)
    y = year - 1
    if month <= 2:
        correction = 0
    elif is_leap_year(year):
        correction = -1
    else:
        correction = -2
    return EPOCH - 1 + 365 * y + y // 4 + (367 * month - 362) // 12 + correction + day


def from_rd(rd: int) -> tuple[int, int, int]:
    """RD -> Julian (tahun, bulan, tanggal)."""
    year = (4 * (rd - EPOCH) + 1464) // 1461
    prior_days = rd - to_rd(year, 1, 1)
    if rd < to_rd(year, 3, 1):
        correction = 0
    elif is_leap_year(year):
        correction = 1
    else:
        correction = 2
    month = (12 * (prior_days + correction) + 373) // 367
    day = rd - to_rd(year, month, 1) + 1
    return (year, month, day)
