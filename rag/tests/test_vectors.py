import math

import pytest

from zrag.vectors import VectorSet, dot, muat, normalisasi, sha256, simpan


def test_normalisasi_panjang_satu():
    v = normalisasi([3.0, 4.0])
    assert v == pytest.approx([0.6, 0.8])
    assert math.isclose(dot(v, v), 1.0)
    with pytest.raises(ValueError):
        normalisasi([0.0, 0.0])


def test_simpan_lalu_muat(tmp_path):
    vs = VectorSet(
        model="uji",
        dim=3,
        ids=["a#0", "a#1"],
        shas=[sha256("satu"), sha256("dua")],
        rows=[[1.0, 0.0, 0.0], [1.0, 1.0, 0.0]],
    )
    simpan(tmp_path / "vektor", vs)
    hasil = muat(tmp_path / "vektor")
    assert (hasil.model, hasil.dim, hasil.ids, hasil.shas) == (
        "uji",
        3,
        vs.ids,
        vs.shas,
    )
    # disimpan sudah dinormalisasi, presisi float16 (~3 digit)
    assert hasil.rows[1] == pytest.approx([0.7071, 0.7071, 0.0], abs=1e-3)
    assert (tmp_path / "vektor.f16").stat().st_size == 2 * 3 * 2


def test_muat_menolak_berkas_terpotong(tmp_path):
    vs = VectorSet("uji", 2, ["x"], [sha256("x")], [[1.0, 2.0]])
    simpan(tmp_path / "v", vs)
    (tmp_path / "v.f16").write_bytes(b"\x00\x00")
    with pytest.raises(ValueError):
        muat(tmp_path / "v")


def test_dimensi_harus_seragam(tmp_path):
    vs = VectorSet("uji", 2, ["x", "y"], ["s1", "s2"], [[1.0, 0.0], [1.0]])
    with pytest.raises(ValueError):
        simpan(tmp_path / "v", vs)
