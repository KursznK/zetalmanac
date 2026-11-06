"""Unduh artikel Wikipedia yang tercatat di manifest sebagai teks polos.

Entri manifest dengan kolom `wikipedia: <judul artikel>` diunduh lewat API resmi Wikipedia
(TextExtracts), disimpan ke corpus/clean/<id>.md, lalu manifest diisi otomatis:
path, url permanen (dengan nomor revisi), revision, retrieved_at, dan sha256.

    uv run python -m zrag.fetch_wikipedia
"""

import json
import time
import urllib.parse
import urllib.request
from datetime import UTC, datetime

from zrag.manifest import REPO_ROOT, load, save, sha256_file

USER_AGENT = "ZetalmanacCorpus/0.1 (https://github.com/KursznK/zetalmanac)"


def fetch(lang: str, title: str) -> dict:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "prop": "extracts|revisions",
            "explaintext": 1,
            "rvprop": "ids",
            "titles": title,
            "redirects": 1,
            "format": "json",
            "formatversion": 2,
        }
    )
    url = f"https://{lang}.wikipedia.org/w/api.php?{params}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        page = json.load(response)["query"]["pages"][0]
    if page.get("missing") or not page.get("extract"):
        raise ValueError(f"Artikel tidak ditemukan: {lang}.wikipedia.org '{title}'")
    return page


def main() -> None:
    entries = load()
    hari_ini = datetime.now(UTC).date().isoformat()
    for e in entries:
        title = e.get("wikipedia")
        if not title:
            continue
        page = fetch(e["lang"], title)
        revisi = page["revisions"][0]["revid"]
        judul = page["title"]
        rel = f"corpus/clean/{e['id']}.md"
        berkas = REPO_ROOT / rel
        berkas.parent.mkdir(parents=True, exist_ok=True)
        berkas.write_text(f"# {judul}\n\n{page['extract'].strip()}\n", encoding="utf-8")
        laman = urllib.parse.quote(judul.replace(" ", "_"))
        e.update(
            {
                "path": rel,
                "url": f"https://{e['lang']}.wikipedia.org/w/index.php?title={laman}&oldid={revisi}",
                "revision": revisi,
                "retrieved_at": hari_ini,
                "attribution": f'Kontributor Wikipedia, "{judul}", {e["lang"]}.wikipedia.org, '
                f"revisi {revisi}. CC BY-SA 4.0",
                "sha256": sha256_file(berkas),
            }
        )
        print(
            f"✓ {e['id']}: {judul} (revisi {revisi}, {len(page['extract'])} karakter)"
        )
        time.sleep(0.5)  # sopan ke server Wikipedia
    save(entries)


if __name__ == "__main__":
    main()
