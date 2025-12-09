"use client";

import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";

export default function TermsPage() {
    return (
        <div className="min-h-screen bg-black text-white font-sans">
            <Navbar />
            <main className="mx-auto max-w-4xl px-6 py-32">
                <h1 className="mb-8 text-4xl font-bold">Terms of Service</h1>
                <div className="prose prose-invert max-w-none text-zinc-400">
                    <p>Last updated: December 2025</p>
                    <p>
                        Please read these Terms of Service carefully before using the TRAVO platform.
                    </p>
                    <h3>1. Acceptance of Terms</h3>
                    <p>
                        By accessing or using TRAVO, you agree to be bound by these Terms. If you disagree with any part of the terms, you may not access the service.
                    </p>
                    <h3>2. AI Accuracy Disclaimer</h3>
                    <p>
                        TRAVO uses artificial intelligence to provide recommendations and identify monuments. While we strive for accuracy, AI outputs may occasionally be incorrect. Always verify critical travel information.
                    </p>
                    <h3>3. User Accounts</h3>
                    <p>
                        You are responsible for safeguarding the password that you use to access the service and for any activities or actions under your password.
                    </p>
                </div>
            </main>
            <Footer />
        </div>
    );
}
