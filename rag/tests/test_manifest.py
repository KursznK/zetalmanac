import hashlib

import pytest

from zrag.manifest import check, load, orphans


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "corpus" / "clean").mkdir(parents=True)
    (tmp_path / "docs" / "specs").mkdir(parents=True)
    berkas = tmp_path / "corpus" / "clean" / "contoh.md"
    berkas.write_text("# Contoh\n\nIsi.\n", encoding="utf-8")
    return tmp_path


def _entri(repo, **ubah):
    isi = (repo / "corpus" / "clean" / "contoh.md").read_bytes()
    entri = {
        "id": "contoh",
        "title": "Contoh",
        "path": "corpus/clean/contoh.md",
        "lang": "id",
        "license": "CC-BY-4.0",
        "attribution": "Penulis contoh",
        "sha256": hashlib.sha256(isi).hexdigest(),
    }
    entri.update(ubah)
    return entri


def test_entri_sah(repo):
    assert check([_entri(repo)], root=repo) == []


@pytest.mark.parametrize(
    ("ubah", "potongan_pesan"),
    [
        ({"license": "All-Rights-Reserved"}, "tidak diizinkan"),
        ({"lang": "jv"}, "bahasa"),
        ({"sha256": "0" * 64}, "berubah sejak dicatat"),
        ({"path": "corpus/clean/tidak-ada.md"}, "tidak ada"),
        ({"path": "../../etc/passwd"}, "harus di dalam"),
        ({"path": "apps/api/app/main.py"}, "harus di dalam"),
        ({"id": "Pakai Spasi"}, "id hanya boleh"),
        ({"attribution": ""}, "'attribution' wajib"),
        ({"url": "http://contoh.org"}, "https"),
        ({"url": "https://contoh.org"}, "retrieved_at"),
    ],
)
def test_entri_ditolak(repo, ubah, potongan_pesan):
    masalah = check([_entri(repo, **ubah)], root=repo)
    assert any(potongan_pesan in m for m in masalah), masalah


def test_id_ganda_ditolak(repo):
    masalah = check([_entri(repo), _entri(repo)], root=repo)
    assert any("lebih dari sekali" in m for m in masalah)


def test_berkas_tanpa_catatan_ketahuan(repo):
    (repo / "corpus" / "clean" / "liar.md").write_text("tanpa izin", encoding="utf-8")
    assert orphans([_entri(repo)], root=repo) == ["corpus/clean/liar.md"]


def test_manifest_repo_terbaca():
    entries = load()
    assert len(entries) >= 5
    assert all(e["license"] in {"CC-BY-4.0", "CC-BY-SA-4.0"} for e in entries)
