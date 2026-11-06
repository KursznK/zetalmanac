"""Bangun indeks potongan teks dari korpus: manifest -> potongan -> chunks.jsonl.

    uv run python -m zrag.ingest

Hasilnya dibundel bersama API (apps/api/data/index/). Prosesnya deterministik:
korpus yang sama selalu menghasilkan berkas yang sama persis (diperiksa di tes).
"""

import json

from zrag.chunking import chunk_document
from zrag.manifest import REPO_ROOT, load

OUT = REPO_ROOT / "apps" / "api" / "data" / "index" / "chunks.jsonl"
META = ("lang", "title", "url", "license", "attribution")


def build() -> list[dict]:
    chunks = []
    for e in sorted(load(), key=lambda e: e["id"]):
        teks = (REPO_ROOT / e["path"]).read_text(encoding="utf-8")
        for c in chunk_document(e["id"], teks):
            c.update({k: e.get(k) for k in META})
            chunks.append(c)
    return chunks


def serialize(chunks: list[dict]) -> str:
    return "".join(
        json.dumps(c, ensure_ascii=False, sort_keys=True) + "\n" for c in chunks
    )


def main() -> None:
    chunks = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(serialize(chunks), encoding="utf-8")
    per_bahasa = {lang: sum(c["lang"] == lang for c in chunks) for lang in ("id", "en")}
    kata = [len(c["text"].split()) for c in chunks]
    print(
        f"{len(chunks)} potongan ({per_bahasa['id']} id, {per_bahasa['en']} en); "
        f"rata-rata {sum(kata) / len(kata):.0f} kata, terpanjang {max(kata)} kata -> {OUT}"
    )


if __name__ == "__main__":
    main()
