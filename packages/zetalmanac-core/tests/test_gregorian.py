"""Tes kalender Gregorian: jangkar, sifat (property), dan pembanding independen."""

import datetime

import pytest
from hypothesis import given
from hypothesis import strategies as st

from zetalmanac_core import gregorian as g

# --- L1: Jangkar (tanggal yang diketahui pasti) ---------------------------------


def test_epoch_is_rd_1() -> None:
    assert g.to_rd(1, 1, 1) == 1


def test_known_dates() -> None:
    assert g.to_rd(2026, 11, 4) == 739924
    assert g.to_rd(1945, 8, 17) == 710260
    assert g.from_rd(739924) == (2026, 11, 4)


def test_day_before_epoch_is_31_dec_year_0() -> None:
    # Tahun 0 (astronomis) = 1 SM, dan tahun kabisat
    assert g.from_rd(0) == (0, 12, 31)
    assert g.is_leap_year(0)


@pytest.mark.parametrize(
    ("year", "expected"),
    [
        (2024, True),
        (2025, False),
        (1900, False),
        (2000, True),
        (2100, False),
        (1600, True),
    ],
)
def test_leap_year_rule(year: int, expected: bool) -> None:
    assert g.is_leap_year(year) is expected


@pytest.mark.parametrize(
    ("year", "month", "day"),
    [(2025, 2, 29), (2026, 4, 31), (2026, 13, 1), (2026, 1, 0)],
)
def test_invalid_dates_rejected(year: int, month: int, day: int) -> None:
    with pytest.raises(ValueError):
        g.to_rd(year, month, day)


# --- L3: Sifat yang harus selalu benar (property-based) -------------------------

RD_RANGE = st.integers(min_value=-3_652_059, max_value=3_652_059)  # ±10.000 tahun


@given(RD_RANGE)
def test_round_trip(rd: int) -> None:
    assert g.to_rd(*g.from_rd(rd)) == rd


@given(RD_RANGE)
def test_consecutive_days(rd: int) -> None:
    y1, m1, d1 = g.from_rd(rd)
    y2, m2, d2 = g.from_rd(rd + 1)
    if d2 == 1:  # pergantian bulan
        assert d1 == g.days_in_month(y1, m1)
    else:
        assert (y2, m2, d2) == (y1, m1, d1 + 1)


@given(st.integers(min_value=-10_000, max_value=10_000))
def test_400_year_cycle_is_146097_days(year: int) -> None:
    assert g.to_rd(year + 400, 1, 1) - g.to_rd(year, 1, 1) == 146097


# --- L4: Pembanding independen (differential) ------------------------------------
# datetime.date di Python memakai Gregorian proleptik, dan toordinal() = RD
# (berlaku untuk tahun 1–9999).


@given(st.dates())
def test_matches_python_datetime(date: datetime.date) -> None:
    assert g.to_rd(date.year, date.month, date.day) == date.toordinal()
    assert g.from_rd(date.toordinal()) == (date.year, date.month, date.day)
