"""Langkah hitung yang bisa ditampilkan ("Tunjukkan langkah"), dengan angka antara yang asli.

Setiap fungsi mengembalikan daftar langkah: {"judul": str, "baris": [str, ...]}.
Angka di sini dihitung dengan rumus yang sama dengan modul kalendernya, lalu dicocokkan
dengan hasil modul itu di tes, supaya penjelasan tidak pernah berbeda dari jawaban.
"""

from zetalmanac_core import gregorian, hijri_urfi, maya
from zetalmanac_core.jd import JDN_OFFSET


def _langkah(judul: str, *baris: str) -> dict:
    return {"judul": judul, "baris": list(baris)}


def gregorian_steps(year: int, month: int, day: int) -> list[dict]:
    """Gregorian -> RD."""
    y = year - 1
    bulan = (367 * month - 362) // 12
    if month <= 2:
        koreksi, alasan = 0, "bulan Januari/Februari"
    elif gregorian.is_leap_year(year):
        koreksi, alasan = -1, f"{year} tahun kabisat"
    else:
        koreksi, alasan = -2, f"{year} bukan tahun kabisat"
    rd = 365 * y + y // 4 - y // 100 + y // 400 + bulan + koreksi + day
    assert rd == gregorian.to_rd(year, month, day)
    return [
        _langkah(
            "Hari dari tahun-tahun yang sudah lewat",
            f"365 × {y} = {365 * y}",
            f"kabisat: ⌊{y}/4⌋ − ⌊{y}/100⌋ + ⌊{y}/400⌋ = {y // 4} − {y // 100} + {y // 400}"
            f" = {y // 4 - y // 100 + y // 400}",
        ),
        _langkah(
            "Hari dari bulan-bulan yang sudah lewat (anggap Februari 30 hari)",
            f"⌊(367 × {month} − 362) / 12⌋ = ⌊{367 * month - 362}/12⌋ = {bulan}",
            f"koreksi Februari: {koreksi} ({alasan})",
        ),
        _langkah(
            "Jumlahkan dengan tanggal",
            f"RD = {365 * y} + {y // 4 - y // 100 + y // 400} + {bulan} + ({koreksi}) + {day} = {rd}",
        ),
    ]


def hijri_steps(
    rd: int, scheme: str = "II", epoch: str = "civil", after_sunset: bool = False
) -> list[dict]:
    """RD -> Hijriah urfi."""
    langkah = []
    if after_sunset:
        langkah.append(
            _langkah(
                "Setelah magrib",
                f"hari Hijriah sudah berganti: pakai RD {rd} + 1 = {rd + 1}",
            )
        )
        rd += 1
    awal = hijri_urfi.EPOCHS[epoch]
    nama_epoch = (
        "sipil, Jumat 16 Juli 622 J"
        if epoch == "civil"
        else "astronomis, Kamis 15 Juli 622 J"
    )
    n = rd - awal
    siklus, sisa = divmod(n, hijri_urfi.CYCLE_DAYS)
    tahun = 30 * siklus + 1
    langkah.append(
        _langkah(f"Hari sejak 1 Muharam 1 H ({nama_epoch})", f"n = {rd} − {awal} = {n}")
    )
    langkah.append(
        _langkah(
            "Siklus 30 tahun penuh (10.631 hari)",
            f"{n} = {siklus} × 10631 + {sisa}",
            f"siklus ke-{siklus + 1} dimulai tahun 30 × {siklus} + 1 = {tahun}",
        )
    )
    rincian = []
    total = 0
    while True:
        panjang = 355 if hijri_urfi.is_leap_year(tahun, scheme) else 354
        if sisa < panjang:
            break
        rincian.append(f"{tahun}: {panjang}{' (kabisat)' if panjang == 355 else ''}")
        sisa -= panjang
        total += panjang
        tahun += 1
    baris = [
        f"skema {scheme}, kabisat pada tahun ke-{', '.join(map(str, hijri_urfi.LEAP_YEARS[scheme]))}"
    ]
    if rincian:
        baris += rincian + [
            f"jumlah {total} hari → sisa p = {sisa} hari di tahun {tahun}"
        ]
    else:
        baris.append(f"sisa p = {sisa} hari di tahun {tahun}")
    langkah.append(_langkah("Telusuri tahun di dalam siklus", *baris))
    bulan = (11 * sisa + 330) // 325
    sebelum = 29 * (bulan - 1) + bulan // 2
    tanggal = sisa - sebelum + 1
    langkah.append(
        _langkah(
            "Bulan",
            f"m = ⌊(11 × {sisa} + 330) / 325⌋ = ⌊{11 * sisa + 330}/325⌋ = {bulan} → {hijri_urfi.MONTHS[bulan - 1]}",
        )
    )
    langkah.append(
        _langkah(
            "Tanggal",
            f"hari sebelum bulan {bulan} = 29 × {bulan - 1} + ⌊{bulan}/2⌋ = {sebelum}",
            f"d = {sisa} − {sebelum} + 1 = {tanggal}",
        )
    )
    assert (tahun, bulan, tanggal) == hijri_urfi.from_rd(rd, scheme, epoch)
    return langkah


def maya_steps(rd: int, correlation: int = maya.GMT) -> list[dict]:
    """RD -> Hitungan Panjang, Tzolk'in, Haab', Penguasa Malam."""
    jdn = rd + JDN_OFFSET
    n = jdn - correlation
    baktun, r1 = divmod(n, 144000)
    katun, r2 = divmod(r1, 7200)
    tun, r3 = divmod(r2, 360)
    winal, kin = divmod(r3, 20)
    tz_angka = (n + 3) % 13 + 1
    tz_nama = (n + 19) % 20
    haab = (n + 348) % 365
    g = (n + 8) % 9 + 1
    assert (baktun, katun, tun, winal, kin) == maya.long_count_from_rd(rd, correlation)
    return [
        _langkah("Julian Day Number", f"JDN = {rd} + {JDN_OFFSET} = {jdn}"),
        _langkah(
            f"Hari sejak 0.0.0.0.0 (korelasi {correlation})",
            f"n = {jdn} − {correlation} = {n}",
        ),
        _langkah(
            "Bagi berturut-turut",
            f"{n} = {baktun} × 144000 + {r1} → baktun {baktun}",
            f"{r1} = {katun} × 7200 + {r2} → katun {katun}",
            f"{r2} = {tun} × 360 + {r3} → tun {tun}",
            f"{r3} = {winal} × 20 + {kin} → winal {winal}, kin {kin}",
        ),
        _langkah(
            "Tzolk'in",
            f"angka = ((n + 3) mod 13) + 1 = {tz_angka}",
            f"nama = (n + 19) mod 20 = {tz_nama} → {maya.TZOLKIN_NAMES[tz_nama]}",
        ),
        _langkah(
            "Haab'",
            f"(n + 348) mod 365 = {haab} → bulan ke-{haab // 20 + 1} ({maya.HAAB_MONTHS[haab // 20]}),"
            f" tanggal {haab % 20}",
        ),
        _langkah("Penguasa Malam", f"((n + 8) mod 9) + 1 = {g} → G{g}"),
    ]
