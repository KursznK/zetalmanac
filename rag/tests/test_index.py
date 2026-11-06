"""Indeks yang di-commit harus sama persis dengan hasil membangun ulang dari korpus."""

from zrag.ingest import OUT, build, serialize
from zrag.search import search


def test_indeks_mutakhir():
    assert OUT.read_text(encoding="utf-8") == serialize(build()), (
        "chunks.jsonl tidak sesuai korpus; jalankan: uv run python -m zrag.ingest"
    )


def test_setiap_potongan_membawa_lisensi_dan_atribusi():
    for chunk in build():
        assert chunk["license"] in {"CC-BY-4.0", "CC-BY-SA-4.0"}
        assert chunk["attribution"]


def test_pencarian_menemukan_dokumen_yang_tepat():
    assert (
        search("julian day number epoch noon")[0][0]["doc_id"] == "wiki-en-julian-day"
    )
    teratas = [
        c["doc_id"] for c, _ in search("siklus 30 tahun kabisat hisab urfi", k=3)
    ]
    assert "spec-hijri-urfi" in teratas
