import json

from zrag import jawab as modul
from zrag.jawab import (
    PENANDA_TIDAK_ADA,
    info_dokumen,
    jawab,
    pesan_awal,
    rapikan_sitasi,
    sitasi,
)
from zrag.manifest import load

SUMBER = [
    {"id": "d#0", "doc_id": "d", "section": "D › A", "text": "Isi A."},
    {"id": "d#1", "doc_id": "d", "section": "D › B", "text": "Isi B."},
]


def test_sitasi_dipisah_sah_dan_tidak():
    assert sitasi("Fakta [1]. Lagi [2][1]. Palsu [7] dan [0].", 2) == ([1, 2], [0, 7])
    assert sitasi("Tanpa sitasi.", 2) == ([], [])


def test_gaya_sitasi_gpt_oss_dirapikan():
    assert rapikan_sitasi("A【1】 B【2†L3-L5】 C[3]") == "A[1] B[2] C[3]"


def test_pesan_awal_memisahkan_sumber_dan_pertanyaan():
    pesan = pesan_awal("Apa itu?", SUMBER, "2026-11-06")
    assert pesan[0]["role"] == "system"
    assert PENANDA_TIDAK_ADA in pesan[0]["content"]
    assert "2026-11-06" in pesan[0]["content"]
    assert modul.KANARI in pesan[0]["content"]
    assert '<sumber nomor="2" dokumen="d" bagian="D › B">' in pesan[1]["content"]
    assert pesan[2]["content"].endswith("Apa itu?")


def test_setiap_dokumen_punya_url_dan_atribusi():
    info = info_dokumen()
    for e in load():
        assert info[e["id"]]["url"].startswith("https://")
        assert info[e["id"]]["atribusi"]


def respons(content=None, tool_calls=None, token=100):
    pesan = {"role": "assistant", "content": content}
    if tool_calls:
        pesan["tool_calls"] = tool_calls
    return {"choices": [{"message": pesan}], "usage": {"total_tokens": token}}


def test_alur_tool_lalu_jawaban(monkeypatch):
    antrean = [
        respons(
            tool_calls=[
                {
                    "id": "c1",
                    "type": "function",
                    "function": {
                        "name": "konversi_tanggal",
                        "arguments": json.dumps(
                            {"kalender": "hijri", "tanggal": "1448-09-01"}
                        ),
                    },
                }
            ]
        ),
        respons("1 Ramadan 1448 H (hisab urfi) = Senin, 8 Februari 2027."),
    ]
    terkirim = []

    def palsu(model, messages, *_):
        terkirim.append([dict(m) for m in messages])
        return antrean.pop(0)

    monkeypatch.setattr(modul, "panggil_groq", palsu)
    j = jawab("1 Ramadan 1448?", sumber=SUMBER, hari_ini="2026-11-06")
    assert j.ditemukan and "8 Februari 2027" in j.teks
    assert j.tool[0]["hasil"]["gregorian"] == "8 Februari 2027"
    assert j.token == 200
    # putaran kedua mengirim hasil tool dengan tool_call_id yang sama
    assert terkirim[1][-1]["role"] == "tool" and terkirim[1][-1]["tool_call_id"] == "c1"


def test_penanda_tidak_ditemukan_dibuang(monkeypatch):
    monkeypatch.setattr(
        modul,
        "panggil_groq",
        lambda m, p, *_: respons(f"{PENANDA_TIDAK_ADA} Maaf, tidak ada di sumber. [9]"),
    )
    j = jawab("Resep rendang?", sumber=SUMBER, hari_ini="2026-11-06")
    assert not j.ditemukan
    assert j.teks.startswith("Maaf")
    assert j.sitasi_tidak_sah == [9]


def test_tool_use_failed_dicoba_sekali_lagi(monkeypatch):
    from zrag.embed import GalatHTTP

    percobaan = []

    def kirim(model, messages, *_):
        percobaan.append(1)
        if len(percobaan) == 1:
            raise GalatHTTP(400, "HTTP 400: ... tool_use_failed ...")
        return respons("Jawaban [1].")

    monkeypatch.setattr(modul, "_kirim_groq", kirim)
    j = jawab("Apa itu?", sumber=SUMBER, hari_ini="2026-11-06")
    assert j.teks == "Jawaban [1]." and len(percobaan) == 2


def test_galat_lain_tidak_dicoba_ulang(monkeypatch):
    import pytest

    from zrag.embed import GalatHTTP

    def kirim(model, messages, *_):
        raise GalatHTTP(401, "HTTP 401: invalid api key")

    monkeypatch.setattr(modul, "_kirim_groq", kirim)
    with pytest.raises(GalatHTTP):
        jawab("Apa itu?", sumber=SUMBER, hari_ini="2026-11-06")
