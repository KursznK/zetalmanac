"""Membuat golden file kalender China dari tabel konversi Hong Kong Observatory 1901–2100.

Mengunduh T{tahun}e.txt dari hko.gov.hk (disimpan sementara di ~/.cache/zetalmanac/hko),
lalu menulis tests/data/hko_china.csv berisi:
  - satu baris "bulan" untuk setiap awal bulan Imlek (tahun, bulan, kabisat?)
  - satu baris "jieqi" untuk setiap jieqi (bujur Matahari dalam derajat)
Tanggal di antara dua awal bulan tidak disimpan karena bisa diturunkan.

Jalankan dari packages/zetalmanac-core:
    uv run python scripts/gen_hko_golden.py
"""

import re
import time
import urllib.request
from pathlib import Path

URL = "https://www.hko.gov.hk/en/gts/time/calendar/text/files/T{year}e.txt"
CACHE = Path.home() / ".cache" / "zetalmanac" / "hko"
OUT = Path(__file__).resolve().parent.parent / "tests" / "data" / "hko_china.csv"
YEARS = range(1901, 2101)

JIEQI = {
    "Vernal Equinox": 0,
    "Bright & Clear": 15,
    "Corn Rain": 30,
    "Summer Commences": 45,
    "Corn Forms": 60,
    "Corn on Ear": 75,
    "Summer Solstice": 90,
    "Moderate Heat": 105,
    "Great Heat": 120,
    "Autumn Commences": 135,
    "End of Heat": 150,
    "White Dew": 165,
    "Autumnal Equinox": 180,
    "Cold Dew": 195,
    "Frost": 210,
    "Winter Commences": 225,
    "Light Snow": 240,
    "Heavy Snow": 255,
    "Winter Solstice": 270,
    "Moderate Cold": 285,
    "Severe Cold": 300,
    "Spring Commences": 315,
    "Spring Showers": 330,
    "Insects Waken": 345,
}
# Cacat yang diketahui di file sumber HKO. Setiap entri wajib punya alasan.
KNOWN_GAPS = {
    "2069-12-30": "Baris ini tidak ada di T2069e.txt (dicek 5 Nov 2026), tetapi ada di versi "
    "bahasa China (十七, 星期一). Tanggal Imlek 17, tanpa jieqi.",
}

DAYS = "Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday"
LINE = re.compile(rf"^(\d{{4}})/(\d{{1,2}})/(\d{{1,2}})\s+(.+?)\s+({DAYS})\s*(.*)$")
MONTH = re.compile(r"(\d+)(?:st|nd|rd|th)\s+Lunar\s+Month", re.IGNORECASE)


def fetch(year: int) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"T{year}e.txt"
    if not path.exists():
        request = urllib.request.Request(
            URL.format(year=year), headers={"User-Agent": "zetalmanac-golden/1.0"}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            path.write_bytes(response.read())
        time.sleep(0.3)  # sopan ke server HKO
    return path.read_bytes().decode("utf-8", errors="replace")


def main() -> None:
    rows = []
    lunar_year = None
    month = None
    days_seen = 0
    for year in YEARS:
        text = fetch(year)
        days_in_file = 0
        for line in text.splitlines():
            match = LINE.match(line.strip())
            if not match:
                continue
            y, m, d, lunar, _weekday, term = match.groups()
            days_in_file += 1
            iso = f"{int(y):04d}-{int(m):02d}-{int(d):02d}"

            label = MONTH.search(lunar)
            if label:
                number = int(label.group(1))
                leap = "leap" in lunar.lower() or number == month
                if (
                    lunar_year is None
                ):  # awal bulan pertama yang terlihat (Januari 1901)
                    lunar_year = int(y) - 1 if number >= 11 else int(y)
                elif number == 1 and not leap:
                    lunar_year = int(y)
                month = number
                rows.append(f"{iso},bulan,{lunar_year},{number},{int(leap)},")
            elif not lunar.strip().isdigit():
                raise ValueError(f"Kolom tanggal Imlek tidak dikenali: {line!r}")

            term = term.strip()
            if term:
                if term not in JIEQI:
                    raise ValueError(f"Nama jieqi tidak dikenal di {iso}: {term!r}")
                rows.append(f"{iso},jieqi,,,,{JIEQI[term]}")
        expected = (
            366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
        )
        gaps = sum(1 for day in KNOWN_GAPS if day.startswith(f"{year}-"))
        if days_in_file + gaps != expected:
            raise ValueError(
                f"T{year}e.txt berisi {days_in_file} hari (+{gaps} celah tercatat), seharusnya {expected}"
            )
        days_seen += days_in_file

    header = [
        "# Sumber: Hong Kong Observatory, Gregorian-Lunar Calendar Conversion Table 1901-2100",
        "# (https://www.hko.gov.hk/en/gts/time/conversion1_text.htm), situs yang diterbitkan oleh",
        "# Hong Kong Observatory. Data disalin/diekstrak untuk keperluan nonkomersial; penyalinan ini",
        "# bukan bentuk kerja sama atau afiliasi dengan Observatory, dan Observatory tidak",
        "# menyetujui atau merekomendasikan Zetalmanac.",
        *(f"# Celah di sumber: {day}: {why}" for day, why in KNOWN_GAPS.items()),
        "# Dibuat oleh scripts/gen_hko_golden.py. Jangan disunting manual.",
        "gregorian,jenis,tahun,bulan,kabisat,bujur",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(header + rows) + "\n", encoding="utf-8")
    bulan = sum(1 for r in rows if ",bulan," in r)
    print(
        f"{days_seen} hari dibaca; {bulan} awal bulan dan {len(rows) - bulan} jieqi -> {OUT}"
    )


if __name__ == "__main__":
    main()
