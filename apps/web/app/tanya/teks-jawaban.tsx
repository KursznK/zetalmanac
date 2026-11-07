import type { ReactNode } from "react";

// Renderer kecil untuk jawaban LLM (OWASP LLM05: improper output handling).
// Hanya mengenali **tebal**, daftar ("1. ", "- "), dan sitasi [n]. Semua teks lain menjadi
// node teks biasa yang di-escape React: tidak ada dangerouslySetInnerHTML, HTML mentah,
// atau tautan dari model. Satu-satunya tautan adalah sitasi ke daftar sumber di halaman ini.

type Blok = { jenis: "paragraf"; baris: string } | { jenis: "daftar"; berurut: boolean; butir: string[] };

const BUTIR_BERURUT = /^\d+[.)]\s+/;
const BUTIR_BIASA = /^[-*•]\s+/;

export function pecahBlok(teks: string): Blok[] {
  const blok: Blok[] = [];
  for (const mentah of teks.split("\n")) {
    const baris = mentah.trim();
    if (!baris) continue;
    const berurut = BUTIR_BERURUT.test(baris);
    if (berurut || BUTIR_BIASA.test(baris)) {
      const isi = baris.replace(berurut ? BUTIR_BERURUT : BUTIR_BIASA, "");
      const akhir = blok.at(-1);
      if (akhir?.jenis === "daftar" && akhir.berurut === berurut) akhir.butir.push(isi);
      else blok.push({ jenis: "daftar", berurut, butir: [isi] });
    } else {
      blok.push({ jenis: "paragraf", baris });
    }
  }
  return blok;
}

function sebaris(teks: string, nomorSah: ReadonlySet<number>, kunci: string): ReactNode[] {
  // Pisahkan **tebal** dan [n]; bagian lain tetap teks biasa.
  return teks.split(/(\*\*[^*]+\*\*|\[\d{1,2}\])/g).map((bagian, i) => {
    const k = `${kunci}-${i}`;
    if (bagian.startsWith("**") && bagian.endsWith("**") && bagian.length > 4) {
      return <strong key={k}>{bagian.slice(2, -2)}</strong>;
    }
    const sitasi = /^\[(\d{1,2})\]$/.exec(bagian);
    if (sitasi && nomorSah.has(Number(sitasi[1]))) {
      return (
        <sup key={k}>
          <a href={`#sumber-${sitasi[1]}`} className="text-accent hover:underline">
            [{sitasi[1]}]
          </a>
        </sup>
      );
    }
    return bagian;
  });
}

export default function TeksJawaban({ teks, nomorSah }: { teks: string; nomorSah: ReadonlySet<number> }) {
  return (
    <div className="flex flex-col gap-3 leading-relaxed">
      {pecahBlok(teks).map((b, i) =>
        b.jenis === "paragraf" ? (
          <p key={i}>{sebaris(b.baris, nomorSah, `p${i}`)}</p>
        ) : b.berurut ? (
          <ol key={i} className="list-decimal pl-6">
            {b.butir.map((butir, j) => (
              <li key={j}>{sebaris(butir, nomorSah, `o${i}-${j}`)}</li>
            ))}
          </ol>
        ) : (
          <ul key={i} className="list-disc pl-6">
            {b.butir.map((butir, j) => (
              <li key={j}>{sebaris(butir, nomorSah, `u${i}-${j}`)}</li>
            ))}
          </ul>
        ),
      )}
    </div>
  );
}
