"""Evaluasi jawaban LLM (RAG + tool) terhadap eval/datasets/answer/questions.yaml.

    uv run python -m zrag.eval_jawaban jalankan openai/gpt-oss-120b qwen/qwen3.8-27b
    uv run python -m zrag.eval_jawaban laporan --tulis

`jalankan` butuh internet dan kunci di .env; hasil mentah disimpan per model di eval/runs/
(bisa dilanjutkan kalau terputus: pertanyaan yang sudah dijawab dilewati). `laporan` hanya
membaca eval/runs/, jadi penilaian bisa diulang tanpa memanggil API lagi.
"""

import json
import sys
import time
import unicodedata
from dataclasses import asdict
from pathlib import Path

import yaml
from zetalmanac_core.convert import to_rd

from zrag.embed import GalatHTTP
from zrag.evaluate import cocok
from zrag.jawab import jawab
from zrag.manifest import REPO_ROOT
from zrag.search import load_chunks

DATASET = REPO_ROOT / "eval" / "datasets" / "answer" / "questions.yaml"
RUNS = REPO_ROOT / "eval" / "runs"
REPORT = REPO_ROOT / "eval" / "reports" / "jawaban.md"
JENIS = ("konversi", "fakta", "tolak")
JEDA_DETIK = 20  # kuota gratis 8 ribu token/menit; satu pertanyaan bisa ±3-6 ribu token


def load_dataset(path: Path = DATASET) -> list[dict]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def berkas_run(model: str) -> Path:
    return RUNS / f"jawaban-{model.replace('/', '__')}.jsonl"


def muat_run(model: str) -> dict[str, dict]:
    path = berkas_run(model)
    if not path.exists():
        return {}
    baris = [json.loads(b) for b in path.read_text(encoding="utf-8").splitlines() if b]
    return {b["id"]: b for b in baris}


def jalankan(model: str, jeda: float = JEDA_DETIK) -> None:
    sudah = muat_run(model)
    data = load_dataset()
    RUNS.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(data):
        lama = sudah.get(item["id"])
        if lama and lama["pertanyaan"] == item["pertanyaan"] and not lama.get("galat"):
            continue
        print(f"{model} · {item['id']}: {item['pertanyaan']}")
        try:
            hasil = asdict(jawab(item["pertanyaan"], model=model))
        except GalatHTTP as e:
            # Dicatat sebagai kegagalan (dihitung tidak lulus), lalu lanjut ke pertanyaan
            # berikutnya. Dijalankan ulang otomatis pada `jalankan` berikutnya.
            print(f"  gagal: {e}")
            hasil = {"pertanyaan": item["pertanyaan"], "galat": str(e)[:300]}
        sudah[item["id"]] = {"id": item["id"], **hasil}
        urut = [sudah[d["id"]] for d in data if d["id"] in sudah]
        berkas_run(model).write_text(
            "".join(json.dumps(b, ensure_ascii=False) + "\n" for b in urut),
            encoding="utf-8",
        )
        if i < len(data) - 1:
            time.sleep(jeda)


# gpt-oss sering memakai spasi sempit tak-terputus (U+202F) dan tanda hubung khusus (U+2011).
# Di layar tampak sama, tetapi "8\u202fFebruari" != "8 Februari" bagi komputer.
_SAMAKAN = dict.fromkeys(map(ord, "\u00a0\u2007\u2009\u202f"), " ") | dict.fromkeys(
    map(ord, "\u2010\u2011\u2012\u2013\u2014"), "-"
)


def normal(teks: str) -> str:
    """Samakan bentuk teks sebelum dicocokkan: Unicode NFKC, spasi/tanda hubung khusus, huruf kecil."""
    return unicodedata.normalize("NFKC", teks).translate(_SAMAKAN).lower()


def memuat(teks: str, pilihan: list[str]) -> bool:
    return any(normal(p) in normal(teks) for p in pilihan)


def argumen_tepat(harapan: dict, argumen: dict) -> bool:
    """Bandingkan lewat RD, jadi '1448-9-1' dan '1448-09-01' dianggap sama."""
    if argumen.get("kalender") != harapan["kalender"]:
        return False
    if bool(argumen.get("bulan_kabisat", False)) != bool(
        harapan.get("bulan_kabisat", False)
    ):
        return False
    try:
        kabisat = bool(harapan.get("bulan_kabisat", False))
        return to_rd(
            harapan["kalender"], str(argumen.get("tanggal", "")), leap=kabisat
        ) == to_rd(harapan["kalender"], harapan["tanggal"], leap=kabisat)
    except ValueError:
        return False


def nilai_item(item: dict, run: dict, chunks: dict[str, dict]) -> dict[str, bool]:
    """Pemeriksaan untuk satu pertanyaan. `lulus` = semua pemeriksaan benar."""
    cek: dict[str, bool] = {}
    if run.get("galat"):
        return {"tanpa_galat": False, "lulus": False}
    if item["jenis"] == "konversi":
        konversi = [t for t in run["tool"] if t["nama"] == "konversi_tanggal"]
        cek["tool_dipanggil"] = bool(konversi)
        cek["argumen_tepat"] = any(
            argumen_tepat(item["tool"], t["argumen"]) for t in konversi
        )
        cek["tidak_menolak"] = run["ditemukan"]
        cek["isi_benar"] = memuat(run["teks"], item["harus_memuat"])
    elif item["jenis"] == "fakta":
        dikutip = [s for s in run["sumber"] if s["nomor"] in run["sitasi"]]
        cek["tidak_menolak"] = run["ditemukan"]
        cek["ada_sitasi"] = bool(run["sitasi"])
        cek["sitasi_sah"] = not run["sitasi_tidak_sah"]
        cek["sitasi_relevan"] = any(
            cocok(chunks[s["id"]], t) for s in dikutip for t in item["relevan"]
        )
        cek["isi_benar"] = memuat(run["teks"], item["harus_memuat"])
    else:
        cek["menolak"] = not run["ditemukan"]
        cek["tanpa_sitasi_palsu"] = not run["sitasi_tidak_sah"]
    cek["lulus"] = all(cek.values())
    return cek


def nilai_model(model: str) -> list[dict]:
    runs = muat_run(model)
    chunks = {c["id"]: c for c in load_chunks()}
    hasil = []
    for item in load_dataset():
        if item["id"] in runs:
            run = runs[item["id"]]
            hasil.append(
                {
                    "id": item["id"],
                    "jenis": item["jenis"],
                    "token": run.get("token", 0),
                    "detik": run.get("detik", 0.0),
                    "retrieval": run.get("retrieval", "-"),
                    **nilai_item(item, run, chunks),
                }
            )
    return hasil


def model_tersedia() -> list[str]:
    if not RUNS.exists():
        return []
    return sorted(
        p.stem.removeprefix("jawaban-").replace("__", "/")
        for p in RUNS.glob("jawaban-*.jsonl")
    )


def laporan() -> str:
    n = len(load_dataset())
    teks = [
        "# Evaluasi jawaban (RAG + tool)\n",
        f"Dataset: {n} pertanyaan (konversi, fakta, tolak). Retrieval: bge-m3 (ADR 0001).\n",
        "## Ringkasan (pertanyaan lulus / jumlah)\n",
        "| model | konversi | fakta | tolak | total | token rata-rata | detik rata-rata |",
        "|---|---|---|---|---|---|---|",
    ]
    semua = {m: nilai_model(m) for m in model_tersedia()}
    for model, hasil in semua.items():
        sel = []
        for jenis in JENIS:
            isi = [h for h in hasil if h["jenis"] == jenis]
            sel.append(f"{sum(h['lulus'] for h in isi)}/{len(isi)}")
        total = f"{sum(h['lulus'] for h in hasil)}/{len(hasil)}"
        token = sum(h["token"] for h in hasil) / max(len(hasil), 1)
        detik = sum(h["detik"] for h in hasil) / max(len(hasil), 1)
        teks.append(
            f"| {model} | {' | '.join(sel)} | {total} | {token:.0f} | {detik:.1f} |"
        )
    for model, hasil in semua.items():
        teks.append(f"\n## {model}\n")
        teks.append("| id | jenis | lulus | pemeriksaan gagal | token | retrieval |")
        teks.append("|---|---|---|---|---|---|")
        for h in hasil:
            gagal = [k for k, v in h.items() if v is False and k not in ("lulus",)]
            teks.append(
                f"| {h['id']} | {h['jenis']} | {'ya' if h['lulus'] else 'tidak'} | "
                f"{', '.join(gagal) or '-'} | {h['token']} | {h['retrieval']} |"
            )
    return "\n".join(teks) + "\n"


def main() -> None:
    perintah = sys.argv[1:2]
    if perintah == ["jalankan"] and len(sys.argv) > 2:
        for model in sys.argv[2:]:
            jalankan(model)
    elif perintah == ["laporan"]:
        teks = laporan()
        print(teks)
        if "--tulis" in sys.argv:
            REPORT.write_text(teks, encoding="utf-8")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
