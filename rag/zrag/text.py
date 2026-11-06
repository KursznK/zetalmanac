"""Tokenisasi, stemming, dan deteksi bahasa sederhana untuk BM25 (Indonesia dan Inggris)."""

import re
import unicodedata
from functools import lru_cache

import snowballstemmer

_KATA = re.compile(r"\w+", re.UNICODE)

STOPWORDS = {
    "id": {
        "yang",
        "dan",
        "di",
        "ke",
        "dari",
        "untuk",
        "pada",
        "dengan",
        "adalah",
        "ini",
        "itu",
        "dalam",
        "tidak",
        "akan",
        "atau",
        "juga",
        "oleh",
        "sebagai",
        "karena",
        "ada",
        "bisa",
        "dapat",
        "telah",
        "sudah",
        "lebih",
        "saat",
        "secara",
        "antara",
        "setiap",
        "hal",
        "para",
        "apa",
        "siapa",
        "bagaimana",
        "kapan",
        "berapa",
        "mengapa",
        "kenapa",
        "tersebut",
        "maka",
        "jika",
        "kalau",
        "namun",
        "yaitu",
        "yakni",
        "pun",
        "lah",
        "kah",
        "nya",
        "se",
        "ia",
        "mereka",
        "kita",
        "kami",
        "saya",
        "anda",
    },
    "en": {
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "on",
        "at",
        "for",
        "with",
        "by",
        "from",
        "as",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "which",
        "who",
        "whom",
        "what",
        "when",
        "where",
        "why",
        "how",
        "not",
        "no",
        "but",
        "if",
        "then",
        "than",
        "so",
        "such",
        "into",
        "about",
        "over",
        "after",
        "before",
        "between",
        "during",
        "also",
        "can",
        "could",
        "may",
        "might",
        "will",
        "would",
        "shall",
        "should",
        "do",
        "does",
        "did",
        "has",
        "have",
        "had",
        "i",
        "you",
        "he",
        "she",
        "we",
        "they",
    },
}

_STEMMER = {
    "id": snowballstemmer.stemmer("indonesian"),
    "en": snowballstemmer.stemmer("english"),
}


@lru_cache(maxsize=200_000)
def _stem(lang: str, kata: str) -> str:
    return _STEMMER[lang].stemWord(kata)


def tokens(teks: str, lang: str) -> list[str]:
    """Teks -> token: huruf kecil, tanpa stopword, di-stem sesuai bahasa."""
    teks = unicodedata.normalize("NFKC", teks).lower()
    return [_stem(lang, k) for k in _KATA.findall(teks) if k not in STOPWORDS[lang]]


def words(teks: str) -> list[str]:
    """Kata mentah (huruf kecil, tanpa stemming)."""
    return _KATA.findall(unicodedata.normalize("NFKC", teks).lower())


def detect_lang(teks: str, kosakata: dict[str, set[str]] | None = None) -> str:
    """Tebak bahasa kueri.

    1. Hitung stopword tiap bahasa ("yang", "the", ...).
    2. Kalau seri (misalnya kueri berupa kata kunci saja), hitung kata kueri yang muncul
       di kosakata korpus tiap bahasa.
    3. Masih seri: 'id'.
    """
    kata = words(teks)
    skor = {lang: sum(k in STOPWORDS[lang] for k in kata) for lang in ("id", "en")}
    if skor["id"] == skor["en"] and kosakata:
        skor = {lang: sum(k in kosakata[lang] for k in kata) for lang in ("id", "en")}
    return "en" if skor["en"] > skor["id"] else "id"
