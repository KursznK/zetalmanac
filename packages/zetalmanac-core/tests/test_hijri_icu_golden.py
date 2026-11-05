"""Lapis 4 (pembanding independen): Hijriah urfi skema II vs ICU.

Data dibuat oleh scripts/gen_hijri_icu.mjs dan disimpan di tests/data/hijri_icu.csv.
"""

import csv
from pathlib import Path

import pytest

from zetalmanac_core import gregorian, hijri_urfi

GOLDEN = Path(__file__).parent / "data" / "hijri_icu.csv"


def _rows():
    with GOLDEN.open(encoding="utf-8") as f:
        lines = (line for line in f if not line.startswith("#"))
        return list(csv.DictReader(lines))


@pytest.fixture(scope="module")
def rows():
    return _rows()


def test_golden_file_lengkap(rows):
    # Menjaga dari file yang terpotong, kosong, atau lupa disimpan
    assert len(rows) > 50_000
    assert rows[0]["gregorian"] == "0622-07-19"
    assert (rows[0]["civil_year"], rows[0]["civil_month"], rows[0]["civil_day"]) == (
        "1",
        "1",
        "1",
    )
    assert rows[-1]["civil_year"] == "2000"


def test_golden_file_mencatat_sumbernya():
    first_line = GOLDEN.read_text(encoding="utf-8").splitlines()[0]
    assert first_line.startswith("# Sumber: ICU ")


def test_cocok_dengan_icu(rows):
    selisih = []
    for row in rows:
        year, month, day = (int(x) for x in row["gregorian"].split("-"))
        rd = gregorian.to_rd(year, month, day)
        civil = (int(row["civil_year"]), int(row["civil_month"]), int(row["civil_day"]))
        tbla = (int(row["tbla_year"]), int(row["tbla_month"]), int(row["tbla_day"]))

        if hijri_urfi.from_rd(rd, epoch="civil") != civil:
            selisih.append(
                (
                    row["gregorian"],
                    "civil",
                    civil,
                    hijri_urfi.from_rd(rd, epoch="civil"),
                )
            )
        if hijri_urfi.from_rd(rd, epoch="astronomical") != tbla:
            selisih.append(
                (
                    row["gregorian"],
                    "tbla",
                    tbla,
                    hijri_urfi.from_rd(rd, epoch="astronomical"),
                )
            )
        try:
            balik = hijri_urfi.to_rd(*civil)
        except ValueError as e:  # kode kita menganggap tanggal ICU tidak ada
            balik = str(e)
        if balik != rd:
            selisih.append((row["gregorian"], "to_rd", civil, balik))

    # Tampilkan maksimal 10 selisih pertama supaya pesan galat tetap terbaca
    assert not selisih, f"{len(selisih)} selisih, contoh: {selisih[:10]}"
