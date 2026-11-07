"""Pecah jawaban LLM menjadi klaim (kalimat) beserta buktinya, untuk dinilai faithfulness-nya.

    uv run python -m zrag.klaim            # tulis eval/datasets/faithfulness/klaim.yaml
    uv run python -m zrag.klaim --timpa    # tulis ulang (label yang sudah diisi akan HILANG)

Bukti sebuah klaim = teks potongan sumber yang dikutipnya ([n]) + hasil tool di jawaban itu.
Klaim dinilai HANYA terhadap bukti itu, bukan terhadap pengetahuan umum.
"""

import json
import re
import sys
import unicodedata

import yaml

from zrag.eval_jawaban import RUNS, load_dataset, model_tersedia, muat_run
from zrag.manifest import REPO_ROOT
from zrag.search import load_chunks

BERKAS = REPO_ROOT / "eval" / "datasets" / "faithfulness" / "klaim.yaml"
LABEL = ("didukung", "sebagian", "tidak_didukung", "bukan_klaim")
SITASI_TEPAT = ("ya", "tidak")
MIN_KARAKTER = 15

PETUNJUK = """\
# Label faithfulness per klaim (Sesi 4.8). Isi `label` setiap klaim dengan salah satu:
#   didukung       : semua isi faktual klaim dinyatakan bukti (tersurat atau parafrase yang setia)
#   sebagian       : sebagian didukung, tetapi ada bagian yang tidak ada di bukti atau dilebih-lebihkan
#   tidak_didukung : inti klaim tidak ada di bukti, atau bertentangan dengan bukti
#   bukan_klaim    : tidak berisi fakta dari sumber (pengantar, penolakan, catatan wajib hisab urfi)
# Nilai HANYA terhadap `bukti` di bawah klaim, bukan pengetahuan umum: klaim yang benar di dunia
# nyata tetapi tidak ada di bukti tetap `tidak_didukung`.
#
# Isi juga `sitasi_tepat` untuk klaim yang punya sitasi (selain itu biarkan null):
#   ya    : sumber yang dikutip ([n]) sendiri memuat isi klaim
#   tidak : isi klaim tidak ada di sumber yang dikutip (mis. sebenarnya berasal dari hasil tool)
# `catatan` boleh diisi alasan singkat. Bukti = sumber yang dikutip + hasil tool. Dibuat `zrag.klaim`.
"""

_SPASI_KHUSUS = dict.fromkeys(map(ord, "    "), " ")
_BUTIR = re.compile(r"^\s*(?:\d+[.)]|[-*•])\s+")
_AKHIR_KALIMAT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\[(*])")
_SITASI = re.compile(r"\[(\d{1,2})\]")


def rapikan(teks: str) -> str:
    """NFKC, spasi khusus jadi spasi biasa, dan sisa sitasi kosong gaya gpt-oss (【】) dibuang."""
    teks = unicodedata.normalize("NFKC", teks).translate(_SPASI_KHUSUS)
    return re.sub(r"\s*【[^】\d]*】", "", teks)


def pecah_kalimat(teks: str) -> list[str]:
    """Baris (termasuk butir daftar) lalu kalimat; potongan sangat pendek dibuang."""
    hasil = []
    for baris in rapikan(teks).splitlines():
        baris = _BUTIR.sub("", baris).strip()
        for k in _AKHIR_KALIMAT.split(baris):
            k = k.strip()
            if len(k) >= MIN_KARAKTER:
                hasil.append(k)
    return hasil


def bukti_untuk(
    kalimat: str, run: dict, teks_potongan: dict[str, str]
) -> tuple[list[int], list[str]]:
    """Nomor sitasi di kalimat dan teks bukti yang ditampilkan untuk penilai."""
    per_nomor = {s["nomor"]: s for s in run["sumber"]}
    nomor = sorted({int(n) for n in _SITASI.findall(kalimat) if int(n) in per_nomor})
    bukti = [
        f"[{n}] {per_nomor[n]['doc_id']} › {per_nomor[n]['section']}\n"
        f"{rapikan(teks_potongan[per_nomor[n]['id']])}"
        for n in nomor
    ]
    for t in run.get("tool", []):
        bukti.append(
            f"[tool {t['nama']}] argumen {json.dumps(t['argumen'], ensure_ascii=False)}\n"
            f"{json.dumps(t['hasil'], ensure_ascii=False)}"
        )
    return nomor, bukti


def ekstrak() -> list[dict]:
    teks_potongan = {c["id"]: c["text"] for c in load_chunks()}
    jenis = {d["id"]: d["jenis"] for d in load_dataset()}
    klaim = []
    for model in model_tersedia():
        for qid, run in muat_run(model).items():
            # Penolakan dan galat tidak berisi klaim dari sumber.
            if (
                run.get("galat")
                or not run.get("ditemukan")
                or jenis.get(qid) == "tolak"
            ):
                continue
            for i, kalimat in enumerate(pecah_kalimat(run["teks"]), start=1):
                nomor, bukti = bukti_untuk(kalimat, run, teks_potongan)
                klaim.append(
                    {
                        "id": f"{model.split('/')[-1]}/{qid}/{i}",
                        "model": model,
                        "pertanyaan": run["pertanyaan"],
                        "klaim": kalimat,
                        "sitasi": nomor,
                        "bukti": bukti,
                        "label": None,
                        "sitasi_tepat": None,
                        "catatan": None,
                    }
                )
    return klaim


class _Dumper(yaml.SafeDumper):
    pass


def _teks(dumper: yaml.SafeDumper, data: str) -> yaml.ScalarNode:
    gaya = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=gaya)


_Dumper.add_representer(str, _teks)


def tulis(klaim: list[dict]) -> str:
    isi = yaml.dump(
        klaim, Dumper=_Dumper, allow_unicode=True, sort_keys=False, width=100
    )
    return PETUNJUK + "\n" + isi


def load(path=BERKAS) -> list[dict]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> None:
    if BERKAS.exists() and "--timpa" not in sys.argv:
        sys.exit(
            f"{BERKAS.relative_to(REPO_ROOT)} sudah ada (mungkin sudah berlabel). Pakai --timpa."
        )
    if not RUNS.exists():
        sys.exit("Belum ada hasil run di eval/runs/. Jalankan zrag.eval_jawaban dulu.")
    klaim = ekstrak()
    BERKAS.parent.mkdir(parents=True, exist_ok=True)
    BERKAS.write_text(tulis(klaim), encoding="utf-8")
    bersitasi = sum(bool(k["sitasi"]) for k in klaim)
    print(
        f"{len(klaim)} klaim ({bersitasi} bersitasi) → {BERKAS.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    main()


def periksa(klaim: list[dict]) -> list[str]:
    """Galat isian label manusia (kosong = sah). Dipakai tes dan sebelum menghitung kesepakatan."""
    galat = []
    for k in klaim:
        if k["label"] not in (*LABEL, None):
            galat.append(f"{k['id']}: label {k['label']!r} tidak dikenal")
        if k["sitasi_tepat"] not in (*SITASI_TEPAT, None):
            galat.append(f"{k['id']}: sitasi_tepat {k['sitasi_tepat']!r} tidak dikenal")
        if k["sitasi_tepat"] is not None and not k["sitasi"]:
            galat.append(f"{k['id']}: sitasi_tepat diisi padahal klaim tanpa sitasi")
    return galat
