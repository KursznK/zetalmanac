"""Kalender Maya: Hitungan Panjang, Haab', Tzolk'in, dan Penguasa Malam <-> RD.

Hari ke-0 Hitungan Panjang (0.0.0.0.0, 4 Ajaw 8 Kumk'u) ditentukan oleh konstanta
korelasi, yaitu JDN dari hari itu. Bawaan: GMT 584283.
Algoritma mengikuti Reingold & Dershowitz (CALENDRICA 4.0) dan
Reingold, Dershowitz & Clamen (1993). Implementasi ditulis ulang sendiri.
"""

from zetalmanac_core.jd import JDN_OFFSET

GMT = 584283
CORRELATIONS = (584283, 584285, 584286)

TZOLKIN_NAMES = (
    "Imix",
    "Ik'",
    "Ak'b'al",
    "K'an",
    "Chikchan",
    "Kimi",
    "Manik'",
    "Lamat",
    "Muluk",
    "Ok",
    "Chuwen",
    "Eb'",
    "B'en",
    "Ix",
    "Men",
    "K'ib'",
    "Kab'an",
    "Etz'nab'",
    "Kawak",
    "Ajaw",
)
HAAB_MONTHS = (
    "Pop",
    "Wo'",
    "Sip",
    "Sotz'",
    "Sek",
    "Xul",
    "Yaxk'in",
    "Mol",
    "Ch'en",
    "Yax",
    "Sak'",
    "Keh",
    "Mak",
    "K'ank'in",
    "Muwan",
    "Pax",
    "K'ayab",
    "Kumk'u",
    "Wayeb'",
)


def epoch_rd(correlation: int = GMT) -> int:
    """RD dari hari 0.0.0.0.0 untuk konstanta korelasi tertentu."""
    if correlation not in CORRELATIONS:
        raise ValueError(
            f"Korelasi harus salah satu dari {CORRELATIONS}, didapat {correlation}"
        )
    return correlation - JDN_OFFSET


def _days(rd: int, correlation: int) -> int:
    """Jumlah hari sejak 0.0.0.0.0 (negatif kalau sebelumnya)."""
    return rd - epoch_rd(correlation)


def rd_from_long_count(
    baktun: int, katun: int, tun: int, winal: int, kin: int, correlation: int = GMT
) -> int:
    """Hitungan Panjang -> RD."""
    if not (
        0 <= katun <= 19 and 0 <= tun <= 19 and 0 <= winal <= 17 and 0 <= kin <= 19
    ):
        raise ValueError(
            f"Hitungan Panjang tidak valid: {baktun}.{katun}.{tun}.{winal}.{kin}"
        )
    days = baktun * 144000 + katun * 7200 + tun * 360 + winal * 20 + kin
    return epoch_rd(correlation) + days


def long_count_from_rd(
    rd: int, correlation: int = GMT
) -> tuple[int, int, int, int, int]:
    """RD -> Hitungan Panjang (baktun, katun, tun, winal, kin)."""
    baktun, rest = divmod(_days(rd, correlation), 144000)
    katun, rest = divmod(rest, 7200)
    tun, rest = divmod(rest, 360)
    winal, kin = divmod(rest, 20)
    return (baktun, katun, tun, winal, kin)


def haab_from_rd(rd: int, correlation: int = GMT) -> tuple[int, int]:
    """RD -> Haab' (bulan 1–19, tanggal 0–19). Bulan 19 (Wayeb') hanya 5 hari."""
    count = (_days(rd, correlation) + 348) % 365  # hari 0 = 8 Kumk'u = hari ke-348
    return (count // 20 + 1, count % 20)


def tzolkin_from_rd(rd: int, correlation: int = GMT) -> tuple[int, int]:
    """RD -> Tzolk'in (angka 1–13, nama 1–20). Hari 0 = 4 Ajaw."""
    days = _days(rd, correlation)
    return ((days + 3) % 13 + 1, (days + 19) % 20 + 1)


def lord_of_night_from_rd(rd: int, correlation: int = GMT) -> int:
    """RD -> Penguasa Malam G1–G9. Hari 0 = G9."""
    return (_days(rd, correlation) + 8) % 9 + 1
