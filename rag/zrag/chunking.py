"""Membersihkan dan memotong dokumen korpus menjadi potongan (chunk) per bagian.

Dokumen dipotong mengikuti judul bagian (Markdown `#`/`##` dan Wikipedia `== ... ==`),
karena satu bagian biasanya membahas satu gagasan. Bagian yang terlalu panjang dipecah
lagi per paragraf, dengan sedikit tumpang tindih supaya konteks di perbatasan tidak hilang.
"""

import re
import unicodedata

MAX_KATA = 300
TUMPANG_TINDIH = 40

# Bagian yang hampir tidak berisi penjelasan: daftar rujukan, tautan, dan sejenisnya.
BAGIAN_DIBUANG = {
    "see also",
    "external links",
    "references",
    "notes",
    "further reading",
    "sources",
    "citations",
    "bibliography",
    "lihat pula",
    "referensi",
    "pranala luar",
    "bacaan lanjutan",
    "catatan",
    "catatan kaki",
    "daftar pustaka",
    "sumber",
}

_JUDUL_MD = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_JUDUL_WIKI = re.compile(r"^(={2,6})\s*(.+?)\s*\1\s*$")


def bersihkan(teks: str) -> str:
    teks = unicodedata.normalize("NFKC", teks)
    teks = teks.replace("[]", "")
    teks = re.sub(r"[ \t]+\n", "\n", teks)
    return re.sub(r"\n{3,}", "\n\n", teks).strip()


def bagian(teks: str) -> list[tuple[list[str], str]]:
    """Pecah dokumen menjadi (jejak judul, isi). Jejak judul misalnya ['Kalender Hijriah', 'Sejarah']."""
    hasil = []
    jejak: list[str] = []
    isi: list[str] = []

    def simpan():
        tubuh = "\n".join(isi).strip()
        if tubuh and not any(j.lower() in BAGIAN_DIBUANG for j in jejak[1:]):
            hasil.append((list(jejak), tubuh))

    for baris in teks.splitlines():
        cocok = _JUDUL_MD.match(baris) or _JUDUL_WIKI.match(baris)
        if cocok:
            simpan()
            isi = []
            # Tingkat judul = jumlah "#" atau "=": judul dokumen "#" = 1, bagian "##"/"==" = 2.
            tingkat = len(cocok.group(1))
            jejak = jejak[: tingkat - 1] + [cocok.group(2)]
        else:
            isi.append(baris)
    simpan()
    return hasil


def potong(
    tubuh: str, max_kata: int = MAX_KATA, tumpang: int = TUMPANG_TINDIH
) -> list[str]:
    """Pecah isi bagian menjadi potongan maksimal `max_kata` kata.

    Paragraf digabung selama muat. Paragraf yang lebih panjang dari batas dipecah dengan
    jendela bergeser. Setiap potongan baru diawali `tumpang` kata terakhir potongan sebelumnya.
    """
    unit: list[list[str]] = []
    for paragraf in re.split(r"\n+", tubuh):
        kata = paragraf.split()
        if not kata:
            continue
        if len(kata) <= max_kata:
            unit.append(kata)
        else:
            langkah = max_kata - tumpang
            unit.extend(
                kata[i : i + max_kata] for i in range(0, len(kata) - tumpang, langkah)
            )
    hasil: list[list[str]] = []
    sekarang: list[str] = []
    for u in unit:
        if sekarang and len(sekarang) + len(u) > max_kata:
            hasil.append(sekarang)
            ekor = sekarang[-tumpang:]
            sekarang = ekor if len(ekor) + len(u) <= max_kata else []
        sekarang = sekarang + u
    if sekarang:
        hasil.append(sekarang)
    return [" ".join(h) for h in hasil]


def chunk_document(doc_id: str, teks: str) -> list[dict]:
    """Dokumen -> daftar chunk {id, doc_id, section, text}."""
    chunks = []
    for jejak, tubuh in bagian(bersihkan(teks)):
        for isi in potong(tubuh):
            chunks.append(
                {
                    "id": f"{doc_id}#{len(chunks)}",
                    "doc_id": doc_id,
                    "section": " › ".join(jejak),
                    "text": isi,
                }
            )
    return chunks
