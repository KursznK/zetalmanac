"""Tool yang boleh dipanggil LLM. Hitungan tanggal SELALU lewat zetalmanac_core, bukan oleh LLM.

Skema mengikuti format function calling yang dipakai Groq (gaya OpenAI):
{"type": "function", "function": {"name", "description", "parameters": <JSON Schema>}}.
"""

import json

from zetalmanac_core.convert import convert

KALENDER = ("gregorian", "julian", "hijri", "china", "maya")

KONVERSI = {
    "type": "function",
    "function": {
        "name": "konversi_tanggal",
        "description": (
            "Ubah satu tanggal dari sebuah kalender ke semua kalender lain (Gregorian, Julian, "
            "Hijriah hisab urfi, China, Maya), plus nama hari dan Julian Day Number. "
            "Wajib dipakai untuk setiap konversi atau hitungan tanggal; jangan menghitung sendiri."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "kalender": {
                    "type": "string",
                    "enum": list(KALENDER),
                    "description": "Kalender asal tanggal yang diberikan.",
                },
                "tanggal": {
                    "type": "string",
                    "description": (
                        "gregorian/julian/hijri: YYYY-MM-DD dengan tahun astronomis "
                        "(1 SM = 0, 2 SM = -1). china: YYYY-MM-DD dengan YYYY = tahun Masehi saat "
                        "tahun Imlek itu dimulai, MM = nomor bulan Imlek 1-12, DD = 1-30. "
                        "maya: Hitungan Panjang baktun.katun.tun.winal.kin, mis. 13.0.0.0.0."
                    ),
                },
                "bulan_kabisat": {
                    "type": "boolean",
                    "description": "Hanya untuk china: true jika bulannya bulan kabisat (闰月).",
                },
            },
            "required": ["kalender", "tanggal"],
        },
    },
}

TOOLS = [KONVERSI]

CATATAN_HIJRIAH = (
    "Hijriah dihitung dengan hisab urfi (tabular, skema II, epoch sipil). Tanggal resmi yang "
    "ditetapkan lewat rukyat atau hisab hakiki bisa berbeda 1-2 hari."
)


def konversi_tanggal(kalender: str, tanggal: str, bulan_kabisat: bool = False) -> dict:
    """Hasil ringkas untuk LLM (hemat token); galat dikembalikan sebagai data, bukan exception."""
    if kalender not in KALENDER:
        return {"galat": f"kalender harus salah satu dari {', '.join(KALENDER)}"}
    try:
        h = convert(kalender, tanggal, leap=bool(bulan_kabisat))
    except ValueError as e:
        return {"galat": str(e)}
    cn = h["china"]
    return {
        "hari": h["hari"],
        "gregorian": h["gregorian"]["label"],
        "julian": h["julian"]["label"],
        "hijriah": h["hijri"]["label"],
        "china": (
            f"{cn['label']} tahun {cn['year_ganzhi']} ({cn['year_label']})"
            + (" - bulan kabisat" if cn["leap"] else "")
            if cn
            else "di luar rentang data kalender China (1901-2100)"
        ),
        "maya": (
            f"{h['maya']['long_count']}, {h['maya']['tzolkin']} {h['maya']['haab']}, "
            f"{h['maya']['lord_of_night']}"
        ),
        "jdn": h["jdn"],
        "catatan": CATATAN_HIJRIAH,
    }


FUNGSI = {"konversi_tanggal": konversi_tanggal}


def jalankan(nama: str, argumen_json: str) -> tuple[dict, dict]:
    """Jalankan satu panggilan tool dari LLM. Kembalikan (argumen, hasil)."""
    try:
        argumen = json.loads(argumen_json or "{}")
    except json.JSONDecodeError:
        return {}, {"galat": "argumen bukan JSON yang sah"}
    if nama not in FUNGSI:
        return argumen, {"galat": f"tool {nama!r} tidak dikenal"}
    if not isinstance(argumen, dict):
        return {}, {"galat": "argumen harus objek JSON"}
    izin = KONVERSI["function"]["parameters"]["properties"]
    bersih = {k: v for k, v in argumen.items() if k in izin}
    try:
        return argumen, FUNGSI[nama](**bersih)
    except TypeError as e:
        return argumen, {"galat": f"argumen tidak lengkap: {e}"}
