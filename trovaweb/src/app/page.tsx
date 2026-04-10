import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black">
      <section className="mx-auto max-w-5xl px-6 py-16">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 items-center">
          <div>
            <h1 className="text-4xl font-bold text-zinc-900 dark:text-zinc-100">TrovaWeb</h1>
            <p className="mt-4 text-lg text-zinc-700 dark:text-zinc-300">
              Discover monuments with AI. Try the camera demo, view results on the dashboard, and explore the API.
            </p>
            <div className="mt-6 flex gap-3">
              <Link href="/explore" className="rounded-md bg-foreground px-5 py-2 text-background hover:bg-[#383838] dark:hover:bg-[#ccc]">Explore</Link>
              <Link href="/dashboard" className="rounded-md border border-black/10 dark:border-white/20 px-5 py-2 hover:bg-black/5 dark:hover:bg-white/10">Dashboard</Link>
              <Link href="/api-docs" className="rounded-md border border-black/10 dark:border-white/20 px-5 py-2 hover:bg-black/5 dark:hover:bg-white/10">API Docs</Link>
            </div>
          </div>
          <div className="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-6">
            <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100">Monument Identification Demo</h2>
            <p className="mt-2 text-sm text-zinc-700 dark:text-zinc-300">Upload an image on the demo page to identify a monument and get details.</p>
            <div className="mt-4">
              <Link href="/demo" className="inline-block rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">Open Demo</Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
