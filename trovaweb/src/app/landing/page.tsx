'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-black text-white font-sans selection:bg-blue-500 selection:text-white">
            {/* Navigation */}
            <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 backdrop-blur-md bg-black/50 border-b border-white/10">
                <div className="text-2xl font-bold tracking-tighter bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                    Memora
                </div>
                <div className="flex gap-6 text-sm font-medium text-zinc-400">
                    <Link href="#features" className="hover:text-white transition-colors">Features</Link>
                    <Link href="#about" className="hover:text-white transition-colors">About</Link>
                    <Link href="/demo" className="hover:text-white transition-colors">Demo</Link>
                </div>
                <Link
                    href="/dashboard"
                    className="px-4 py-2 text-sm font-semibold bg-white text-black rounded-full hover:bg-zinc-200 transition-colors"
                >
                    Get Started
                </Link>
            </nav>

            {/* Hero Section */}
            <section className="relative flex flex-col items-center justify-center min-h-screen px-6 pt-20 text-center overflow-hidden">
                {/* Background Gradients */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500/20 rounded-full blur-[120px] -z-10" />
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-purple-500/20 rounded-full blur-[100px] -z-10 translate-x-20 translate-y-20" />

                <motion.h1
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    className="max-w-4xl text-5xl md:text-7xl font-bold tracking-tight leading-tight"
                >
                    Travel Smarter with <br />
                    <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                        AI-Powered Vision
                    </span>
                </motion.h1>

                <motion.p
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
                    className="mt-6 max-w-2xl text-lg md:text-xl text-zinc-400"
                >
                    Instantly identify monuments, track your journey, and get personalized recommendations. Your personal travel guide, reinvented.
                </motion.p>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.4, ease: "easeOut" }}
                    className="mt-10 flex flex-col sm:flex-row gap-4"
                >
                    <Link
                        href="/dashboard"
                        className="px-8 py-4 text-lg font-semibold bg-white text-black rounded-full hover:bg-zinc-200 transition-all hover:scale-105 active:scale-95"
                    >
                        Start Your Journey
                    </Link>
                    <Link
                        href="/demo"
                        className="px-8 py-4 text-lg font-semibold bg-white/10 text-white border border-white/10 rounded-full hover:bg-white/20 transition-all hover:scale-105 active:scale-95 backdrop-blur-sm"
                    >
                        Try the Demo
                    </Link>
                </motion.div>

                {/* Floating UI Elements (Mock) */}
                <motion.div
                    initial={{ opacity: 0, y: 50 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, delay: 0.6 }}
                    className="mt-20 relative w-full max-w-5xl aspect-[16/9] bg-zinc-900/50 rounded-xl border border-white/10 shadow-2xl overflow-hidden backdrop-blur-sm"
                >
                    <div className="absolute inset-0 flex flex-col items-center justify-center bg-zinc-900 text-zinc-700">
                        <div className="w-64 h-full bg-black border-x border-white/10 flex flex-col relative overflow-hidden">
                            {/* Mock Header */}
                            <div className="h-14 border-b border-white/10 flex items-center justify-center font-bold text-white">
                                My Diary
                            </div>
                            {/* Mock Content */}
                            <div className="flex-1 p-4 space-y-4">
                                <div className="h-40 bg-zinc-800 rounded-lg animate-pulse" />
                                <div className="h-4 w-3/4 bg-zinc-800 rounded animate-pulse" />
                                <div className="h-4 w-1/2 bg-zinc-800 rounded animate-pulse" />
                            </div>
                            {/* Mock Tab Bar */}
                            <div className="h-16 border-t border-white/10 flex items-center justify-around text-2xl">
                                <span>🏠</span>
                                <span className="text-blue-500">📷</span>
                                <span>👤</span>
                            </div>
                        </div>
                    </div>
                </motion.div>
            </section>

            {/* Features Section */}
            <section id="features" className="py-32 px-6 bg-zinc-950">
                <div className="max-w-6xl mx-auto">
                    <h2 className="text-3xl md:text-5xl font-bold text-center mb-20">
                        Everything you need <br />
                        <span className="text-zinc-500">to explore the world.</span>
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {[
                            { title: "AI Vision", desc: "Point your camera at any monument to get instant history and facts.", icon: "👁️" },
                            { title: "Smart Diary", desc: "Automatically log your trips with GPS and photo recognition.", icon: "📔" },
                            { title: "Local Guide", desc: "Get real-time recommendations based on your interests.", icon: "🗺️" }
                        ].map((feature, i) => (
                            <div key={i} className="p-8 rounded-3xl bg-zinc-900/50 border border-white/5 hover:border-white/10 transition-colors">
                                <div className="text-4xl mb-6">{feature.icon}</div>
                                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                                <p className="text-zinc-400 leading-relaxed">{feature.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="py-24 px-6 bg-black">
                <div className="max-w-6xl mx-auto">
                    <h2 className="text-3xl md:text-5xl font-bold text-center mb-16">
                        Your Journey, <span className="text-blue-500">Simplified.</span>
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center">
                        {[
                            { step: "01", title: "Snap", desc: "Take a photo of any monument or landmark." },
                            { step: "02", title: "Identify", desc: "Our AI instantly recognizes it and tells you its story." },
                            { step: "03", title: "Track", desc: "It's automatically added to your travel diary." }
                        ].map((item, i) => (
                            <div key={i} className="relative p-6">
                                <div className="text-8xl font-bold text-zinc-900 absolute -top-10 left-1/2 -translate-x-1/2 -z-10 select-none">
                                    {item.step}
                                </div>
                                <h3 className="text-2xl font-bold mb-4">{item.title}</h3>
                                <p className="text-zinc-400">{item.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Testimonials Section */}
            <section className="py-24 px-6 bg-zinc-900/30 border-y border-white/5">
                <div className="max-w-4xl mx-auto text-center">
                    <h2 className="text-3xl font-bold mb-12">Loved by Travelers</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {[
                            { quote: "Memora changed how I travel. No more guessing what I'm looking at!", author: "Sarah J., Backpacker" },
                            { quote: "The automated diary feature is a lifesaver. I have a record of everywhere I've been.", author: "Mike T., Digital Nomad" }
                        ].map((t, i) => (
                            <div key={i} className="p-8 rounded-2xl bg-black border border-white/10 text-left">
                                <p className="text-lg text-zinc-300 mb-6">"{t.quote}"</p>
                                <p className="font-semibold text-blue-400">{t.author}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-32 px-6 text-center relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-b from-transparent to-blue-900/20 pointer-events-none" />
                <h2 className="text-4xl md:text-6xl font-bold mb-8">Ready to explore?</h2>
                <p className="text-xl text-zinc-400 mb-10 max-w-2xl mx-auto">
                    Join thousands of travelers who are discovering the world with Memora.
                </p>
                <Link
                    href="/dashboard"
                    className="inline-block px-10 py-5 text-xl font-bold bg-white text-black rounded-full hover:bg-zinc-200 transition-transform hover:scale-105"
                >
                    Get Started for Free
                </Link>
            </section>

            {/* Footer */}
            <footer className="py-12 px-6 border-t border-white/10 bg-black text-zinc-500 text-sm">
                <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
                    <div className="flex flex-col gap-2">
                        <span className="text-2xl font-bold text-white">Memora</span>
                        <p>Your personal AI travel companion.</p>
                    </div>
                    <div className="flex gap-8">
                        <Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link>
                        <Link href="/terms" className="hover:text-white transition-colors">Terms</Link>
                        <a href="mailto:nabih.ai.agency@gmail.com" className="hover:text-white transition-colors">Contact</a>
                        <a href="https://wa.me/201102481879" target="_blank" rel="noopener noreferrer" className="hover:text-green-400 transition-colors">WhatsApp</a>
                    </div>
                    <p>&copy; {new Date().getFullYear()} Memora Inc.</p>
                </div>
            </footer>
        </div>
    );
}
