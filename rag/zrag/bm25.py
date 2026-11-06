"""Okapi BM25, ditulis sendiri supaya setiap bagian rumusnya kelihatan.

skor(D, Q) = Σ_q IDF(q) · f(q,D)·(k1+1) / (f(q,D) + k1·(1 − b + b·|D|/avgdl))
IDF(q)     = ln(1 + (N − n(q) + 0,5) / (n(q) + 0,5))
"""

import math
from collections import Counter

from zrag.text import tokens


class BM25:
    def __init__(self, chunks: list[dict], lang: str, k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.lang = lang
        self.k1 = k1
        self.b = b
        self.tf = [Counter(tokens(f"{c['section']} {c['text']}", lang)) for c in chunks]
        self.len = [sum(tf.values()) for tf in self.tf]
        self.avgdl = sum(self.len) / len(self.len) if self.len else 0.0
        df = Counter(term for tf in self.tf for term in tf)
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def scores(self, query: str) -> list[float]:
        q = tokens(query, self.lang)
        hasil = []
        for tf, panjang in zip(self.tf, self.len, strict=True):
            norm = (
                self.k1 * (1 - self.b + self.b * panjang / self.avgdl)
                if self.avgdl
                else self.k1
            )
            hasil.append(
                sum(
                    self.idf[t] * tf[t] * (self.k1 + 1) / (tf[t] + norm)
                    for t in q
                    if t in tf
                )
            )
        return hasil

    def search(self, query: str, k: int = 5) -> list[tuple[dict, float]]:
        skor = self.scores(query)
        urutan = sorted(range(len(skor)), key=lambda i: skor[i], reverse=True)
        return [(self.chunks[i], skor[i]) for i in urutan[:k] if skor[i] > 0]
