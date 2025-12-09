"use client";

import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";

export default function ContactPage() {
    return (
        <div className="min-h-screen bg-black text-white font-sans">
            <Navbar />
            <main className="mx-auto max-w-4xl px-6 py-32">
                <h1 className="mb-4 text-4xl font-bold">Contact Us</h1>
                <p className="mb-12 text-zinc-400">
                    Have questions or feedback? We'd love to hear from you.
                </p>

                <div className="grid gap-12 md:grid-cols-2">
                    <div>
                        <h2 className="mb-6 text-2xl font-semibold">Get in Touch</h2>
                        <div className="space-y-6 text-zinc-300">
                            <div className="flex items-center gap-4">
                                <span className="text-2xl">📧</span>
                                <div>
                                    <div className="font-semibold text-white">Email</div>
                                    <div>support@travo.ai</div>
                                </div>
                            </div>
                            <div className="flex items-center gap-4">
                                <span className="text-2xl">📍</span>
                                <div>
                                    <div className="font-semibold text-white">Office</div>
                                    <div>123 AI Boulevard, Tech City</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <form className="space-y-4 rounded-xl border border-white/10 bg-white/5 p-6">
                        <div>
                            <label className="mb-2 block text-sm font-medium">Name</label>
                            <input type="text" className="w-full rounded-lg border border-white/10 bg-black/50 px-4 py-2 focus:border-blue-500 focus:outline-none" placeholder="Your name" />
                        </div>
                        <div>
                            <label className="mb-2 block text-sm font-medium">Email</label>
                            <input type="email" className="w-full rounded-lg border border-white/10 bg-black/50 px-4 py-2 focus:border-blue-500 focus:outline-none" placeholder="you@example.com" />
                        </div>
                        <div>
                            <label className="mb-2 block text-sm font-medium">Message</label>
                            <textarea rows={4} className="w-full rounded-lg border border-white/10 bg-black/50 px-4 py-2 focus:border-blue-500 focus:outline-none" placeholder="How can we help?" />
                        </div>
                        <button type="submit" className="w-full rounded-lg bg-white py-2 font-medium text-black transition hover:bg-zinc-200">
                            Send Message
                        </button>
                    </form>
                </div>
            </main>
            <Footer />
        </div>
    );
}
