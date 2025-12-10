"use client";

import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";

export default function PrivacyPage() {
    return (
        <div className="min-h-screen bg-black text-white font-sans">
            <Navbar />
            <main className="mx-auto max-w-4xl px-6 py-32">
                <h1 className="mb-8 text-4xl font-bold">Privacy Policy</h1>
                <div className="prose prose-invert max-w-none text-zinc-400">
                    <p>Last updated: December 2025</p>
                    <p>
                        At Memora, we take your privacy seriously. This Privacy Policy explains how we collect, use, and protect your personal information when you use our AI-powered travel companion services.
                    </p>
                    <h3>1. Information We Collect</h3>
                    <p>
                        We collect information you provide directly to us, such as when you create an account, plan a trip, or contact us. This may include your name, email address, and travel preferences.
                    </p>
                    <h3>2. How We Use Your Information</h3>
                    <p>
                        We use your information to provide personalized travel recommendations, improve our AI models (anonymized), and communicate with you about your account.
                    </p>
                    <h3>3. Data Security</h3>
                    <p>
                        We implement industry-standard security measures to protect your data. Your personal travel data is encrypted and never shared with third parties without your consent.
                    </p>
                </div>
            </main>
            <Footer />
        </div>
    );
}
