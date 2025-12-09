"use client";

import Link from "next/link";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white font-sans selection:bg-purple-500/30">
      <Navbar />

      {/* Hero Section */}
      <section className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6 pt-16 text-center">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-black to-black opacity-50" />

        <h1 className="relative z-10 mx-auto max-w-4xl text-6xl font-bold tracking-tighter sm:text-7xl md:text-8xl">
          <span className="bg-gradient-to-b from-white to-white/70 bg-clip-text text-transparent">
            Explore the World
          </span>
          <br />
          <span className="bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
            Intelligently
          </span>
        </h1>

        <p className="relative z-10 mt-8 max-w-2xl text-lg text-zinc-400 sm:text-xl">
          TRAVO uses advanced AI to identify monuments, plan your perfect itinerary, and guide you through unforgettable adventures.
        </p>

        <div className="relative z-10 mt-10 flex flex-wrap justify-center gap-4">
          <Link
            href="/explore"
            className="group relative rounded-full bg-white px-8 py-3 text-sm font-semibold text-black transition hover:bg-zinc-200"
          >
            Start Exploring
            <span className="absolute inset-0 -z-10 animate-pulse rounded-full bg-white blur-lg opacity-50 transition-opacity group-hover:opacity-75" />
          </Link>
          <Link
            href="/dashboard"
            className="rounded-full border border-zinc-800 bg-zinc-950 px-8 py-3 text-sm font-semibold text-white transition hover:bg-zinc-900 hover:border-zinc-700"
          >
            View Dashboard
          </Link>
        </div>
      </section>

      {/* Stats Section */}
      <section className="border-y border-white/5 bg-white/5 py-12 backdrop-blur-sm">
        <div className="mx-auto grid max-w-7xl grid-cols-2 gap-8 px-6 text-center md:grid-cols-4">
          {[
            { label: "Active Users", value: "10k+" },
            { label: "Monuments Indexed", value: "50k+" },
            { label: "Cities Covered", value: "120+" },
            { label: "AI Accuracy", value: "99%" },
          ].map((stat) => (
            <div key={stat.label}>
              <div className="text-3xl font-bold text-white">{stat.value}</div>
              <div className="mt-1 text-sm text-zinc-500">{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-24">
        <div className="mx-auto max-w-7xl px-6">
          <h2 className="mb-16 text-center text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Everything you need for your journey
          </h2>
          <div className="grid gap-8 md:grid-cols-3">
            {[
              {
                title: "AI Recognition",
                desc: "Point your camera at any monument to instantly get history, facts, and details.",
                icon: "📸",
              },
              {
                title: "Smart Itineraries",
                desc: "Get personalized travel plans based on your interests, time, and budget.",
                icon: "🗺️",
              },
              {
                title: "Local Secrets",
                desc: "Discover hidden gems and local favorites that aren't in the guidebooks.",
                icon: "💎",
              },
            ].map((feature) => (
              <div key={feature.title} className="rounded-2xl border border-white/10 bg-white/5 p-8 transition hover:bg-white/10">
                <div className="mb-4 text-4xl">{feature.icon}</div>
                <h3 className="mb-2 text-xl font-semibold text-white">{feature.title}</h3>
                <p className="text-zinc-400">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
