"use client";

import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-zinc-950 text-white font-sans">
      <main className="flex flex-col items-center text-center px-4">
        <h1 className="text-6xl font-bold tracking-tighter sm:text-7xl mb-6 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
          TRAVO
        </h1>
        <p className="max-w-[600px] text-zinc-400 text-xl mb-10">
          Your AI-Powered Travel Companion. Intelligently planning your trips, identifying monuments, and guiding you through your adventures.
        </p>

        <div className="flex gap-4">
          <Link
            href="/explore"
            className="rounded-full bg-white text-black px-8 py-3 font-medium transition hover:bg-zinc-200"
          >
            Explore
          </Link>
          <Link
            href="/dashboard"
            className="rounded-full border border-zinc-700 px-8 py-3 font-medium transition hover:bg-zinc-800"
          >
            Dashboard
          </Link>
          <a
            href="http://159.138.92.94:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-full border border-zinc-700 px-8 py-3 font-medium transition hover:bg-zinc-800"
          >
            API Docs
          </a>
        </div>
      </main>
    </div>
  );
}
