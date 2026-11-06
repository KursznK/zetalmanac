"""Periksa manifest korpus. Gagal (exit 1) kalau ada masalah.

uv run python -m zrag.check_corpus
uv run python -m zrag.check_corpus --perbarui-sha   # setelah sengaja mengubah isi dokumen
"""

import sys

from zrag.manifest import REPO_ROOT, check, load, orphans, save, sha256_file


def main() -> int:
    entries = load()
    if "--perbarui-sha" in sys.argv:
        for e in entries:
            berkas = REPO_ROOT / str(e.get("path", ""))
            if e.get("path") and berkas.is_file():
                e["sha256"] = sha256_file(berkas)
        save(entries)
        print("sha256 diperbarui.")
    masalah = check(entries) + [
        f"{p}: tidak tercatat di manifest" for p in orphans(entries)
    ]
    for m in masalah:
        print(f"✗ {m}")
    if masalah:
        print(f"\n{len(masalah)} masalah di corpus/sources.yaml")
        return 1
    lisensi = sorted({e["license"] for e in entries})
    print(f"✓ {len(entries)} dokumen sah ({', '.join(lisensi)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
