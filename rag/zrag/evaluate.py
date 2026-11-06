"""Evaluasi retrieval: recall@k dan MRR@10 per kategori (id, en, lintas bahasa).

    uv run python -m zrag.evaluate            # cetak laporan
    uv run python -m zrag.evaluate --tulis    # juga tulis eval/reports/retrieval.md

Sistem yang dibandingkan: BM25, dense (per model embedding yang vektornya sudah dibuat dengan
zrag.embed_index), dan hybrid BM25 + dense yang digabung dengan RRF.

recall@k = target relevan yang muncul di k potongan teratas / jumlah target
MRR@10   = rata-rata 1/peringkat potongan relevan pertama (0 bila tidak ada di 10 teratas)
"""

import sys
from collections.abc import Callable
from pathlib import Path

import yaml

from zrag.dense import cari, kueri_eval, rrf, tersedia
from zrag.embed import EMBEDDERS
from zrag.manifest import REPO_ROOT, load
from zrag.search import search

DATASET = REPO_ROOT / "eval" / "datasets" / "retrieval" / "queries.yaml"
REPORTS = REPO_ROOT / "eval" / "reports"
KS = (1, 3, 5, 10)
KATEGORI = ("id", "en", "lintas")
KEDALAMAN = 50  # kandidat dari tiap retriever sebelum digabung dengan RRF

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


def dense(nama: str) -> Retriever:
    def cari_dense(query: str, k: int) -> list[dict]:
        return [c for c, _ in cari(nama, kueri_eval(nama, query), k)]

    return cari_dense


def hybrid(nama: str) -> Retriever:
    def cari_hybrid(query: str, k: int) -> list[dict]:
        return rrf([bm25(query, KEDALAMAN), dense(nama)(query, KEDALAMAN)])[:k]

    return cari_hybrid


def sistem() -> dict[str, Retriever]:
    """Semua retriever yang bisa dievaluasi (yang vektornya belum dibuat dilewati)."""
    hasil: dict[str, Retriever] = {"BM25": bm25}
    for nama in EMBEDDERS:
        if tersedia(nama):
            hasil[nama] = dense(nama)
            hasil[f"BM25 + {nama} (RRF)"] = hybrid(nama)
        else:
            print(
                f"(lewati {nama}: vektor belum ada; jalankan zrag.embed_index {nama})"
            )
    return hasil


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


def laporan(hasil: dict[str, list[dict]]) -> str:
    """Laporan Markdown untuk beberapa sistem sekaligus (dataset yang sama)."""
    n = len(next(iter(hasil.values())))
    teks = ["# Evaluasi retrieval\n", f"Dataset: {n} kueri, label diperiksa manusia.\n"]

    teks.append("## Ringkasan\n")
    teks.append(
        "| sistem | recall@5 semua | id | en | lintas | recall@10 semua | mrr@10 |"
    )
    teks.append("|---|---|---|---|---|---|---|")
    for nama, baris in hasil.items():
        r = ringkas(baris)
        sel = [
            f"{r[g]['recall@5']:.2f}" if g in r else "-" for g in ("semua", *KATEGORI)
        ]
        teks.append(
            f"| {nama} | "
            + " | ".join(sel)
            + f" | {r['semua']['recall@10']:.2f} | {r['semua']['mrr@10']:.2f} |"
        )

    kolom = [f"recall@{k}" for k in KS] + ["mrr@10"]
    for nama, baris in hasil.items():
        teks.append(f"\n## {nama}\n")
        teks.append("| kategori | n | " + " | ".join(kolom) + " |")
        teks.append("|---|---|" + "---|" * len(kolom))
        for grup, m in ringkas(baris).items():
            nilai_kolom = " | ".join(f"{m[c]:.2f}" for c in kolom)
            teks.append(f"| {grup} | {m['n']} | {nilai_kolom} |")

    nama_sistem = list(hasil)
    teks.append("\n## recall@5 per kueri\n")
    teks.append("| id | kategori | kueri | " + " | ".join(nama_sistem) + " |")
    teks.append("|---|---|---|" + "---|" * len(nama_sistem))
    for i, b in enumerate(next(iter(hasil.values()))):
        sel = " | ".join(f"{hasil[s][i]['recall@5']:.2f}" for s in nama_sistem)
        teks.append(f"| {b['id']} | {b['kategori']} | {b['query']} | {sel} |")
    return "\n".join(teks) + "\n"


def main() -> None:
    hasil = {nama: run(r) for nama, r in sistem().items()}
    teks = laporan(hasil)
    print(teks)
    if "--tulis" in sys.argv:
        REPORTS.mkdir(parents=True, exist_ok=True)
        (REPORTS / "retrieval.md").write_text(teks, encoding="utf-8")


if __name__ == "__main__":
    main()
