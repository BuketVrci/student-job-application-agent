import { getBackendHealth } from "@/lib/api";

export default async function HomePage() {
  const health = await getBackendHealth();

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-8 text-center">
      <h1 className="text-3xl font-semibold">Student Job Application Agent</h1>
      <p className="text-slate-600">
        AI-powered Werkstudent &amp; Praktikum search, document tailoring, and application tracking.
      </p>
      <p className="text-sm">
        Backend status:{" "}
        <span className={health?.status === "ok" ? "text-green-600" : "text-red-600"}>
          {health?.status === "ok" ? "connected" : "unreachable"}
        </span>
      </p>
    </main>
  );
}
