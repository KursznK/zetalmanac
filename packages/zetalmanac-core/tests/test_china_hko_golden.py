"""Lapis 4: kalender China (Skyfield/DE440s + aturan) vs tabel HKO 1901–2100.

Data: tests/data/hko_china.csv, dibuat oleh scripts/gen_hko_golden.py.
"""

import csv
from pathlib import Path

import pytest

from zetalmanac_core import china, gregorian

GOLDEN = Path(__file__).parent / "data" / "hko_china.csv"

# Selisih yang sudah diselidiki (Sesi 2.3, 5 Nov 2026). Waktu = momen menurut Skyfield + DE440s,
# dalam waktu Beijing pada masanya (waktu lokal sebelum 1929, UTC+8 sesudahnya).
# Kunci = tanggal versi HKO. Setiap entri wajib punya alasan.
_HKO_AWAL_ABAD = (
    "Untuk 1906–1913, HKO mencatat hari berikutnya walaupun menurut efemeris modern momennya "
    "4–27 menit sebelum tengah malam. Dugaan: tabel HKO untuk masa itu mengikuti kalender resmi "
    "yang dihitung dengan teori lama. Belum dipastikan."
)
BULAN_DIKECUALIKAN = {
    "1906-04-24": "Bulan baru 23 Apr 1906 pukul 23.52 waktu lokal (kita) vs 24 Apr (HKO). "
    + _HKO_AWAL_ABAD,
    "2057-09-28": "Bulan baru 29 Sep 2057 pukul 00.01 (kita) vs 28 Sep (HKO). "
    "HKO sendiri mencantumkan tanggal ini sebagai bisa meleset 1 hari.",
    "2097-08-07": "Bulan baru 8 Agu 2097 pukul 00.02 (kita) vs 7 Agu (HKO). "
    "HKO sendiri mencantumkan tanggal ini sebagai bisa meleset 1 hari.",
}
ZHONGQI_DIKECUALIKAN = {
    "1909-01-21": "大寒 20 Jan 1909 pukul 23.56 waktu lokal (kita) vs 21 Jan (HKO). "
    + _HKO_AWAL_ABAD,
    "2084-03-19": "春分 20 Mar 2084 pukul 00.01 (kita) vs 19 Mar (HKO). "
    "HKO sendiri mencantumkan tanggal ini sebagai bisa meleset 1 hari.",
    "1951-12-23": "冬至 kurang dari 30 detik sebelum tengah malam 22/23 Des 1951. "
    "Di bawah batas ketelitian perbandingan antar-metode.",
    "1979-01-21": "大寒 kurang dari 30 detik sebelum tengah malam 20/21 Jan 1979. "
    "Di bawah batas ketelitian perbandingan antar-metode.",
    "1912-11-23": "小雪 22 Nov 1912 pukul 23.33 waktu lokal (kita) vs 23 Nov (HKO). "
    + _HKO_AWAL_ABAD,
    "1913-09-24": "秋分 23 Sep 1913 pukul 23.38 waktu lokal (kita) vs 24 Sep (HKO). "
    + _HKO_AWAL_ABAD,
}


def _rd(text):
    y, m, d = (int(x) for x in text.split("-"))
    return gregorian.to_rd(y, m, d)


@pytest.fixture(scope="module")
def rows():
    with GOLDEN.open(encoding="utf-8") as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


@pytest.fixture(scope="module")
def bulan(rows):
    return [r for r in rows if r["jenis"] == "bulan"]


def _hari_per_bulan(bulan):
    """Untuk setiap baris awal bulan HKO: (baris, daftar (rd, tanggal versi HKO))."""
    akhir_data = _rd("2101-01-01")
    for k, row in enumerate(bulan):
        start = _rd(row["gregorian"])
        end = _rd(bulan[k + 1]["gregorian"]) if k + 1 < len(bulan) else akhir_data
        tahun, nomor, kabisat = (
            int(row["tahun"]),
            int(row["bulan"]),
            row["kabisat"] == "1",
        )
        yield (
            row,
            [(rd, (tahun, nomor, kabisat, rd - start + 1)) for rd in range(start, end)],
        )


def _zhongqi_berbeda(rows):
    kita = set(china.default_calendar().zhongqi_days)
    return [
        r["gregorian"]
        for r in rows
        if r["jenis"] == "jieqi"
        and int(r["bujur"]) % 30 == 0
        and _rd(r["gregorian"]) not in kita
    ]


def test_golden_file_lengkap(bulan, rows):
    assert len(bulan) > 2400  # ~12,37 bulan per tahun x 200 tahun
    assert bulan[0]["gregorian"].startswith("1901-")
    assert bulan[-1]["tahun"] == "2100"
    assert sum(1 for r in rows if r["jenis"] == "jieqi") == 24 * 200


def test_setiap_hari_cocok_dengan_hko(bulan):
    """Setiap hari dari awal bulan pertama sampai 31 Des 2100 dibandingkan dengan HKO."""
    # Hari yang dikecualikan: seluruh bulan HKO itu, ditambah hari sebelum awalnya
    # (kalau bulan kita mulai sehari lebih awal, hari terakhir bulan sebelumnya ikut berbeda).
    dikecualikan = set()
    for row, hari in _hari_per_bulan(bulan):
        if row["gregorian"] in BULAN_DIKECUALIKAN:
            dikecualikan.update(rd for rd, _ in hari)
            dikecualikan.add(hari[0][0] - 1)

    selisih = []
    for _row, hari in _hari_per_bulan(bulan):
        for rd, hko in hari:
            if rd in dikecualikan:
                continue
            kita = china.from_rd(rd)
            if kita != hko:
                y, m, d = gregorian.from_rd(rd)
                selisih.append((f"{y:04d}-{m:02d}-{d:02d}", "HKO", hko, "kita", kita))
    assert not selisih, f"{len(selisih)} hari berbeda, contoh: {selisih[:10]}"


def test_zhongqi_cocok_dengan_hko(rows):
    """Hari zhongqi (bujur kelipatan 30°) di tabel kita = hari zhongqi di HKO."""
    selisih = [d for d in _zhongqi_berbeda(rows) if d not in ZHONGQI_DIKECUALIKAN]
    assert not selisih, f"{len(selisih)} zhongqi berbeda: {selisih[:10]}"


def test_pengecualian_masih_diperlukan(bulan, rows):
    """Pengecualian yang ternyata sudah cocok harus dihapus, supaya daftarnya tidak basi."""
    bulan_berbeda = {
        row["gregorian"]
        for row, hari in _hari_per_bulan(bulan)
        if any(china.from_rd(rd) != hko for rd, hko in hari)
    }
    basi = [d for d in BULAN_DIKECUALIKAN if d not in bulan_berbeda]
    basi += [d for d in ZHONGQI_DIKECUALIKAN if d not in _zhongqi_berbeda(rows)]
    assert not basi, f"Pengecualian ini sudah tidak diperlukan, hapus: {basi}"
