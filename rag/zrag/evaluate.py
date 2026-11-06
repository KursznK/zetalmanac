"""Evaluasi retrieval: recall@k dan MRR@10 per kategori (id, en, lintas bahasa).

    uv run python -m zrag.evaluate            # cetak ringkasan
    uv run python -m zrag.evaluate --tulis    # juga tulis eval/reports/retrieval-bm25.md

recall@k = target relevan yang muncul di k potongan teratas / jumlah target
MRR@10   = rata-rata 1/peringkat potongan relevan pertama (0 bila tidak ada di 10 teratas)
"""

import sys
from collections.abc import Callable
from pathlib import Path

import yaml

from zrag.manifest import REPO_ROOT, load
from zrag.search import search

DATASET = REPO_ROOT / "eval" / "datasets" / "retrieval" / "queries.yaml"
REPORTS = REPO_ROOT / "eval" / "reports"
KS = (1, 3, 5, 10)
KATEGORI = ("id", "en", "lintas")

Retriever = Callable[[str, int], list[dict]]


def load_dataset(path: Path = DATASET) -> list[dict]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def cocok(chunk: dict, target: dict) -> bool:
    """Apakah potongan ini termasuk target relevan (dokumen, dan bagian bila disebut).

    section dicocokkan dari ujung jejak judul, per judul utuh: "Calendar Round" cocok dengan
    "Maya calendar › Calendar Round", tetapi TIDAK dengan sub-bagiannya
    "Maya calendar › Calendar Round › Year Bearer". Sub-bagian harus dilabeli sendiri.
    """
    if chunk["doc_id"] != target["doc"]:
        return False
    bagian = target.get("section")
    if bagian is None:
        return True
    jejak = chunk["section"].split(" › ")
    if bagian == "(intro)":
        return len(jejak) == 1
    dicari = bagian.split(" › ")
    return jejak[-len(dicari) :] == dicari


def kategori(item: dict, bahasa_dokumen: dict[str, str]) -> str:
    """'lintas' kalau ada target berbahasa lain dari kueri; selain itu bahasa kueri."""
    if any(bahasa_dokumen[t["doc"]] != item["lang"] for t in item["relevan"]):
        return "lintas"
    return item["lang"]


def nilai(hasil: list[dict], targets: list[dict]) -> dict[str, float]:
    """Metrik untuk satu kueri, dari daftar potongan hasil (urut dari teratas)."""
    skor = {}
    for k in KS:
        kena = sum(any(cocok(c, t) for c in hasil[:k]) for t in targets)
        skor[f"recall@{k}"] = kena / len(targets)
    peringkat = next(
        (
            i
            for i, c in enumerate(hasil[:10], start=1)
            if any(cocok(c, t) for t in targets)
        ),
        None,
    )
    skor["mrr@10"] = 1 / peringkat if peringkat else 0.0
    return skor


def bm25(query: str, k: int) -> list[dict]:
    return [c for c, _ in search(query, k)]


def run(retriever: Retriever = bm25) -> list[dict]:
    bahasa_dokumen = {e["id"]: e["lang"] for e in load()}
    baris = []
    for item in load_dataset():
        hasil = retriever(item["query"], max(KS))
        baris.append(
            {
                "id": item["id"],
                "query": item["query"],
                "kategori": kategori(item, bahasa_dokumen),
                "teratas": [c["id"] for c in hasil[:3]],
                **nilai(hasil, item["relevan"]),
            }
        )
    return baris


def ringkas(baris: list[dict]) -> dict[str, dict[str, float]]:
    kolom = [f"recall@{k}" for k in KS] + ["mrr@10"]
    grup = {"semua": baris} | {
        kat: [b for b in baris if b["kategori"] == kat] for kat in KATEGORI
    }
    return {
        nama: {"n": len(isi), **{c: sum(b[c] for b in isi) / len(isi) for c in kolom}}
        for nama, isi in grup.items()
        if isi
    }


def laporan(nama_sistem: str, baris: list[dict]) -> str:
    kolom = [f"recall@{k}" for k in KS] + ["mrr@10"]
    teks = [f"# Evaluasi retrieval: {nama_sistem}\n", f"Dataset: {len(baris)} kueri.\n"]
    teks.append("| kategori | n | " + " | ".join(kolom) + " |")
    teks.append("|---|---|" + "---|" * len(kolom))
    for nama, m in ringkas(baris).items():
        teks.append(
            f"| {nama} | {m['n']} | " + " | ".join(f"{m[c]:.2f}" for c in kolom) + " |"
        )
    teks.append("\n## Kueri dengan recall@5 < 1\n")
    teks.append("| id | kategori | recall@5 | kueri | 3 teratas |")
    teks.append("|---|---|---|---|---|")
    for b in baris:
        if b["recall@5"] < 1:
            teratas = "<br>".join(b["teratas"]) or "(kosong)"
            teks.append(
                f"| {b['id']} | {b['kategori']} | {b['recall@5']:.2f} | {b['query']} | {teratas} |"
            )
    return "\n".join(teks) + "\n"


def main() -> None:
    baris = run()
    teks = laporan("BM25 per bahasa", baris)
    print(teks)
    if "--tulis" in sys.argv:
        REPORTS.mkdir(parents=True, exist_ok=True)
        (REPORTS / "retrieval-bm25.md").write_text(teks, encoding="utf-8")


if __name__ == "__main__":
    main()
