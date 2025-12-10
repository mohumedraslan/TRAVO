"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
    const pathname = usePathname();

    const isActive = (path: string) => pathname === path;

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-black/50 backdrop-blur-xl">
            <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
                <Link href="/" className="text-2xl font-bold tracking-tighter text-white">
                    Memora
                </Link>
                <div className="hidden gap-8 md:flex">
                    {[
                        { name: "Explore", href: "/explore" },
                        { name: "Dashboard", href: "/dashboard" },
                        { name: "About", href: "/about" },
                        { name: "Contact", href: "/contact" },
                    ].map((link) => (
                        <Link
                            key={link.href}
                            href={link.href}
                            className={`text-sm font-medium transition-colors hover:text-white ${isActive(link.href) ? "text-white" : "text-zinc-400"
                                }`}
                        >
                            {link.name}
                        </Link>
                    ))}
                </div>
                <div className="flex gap-4">
                    <a
                        href="http://159.138.92.94:8000/docs"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="rounded-full bg-white/10 px-4 py-2 text-sm font-medium text-white transition hover:bg-white/20"
                    >
                        API Docs
                    </a>
                </div>
            </div>
        </nav>
    );
}
