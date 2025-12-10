import Link from "next/link";

export default function Footer() {
    return (
        <footer className="border-t border-white/10 bg-black py-12 text-zinc-400">
            <div className="mx-auto max-w-7xl px-6">
                <div className="grid gap-8 md:grid-cols-4">
                    <div>
                        <h3 className="mb-4 text-lg font-bold text-white">Memora</h3>
                        <p className="text-sm">
                            Your AI-Powered Travel Companion. Integrating machine learning to enhance your travel experience.
                        </p>
                    </div>
                    <div>
                        <h4 className="mb-4 text-sm font-semibold text-white">Product</h4>
                        <ul className="space-y-2 text-sm">
                            <li><Link href="/explore" className="hover:text-white">Explore</Link></li>
                            <li><Link href="/dashboard" className="hover:text-white">Dashboard</Link></li>
                            <li><Link href="/features" className="hover:text-white">Features</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h4 className="mb-4 text-sm font-semibold text-white">Legal</h4>
                        <ul className="space-y-2 text-sm">
                            <li><Link href="/privacy" className="hover:text-white">Privacy Policy</Link></li>
                            <li><Link href="/terms" className="hover:text-white">Terms of Service</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h4 className="mb-4 text-sm font-semibold text-white">Connect</h4>
                        <ul className="space-y-2 text-sm">
                            <li><Link href="/contact" className="hover:text-white">Contact Us</Link></li>
                            <li><a href="https://github.com/mohumedraslan/TRAVO" target="_blank" rel="noopener noreferrer" className="hover:text-white">GitHub</a></li>
                        </ul>
                    </div>
                </div>
                <div className="mt-12 border-t border-white/10 pt-8 text-center text-xs">
                    © {new Date().getFullYear()} Memora. All rights reserved.
                </div>
            </div>
        </footer>
    );
}
