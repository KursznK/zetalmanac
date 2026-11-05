"""Kalender Hijriah hisab urfi (aritmetis/tabular) <-> RD.

Bulan ganjil 30 hari, bulan genap 29 hari; Zulhijah 30 hari di tahun kabisat.
Siklus 30 tahun = 10.631 hari dengan 11 tahun kabisat. Letak tahun kabisat
dalam siklus ditentukan skema (I–IV); hari pertama ditentukan epoch.
Skema II + epoch sipil sama dengan ICU "islamic-civil";
skema II + epoch astronomis sama dengan ICU "islamic-tbla".
Algoritma mengikuti Reingold & Dershowitz (fixed-from-islamic, CALENDRICA 4.0),
diperluas untuk empat skema. Implementasi ditulis ulang sendiri.

Catatan: fungsi di sini bekerja pada hari sipil (tengah malam ke tengah malam).
Hari Hijriah dimulai saat magrib, jadi untuk waktu setelah magrib pakai after_sunset=True.
"""

from zetalmanac_core import julian

MONTHS = (
    "Muharam",
    "Safar",
    "Rabiulawal",
    "Rabiulakhir",
    "Jumadilawal",
    "Jumadilakhir",
    "Rajab",
    "Syakban",
    "Ramadan",
    "Syawal",
    "Zulkaidah",
    "Zulhijah",
)

LEAP_YEARS = {
    "I": (2, 5, 7, 10, 13, 15, 18, 21, 24, 26, 29),
    "II": (2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29),
    "III": (2, 5, 8, 10, 13, 16, 19, 21, 24, 27, 29),
    "IV": (2, 5, 8, 11, 13, 16, 19, 21, 24, 27, 30),
}

EPOCHS = {
    "civil": julian.to_rd(622, 7, 16),  # Jumat, 16 Juli 622 (Julian) = RD 227015
    "astronomical": julian.to_rd(622, 7, 15),  # Kamis, 15 Juli 622 (Julian) = RD 227014
}

CYCLE_DAYS = 10631  # 30 x 354 + 11


def _check_scheme(scheme: str) -> None:
    if scheme not in LEAP_YEARS:
        raise ValueError(
            f"Skema harus salah satu dari {tuple(LEAP_YEARS)}, didapat {scheme!r}"
        )


def _check_epoch(epoch: str) -> None:
    if epoch not in EPOCHS:
        raise ValueError(
            f"Epoch harus salah satu dari {tuple(EPOCHS)}, didapat {epoch!r}"
        )


def is_leap_year(year: int, scheme: str = "II") -> bool:
    """Tahun kabisat (355 hari) menurut skema."""
    _check_scheme(scheme)
    return (year - 1) % 30 + 1 in LEAP_YEARS[scheme]


def days_in_month(year: int, month: int, scheme: str = "II") -> int:
    """Jumlah hari dalam bulan tertentu."""
    if not 1 <= month <= 12:
        raise ValueError(f"Bulan harus 1–12, didapat {month}")
    if month == 12 and is_leap_year(year, scheme):
        return 30
    return 30 if month % 2 == 1 else 29


def validate(year: int, month: int, day: int, scheme: str = "II") -> None:
    """Tolak tanggal yang tidak ada, misalnya 30 Safar."""
    dim = days_in_month(year, month, scheme)
    if not 1 <= day <= dim:
        raise ValueError(
            f"Tanggal Hijriah {year}-{month:02d}-{day:02d} tidak ada (bulan ini {dim} hari)"
        )


def _days_before_year(year: int, scheme: str) -> int:
    """Jumlah hari dari 1 Muharam tahun 1 sampai sebelum 1 Muharam tahun `year`."""
    cycles, years_in_cycle = divmod(year - 1, 30)
    leap_days = sum(1 for k in LEAP_YEARS[scheme] if k <= years_in_cycle)
    return cycles * CYCLE_DAYS + 354 * years_in_cycle + leap_days


def _days_before_month(month: int) -> int:
    """Jumlah hari sebelum tanggal 1 bulan `month` (30, 29, 30, 29, ...)."""
    return 29 * (month - 1) + month // 2


def to_rd(
    year: int, month: int, day: int, scheme: str = "II", epoch: str = "civil"
) -> int:
    """Hijriah urfi -> RD (hari sipil yang siangnya bertanggal ini)."""
    _check_epoch(epoch)
    validate(year, month, day, scheme)
    return (
        EPOCHS[epoch]
        - 1
        + _days_before_year(year, scheme)
        + _days_before_month(month)
        + day
    )


def from_rd(
    rd: int, scheme: str = "II", epoch: str = "civil", after_sunset: bool = False
) -> tuple[int, int, int]:
    """RD -> Hijriah urfi (tahun, bulan, tanggal).

    after_sunset=True: waktunya setelah magrib, sehingga sudah masuk tanggal Hijriah berikutnya.
    """
    _check_scheme(scheme)
    _check_epoch(epoch)
    if after_sunset:
        rd += 1
    cycles, rest = divmod(rd - EPOCHS[epoch], CYCLE_DAYS)
    year = 30 * cycles + 1
    while True:
        length = 355 if is_leap_year(year, scheme) else 354
        if rest < length:
            break
        rest -= length
        year += 1
    month = (11 * rest + 330) // 325
    day = rest - _days_before_month(month) + 1
    return (year, month, day)
