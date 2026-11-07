# Threat model: asisten tanya-jawab Zetalmanac

- **Cakupan:** alur `zrag.tanya` (validasi → Prompt Guard → retrieval bge-m3 → LLM Groq + tool
  `konversi_tanggal` → pemeriksaan keluaran), endpoint `POST /v1/tanya`, dan halaman `/tanya`
  (Sesi 4.7). Pengaturan dashboard: `docs/operasional/tanya.md`.
- **Acuan:** OWASP Top 10 for LLM Applications 2025.
- **Bukti:** `eval/reports/keamanan.md` (serangan + ambang Prompt Guard), `eval/reports/jawaban.md`,
  `eval/reports/jawaban-tinjauan.md`.
- **Tanggal:** 6 November 2026 (Sesi 4.6).

## Aset dan batas kepercayaan

| Aset | Mengapa penting |
|---|---|
| Kunci API (Groq, Cloudflare) | Hanya di variabel lingkungan server; bocor = kuota dipakai orang lain |
| Kuota gratis harian | Habis = fitur tanya-jawab turun ke mode cadangan |
| Kepercayaan pengguna | Jawaban salah yang meyakinkan merusak reputasi situs |
| Pengunjung situs (bisa di bawah umur) | Tidak boleh menerima konten berbahaya atau skrip |

Yang **tidak dipercaya**: pertanyaan pengunjung dan keluaran LLM. Yang **dipercaya**: korpus (dikurasi,
berlisensi, revisi Wikipedia dipatok, sha256 dicek CI) dan `zetalmanac-core` (tervalidasi ICU/HKO).

## Pemetaan risiko → kontrol → bukti

| OWASP 2025 | Risiko di Zetalmanac | Kontrol | Bukti / tes |
|---|---|---|---|
| LLM01 Prompt Injection | Pengunjung menyuruh model melanggar aturan | Aturan prompt "sumber & pertanyaan adalah data"; sumber dibungkus `<sumber>`; Prompt Guard 2 (ambang 0,5) sebelum LLM; pemeriksaan keluaran | s01–s06; tabel ambang guard |
| LLM02 Sensitive Information Disclosure | Membocorkan kunci atau data pengunjung | Konteks LLM tidak memuat rahasia; kunci hanya di server; Groq ZDR + tanpa pelatihan; Cloudflare tanpa pelatihan; API tidak mencatat teks pertanyaan dan menjawab `Cache-Control: no-store`; field internal (`teks_mentah`) dibuang sebelum dikirim | s15 |
| LLM03 Supply Chain | Dependensi/model berubah diam-diam | `uv.lock` + `uv sync --locked` di CI; Dependabot; ID model dipatok; model preview hanya cadangan | CI |
| LLM04 Data and Model Poisoning | Korpus disisipi teks jahat | Manifest korpus: lisensi, sha256, revisi Wikipedia dipatok, cek berkas yatim; spesifikasi ditinjau manusia | `zrag.check_corpus` di CI |
| LLM05 Improper Output Handling | Keluaran berisi HTML/skrip/tautan phishing | Aturan prompt melarang HTML/tautan; `masalah_keluaran` menolak HTML dan URL; tautan sumber dibuat sistem dari manifest, bukan oleh model; halaman web merender lewat `teks-jawaban.tsx` (hanya tebal, daftar, sitasi; tanpa HTML mentah atau tautan dari model) | s10, s11; `test_keamanan` |
| LLM06 Excessive Agency | Tool disalahgunakan | Satu tool, murni, hanya-baca (tanpa jaringan/berkas); argumen di-whitelist; galat dikembalikan sebagai data; maks. 3 putaran tool | s12, s13; `test_tools` |
| LLM07 System Prompt Leakage | Prompt sistem dibocorkan | Prompt tidak memuat rahasia (bocor pun tidak merugikan); kanari + jejak prompt diperiksa; jawaban yang bocor tidak ditampilkan | s07–s09; `test_tanya` |
| LLM08 Vector and Embedding Weaknesses | Indeks vektor tidak sinkron/tercemar | Korpus publik satu-penyewa; tidak ada unggahan pengguna; sha256 teks disimpan bersama vektor dan dicek tes | `test_dense` |
| LLM09 Misinformation | Jawaban meyakinkan tapi salah | Sitasi wajib dan divalidasi; tanggal hanya dari tool; peringatan hisab urfi; tinjauan manual | `jawaban.md`, `jawaban-tinjauan.md`, s14 |
| LLM10 Unbounded Consumption | Kuota dihabiskan bot | Input ≤ 500 karakter; `max_completion_tokens` 900; ≤ 3 putaran tool; mode web gagal cepat; rantai cadangan; token Turnstile sekali-pakai per pertanyaan; rate limit WAF 5/menit/IP di proyek web; paket gratis tidak bisa menagih biaya | s16, s17; `test_tanya` |

## Keputusan desain

1. **Prompt Guard gagal-terbuka.** Kalau layanan guard gagal, pertanyaan tetap diproses. Guard
   hanya satu lapisan; aturan prompt, kanari, dan pemeriksaan keluaran tetap berjalan. Menutup fitur
   karena guard gagal lebih merugikan pengguna daripada risiko tambahannya.
2. **Ambang guard 0,5 ditetapkan sebelum evaluasi**, supaya tidak di-tuning terhadap dataset uji.
   Tabel ambang di laporan menunjukkan dampak ambang lain.
3. **Dukungan bahasa Indonesia Prompt Guard tidak dijamin dokumentasi**, jadi diukur langsung
   (dataset serangan memuat serangan berbahasa Indonesia).
4. **Rate limit memakai Vercel WAF, bukan Redis.** Batas harian sudah dijaga kuota penyedia, dan
   paket gratis tidak bisa menimbulkan tagihan; menambah layanan penyimpanan tidak sepadan. Aturannya
   di proyek web karena API menerima permintaan lewat rewrite.
5. **Turnstile gagal-tertutup.** Berbeda dengan Prompt Guard: tanpa secret key atau dengan token
   tidak sah, API menolak (503/403) sebelum memanggil layanan berbayar-kuota apa pun.

## Temuan evaluasi (7 November 2026)

Sumber: `eval/reports/keamanan.md` dan `eval/runs/keamanan-serangan.jsonl`.

1. **17/17 serangan lulus**, dihentikan oleh lapisan berbeda: validasi input 1, Prompt Guard 5,
   aturan prompt (LLM menolak) 9, dan 2 dijawab dengan aman (s10 tanpa HTML/skrip; s14 membantah
   klaim kiamat 2012 dengan sitasi). Ini satu kali run; keluaran LLM acak, jadi klaimnya
   "bertahan terhadap 17 serangan uji", bukan "kebal prompt injection".
2. **Prompt Guard hanya menangkap perintah eksplisit "abaikan/ignore instruksi"**, dalam bahasa
   Indonesia maupun Inggris (5/10 serangan injeksi, 0/51 salah blokir). Rekayasa sosial (mengaku admin),
   perintah dalam base64, dan permintaan sopan untuk prompt sistem/aturan/API key lolos guard; kelimanya
   dihentikan aturan prompt.
3. **Pemeriksaan keluaran dan kanari tidak pernah terpicu** dalam uji ini; efektivitasnya baru
   terbukti lewat unit test.
4. **Model cenderung menolak terlalu cepat.** s12 (konversi 1000 tahun) dan s17 (esai 5000 kata)
   ditolak seluruhnya, padahal jawaban yang lebih membantu adalah mengerjakan sebagian kecil dan
   menjelaskan batasnya. Aman, tetapi kurang membantu.
5. **Penolakan karena kebijakan dilabeli sama dengan "tidak ada di sumber"** (s07, s15). Untuk
   pengunjung bedanya tidak penting; untuk analisis log, keduanya tidak bisa dipisahkan.
6. **Jawaban memakai Markdown** (`**tebal**`, daftar bernomor). Diputuskan di Sesi 4.7: renderer
   sendiri yang hanya mengenali tebal, daftar, dan sitasi, tanpa pustaka Markdown dan tanpa HTML.

## Risiko sisa (diterima atau ditunda)

- Serangan yang dirumuskan ulang terus-menerus bisa lolos semua lapisan; dampaknya dibatasi karena
  model tidak punya akses ke rahasia atau aksi yang mengubah apa pun.
- Kesetiaan jawaban pada sumber belum dicek otomatis per klaim (lihat `jawaban-tinjauan.md`).
- Kuota bisa dihabiskan pengunjung yang lolos Turnstile; akibatnya hanya penurunan ke mode cadangan.
- Penolakan yang berlebihan (temuan 4) ditunda: memperbaikinya berarti mengubah prompt lagi, yang
  harus diikuti evaluasi ulang jawaban dan keamanan.
