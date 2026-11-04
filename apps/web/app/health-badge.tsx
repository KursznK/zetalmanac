"use client";

import { useEffect, useState } from "react";

type Health = { status: string; service: string; version: string };

export default function HealthBadge() {
  const [state, setState] = useState<"loading" | "ok" | "error">("loading");
  const [info, setInfo] = useState<Health | null>(null);

  useEffect(() => {
    fetch("/api/v1/health")
      .then((res) => {
        if (!res.ok) throw new Error(String(res.status));
        return res.json();
      })
      .then((data: Health) => {
        setInfo(data);
        setState("ok");
      })
      .catch(() => setState("error"));
  }, []);

  if (state === "loading") {
    return <p className="text-sm text-neutral-500">Memeriksa API…</p>;
  }
  if (state === "error") {
    return <p className="text-sm text-red-600">API belum bisa dihubungi.</p>;
  }
  return (
    <p className="text-sm text-emerald-600">
      API aktif: {info?.service} v{info?.version}
    </p>
  );
}
