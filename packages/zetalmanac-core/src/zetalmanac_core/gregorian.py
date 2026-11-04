"""Kalender Gregorian (proleptik) <-> RD (Rata Die).

RD 1 = 1 Januari tahun 1 M (Gregorian proleptik).
Algoritma mengikuti Dershowitz & Reingold (1990), "Calendrical Calculations",
Software--Practice and Experience 20(9); implementasi ditulis ulang sendiri.
Penomoran tahun astronomis: tahun 0 = 1 SM, tahun -1 = 2 SM.
"""

EPOCH = 1  # RD dari 1 Januari tahun 1 (Gregorian)

_DAYS_IN_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def is_leap_year(year: int) -> bool:
    """Tahun kabisat Gregorian: habis dibagi 4, kecuali abad yang tidak habis dibagi 400."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


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
            f"Tanggal {year}-{month:02d}-{day:02d} tidak ada (bulan ini {dim} hari)"
        )


def to_rd(year: int, month: int, day: int) -> int:
    """Gregorian -> RD."""
    validate(year, month, day)
    y = year - 1
    if month <= 2:
        correction = 0
    elif is_leap_year(year):
        correction = -1
    else:
        correction = -2
    return (
        EPOCH
        - 1
        + 365 * y
        + y // 4
        - y // 100
        + y // 400
        + (367 * month - 362) // 12
        + correction
        + day
    )


def year_from_rd(rd: int) -> int:
    """Tahun Gregorian yang memuat hari RD tertentu."""
    d0 = rd - EPOCH
    n400, d1 = divmod(d0, 146097)  # siklus 400 tahun = 146.097 hari
    n100, d2 = divmod(d1, 36524)  # siklus 100 tahun = 36.524 hari
    n4, d3 = divmod(d2, 1461)  # siklus 4 tahun = 1.461 hari
    n1 = d3 // 365
    year = 400 * n400 + 100 * n100 + 4 * n4 + n1
    # Hari terakhir tahun kabisat di ujung siklus 4 atau 400 tahun
    return year if (n100 == 4 or n1 == 4) else year + 1


def from_rd(rd: int) -> tuple[int, int, int]:
    """RD -> Gregorian (tahun, bulan, tanggal)."""
    year = year_from_rd(rd)
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
