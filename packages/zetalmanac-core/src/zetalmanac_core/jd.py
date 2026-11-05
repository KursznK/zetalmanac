"""Julian Date (JD) dan Julian Day Number (JDN) <-> RD.

- RD     : nomor hari, hari dimulai tengah malam. RD 1 = 1 Januari 1 M (Gregorian).
- JD     : hitungan hari (boleh pecahan) sejak tengah hari 1 Januari 4713 SM (Julian).
- JDN    : bilangan bulat JD saat tengah hari pada hari tersebut.

Tengah malam awal hari RD r jatuh pada JD r + 1721424,5,
sedangkan tengah hari hari itu jatuh pada JD r + 1721425 (= JDN).
"""

import math

JD_EPOCH = -1721424.5  # momen RD dari JD 0 (tengah hari 1 Januari 4713 SM, Julian)
JDN_OFFSET = 1721425  # JDN = RD + 1721425


def jd_from_rd(rd: int) -> float:
    """JD pada tengah malam awal hari RD."""
    return rd - JD_EPOCH


def rd_from_jd(jd: float) -> int:
    """RD dari hari yang memuat momen JD."""
    return math.floor(jd + JD_EPOCH)


def jdn_from_rd(rd: int) -> int:
    """JDN (tengah hari) dari hari RD."""
    return rd + JDN_OFFSET


def rd_from_jdn(jdn: int) -> int:
    """RD dari JDN."""
    return jdn - JDN_OFFSET
