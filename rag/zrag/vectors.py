"""Penyimpanan vektor embedding: satu berkas biner float16 + satu berkas JSON metadata.

    <nama>.f16   baris-baris vektor (little-endian float16), sudah dinormalisasi panjangnya = 1
    <nama>.json  {"model", "dim", "items": [{"id", "sha256"}]}

sha256 dihitung dari teks yang benar-benar dikirim ke model. Kalau teks potongan berubah, sha256-nya
tidak cocok lagi dan potongan itu perlu di-embed ulang (lihat zrag.embed_index).
"""

import hashlib
import json
import math
import struct
from dataclasses import dataclass
from pathlib import Path


def sha256(teks: str) -> str:
    return hashlib.sha256(teks.encode("utf-8")).hexdigest()


def normalisasi(v: list[float]) -> list[float]:
    """Skala vektor agar panjangnya 1, sehingga cosine similarity = perkalian titik (dot product)."""
    panjang = math.sqrt(sum(x * x for x in v))
    if panjang == 0:
        raise ValueError("vektor nol tidak bisa dinormalisasi")
    return [x / panjang for x in v]


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


@dataclass
class VectorSet:
    model: str
    dim: int
    ids: list[str]
    shas: list[str]
    rows: list[list[float]]

    def by_id(self) -> dict[str, list[float]]:
        return dict(zip(self.ids, self.rows, strict=True))

    def by_sha(self) -> dict[str, list[float]]:
        return dict(zip(self.shas, self.rows, strict=True))


def simpan(prefix: Path, vs: VectorSet) -> None:
    if any(len(r) != vs.dim for r in vs.rows):
        raise ValueError("semua vektor harus berdimensi sama")
    prefix.parent.mkdir(parents=True, exist_ok=True)
    data = b"".join(struct.pack(f"<{vs.dim}e", *normalisasi(r)) for r in vs.rows)
    prefix.with_suffix(".f16").write_bytes(data)
    meta = {
        "model": vs.model,
        "dim": vs.dim,
        "items": [{"id": i, "sha256": s} for i, s in zip(vs.ids, vs.shas, strict=True)],
    }
    prefix.with_suffix(".json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )


def muat(prefix: Path) -> VectorSet:
    meta = json.loads(prefix.with_suffix(".json").read_text(encoding="utf-8"))
    dim, items = meta["dim"], meta["items"]
    data = prefix.with_suffix(".f16").read_bytes()
    if len(data) != 2 * dim * len(items):
        raise ValueError(f"{prefix}: ukuran .f16 tidak cocok dengan metadata")
    rows = [
        list(struct.unpack_from(f"<{dim}e", data, 2 * dim * i))
        for i in range(len(items))
    ]
    return VectorSet(
        model=meta["model"],
        dim=dim,
        ids=[it["id"] for it in items],
        shas=[it["sha256"] for it in items],
        rows=rows,
    )


def ada(prefix: Path) -> bool:
    return prefix.with_suffix(".json").exists() and prefix.with_suffix(".f16").exists()
