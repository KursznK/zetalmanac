"""Manifest korpus (corpus/sources.yaml) dan aturan tata kelolanya.

Setiap dokumen di korpus wajib tercatat di manifest: dari mana asalnya, lisensinya,
siapa yang harus diberi atribusi, dan sidik jari isinya (SHA-256). Dokumen dengan
lisensi di luar daftar izin ditolak, sehingga korpus selalu boleh dipakai ulang.
"""

import hashlib
import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = REPO_ROOT / "corpus" / "sources.yaml"

LISENSI_DIIZINKAN = {"CC-BY-4.0", "CC-BY-SA-4.0", "CC0-1.0", "public-domain"}
BAHASA = {"id", "en"}
FOLDER_DIIZINKAN = ("corpus/clean/", "docs/specs/")
_ID = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path = MANIFEST) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        raise TypeError("Manifest harus berupa daftar dokumen")
    return data


def check(entries: list[dict], root: Path = REPO_ROOT) -> list[str]:
    """Kembalikan daftar masalah. Daftar kosong berarti manifest sah."""
    masalah = []
    dilihat = set()
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            masalah.append(f"entri ke-{i + 1}: harus berupa objek")
            continue
        nama = e.get("id", f"entri ke-{i + 1}")
        for kolom in (
            "id",
            "title",
            "path",
            "lang",
            "license",
            "attribution",
            "sha256",
        ):
            if not e.get(kolom):
                masalah.append(f"{nama}: kolom '{kolom}' wajib diisi")
        if e.get("id"):
            if not _ID.match(str(e["id"])):
                masalah.append(f"{nama}: id hanya boleh huruf kecil, angka, dan '-'")
            if e["id"] in dilihat:
                masalah.append(f"{nama}: id dipakai lebih dari sekali")
            dilihat.add(e["id"])
        if e.get("license") and e["license"] not in LISENSI_DIIZINKAN:
            masalah.append(f"{nama}: lisensi '{e['license']}' tidak diizinkan")
        if e.get("lang") and e["lang"] not in BAHASA:
            masalah.append(f"{nama}: bahasa harus 'id' atau 'en'")
        if e.get("url") and not str(e["url"]).startswith("https://"):
            masalah.append(f"{nama}: url harus https")
        if e.get("url") and not e.get("retrieved_at"):
            masalah.append(f"{nama}: sumber dari web wajib punya 'retrieved_at'")
        if e.get("sha256") and not _SHA256.match(str(e["sha256"])):
            masalah.append(f"{nama}: sha256 harus 64 karakter heksadesimal")
        rel = str(e.get("path", ""))
        if rel:
            berkas = (root / rel).resolve()
            di_folder_sah = any(
                berkas.is_relative_to((root / folder).resolve())
                for folder in FOLDER_DIIZINKAN
            )
            if not di_folder_sah:
                masalah.append(
                    f"{nama}: path harus di dalam {' atau '.join(FOLDER_DIIZINKAN)}"
                )
            elif not berkas.is_file():
                masalah.append(f"{nama}: berkas {rel} tidak ada")
            elif e.get("sha256") and sha256_file(berkas) != e["sha256"]:
                masalah.append(
                    f"{nama}: isi {rel} berubah sejak dicatat (sha256 tidak cocok); "
                    "kalau perubahannya disengaja, jalankan: uv run python -m zrag.check_corpus --perbarui-sha"
                )
    return masalah


def orphans(entries: list[dict], root: Path = REPO_ROOT) -> list[str]:
    """Berkas di corpus/clean yang tidak tercatat di manifest (asal-usulnya tidak jelas)."""
    tercatat = {str(e.get("path")) for e in entries if isinstance(e, dict)}
    folder = root / "corpus" / "clean"
    if not folder.is_dir():
        return []
    return sorted(
        str(p.relative_to(root))
        for p in folder.rglob("*")
        if p.is_file()
        and p.name != ".gitkeep"
        and str(p.relative_to(root)) not in tercatat
    )


def save(entries: list[dict], path: Path = MANIFEST) -> None:
    kepala = (
        "# Manifest korpus Zetalmanac. Setiap dokumen wajib tercatat di sini.\n"
        "# Diperiksa oleh `uv run python -m zrag.check_corpus` dari folder rag/ (juga di CI).\n"
    )
    isi = yaml.safe_dump(entries, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(kepala + isi, encoding="utf-8")
