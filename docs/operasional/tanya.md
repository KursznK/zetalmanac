# Operasional fitur Tanya

Pengaturan yang **tidak ada di repo** (dashboard Cloudflare dan Vercel). Catat di sini setiap kali
diubah, supaya situs bisa dibangun ulang dari nol.

## Alur permintaan

```
browser (halaman /tanya + widget Turnstile)
  → POST zetalmanac.vercel.app/api/v1/tanya       ← aturan rate limit WAF (proyek web)
  → rewrite next.config.ts → zetalmanac-api.vercel.app/v1/tanya
  → verifikasi token Turnstile (Cloudflare siteverify)
  → zrag.tanya: validasi → Prompt Guard → bge-m3 → gpt-oss-120b → Qwen → cadangan → cek keluaran
```

## Cloudflare Turnstile

- Widget mode *Managed*, hostname: `zetalmanac.vercel.app`, `localhost`.
- **Site key** (publik) → proyek web: `NEXT_PUBLIC_TURNSTILE_SITE_KEY`.
- **Secret key** (rahasia) → proyek API: `TURNSTILE_SECRET_KEY`.

## Variabel lingkungan Vercel

| Proyek | Variabel | Isi |
|---|---|---|
| API | `GROQ_API_KEY` | LLM + Prompt Guard (Zero Data Retention aktif) |
| API | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN` | embedding bge-m3 (token: izin Workers AI Read saja) |
| API | `TURNSTILE_SECRET_KEY` | verifikasi anti-bot |
| Web | `NEXT_PUBLIC_TURNSTILE_SITE_KEY` | widget anti-bot (dibaca saat build: redeploy setelah mengubah) |

Tanpa `TURNSTILE_SECRET_KEY`, API menjawab 503 (gagal-tertutup). Tanpa site key, halaman Tanya
menampilkan "belum dikonfigurasi".

## Aturan WAF (proyek web)

- **If:** Request Path *equals* `/api/v1/tanya`
- **Then:** Rate Limit, Fixed Window 60 detik, 5 request, per IP, aksi *Deny* (HTTP 429)
- Hobby: 1 aturan rate limit gratis per proyek.

Aturan dipasang di proyek **web**, bukan API: permintaan ke API datang lewat rewrite, jadi di API
semua pengunjung bisa terlihat berasal dari alamat yang sama. Pemanggil langsung ke API tetap butuh
token Turnstile sekali-pakai.

## Pengembangan lokal

1. Root repo `.env`: `GROQ_API_KEY`, `CLOUDFLARE_*`, `TURNSTILE_SECRET_KEY` (dibaca API lewat zrag).
2. `apps/web/.env.local`: `NEXT_PUBLIC_TURNSTILE_SITE_KEY=...` (Next.js tidak membaca `.env` root).
3. Terminal 1, `apps/api/`: `uv run fastapi dev app/main.py` (port 8000).
4. Terminal 2, `apps/web/`: `npm run dev`, lalu buka http://localhost:3000/tanya.

## Kuota dan pemulihan

- Kuota habis → otomatis turun ke Qwen, lalu ke mode cadangan (cuplikan sumber tanpa AI).
- Cloudflare Workers AI direset 00.00 UTC (07.00 WIB). Waktu reset kuota harian Groq tidak
  didokumentasikan; cek header `x-ratelimit-*`.
