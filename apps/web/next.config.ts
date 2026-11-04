import type { NextConfig } from "next";

// Alamat API. Di Vercel diisi lewat Environment Variable; di laptop default ke server lokal.
const apiOrigin = process.env.API_ORIGIN ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${apiOrigin}/:path*` }];
  },
};

export default nextConfig;
