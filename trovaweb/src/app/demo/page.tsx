'use client';
import React, { useState } from 'react';
import Link from 'next/link';

export default function DemoPage() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setResult(null);
            setError(null);
        }
    };

    const handleIdentify = async () => {
        if (!selectedFile) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const formData = new FormData();
            formData.append('image', selectedFile);

            // Use the backend on the same host, or fallback to localhost
            const host = typeof window !== 'undefined' ? window.location.hostname : 'localhost';
            const backendUrl = host === 'localhost' || host === '127.0.0.1'
                ? 'http://localhost:8000/api'
                : `http://${host}:8000/api`;

            const response = await fetch(`${backendUrl}/vision/identify`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server error ${response.status}: ${errorText}`);
            }

            const data = await response.json();
            setResult(data);
        } catch (err: any) {
            console.error('Vision API Error:', err);
            setError(err.message || 'Failed to identify image');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-black text-white font-sans">
            {/* Navigation */}
            <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 backdrop-blur-md bg-black/50 border-b border-white/10">
                <Link href="/landing" className="text-2xl font-bold tracking-tighter bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                    Memora
                </Link>
                <Link href="/dashboard" className="px-4 py-2 text-sm font-semibold bg-white text-black rounded-full hover:bg-zinc-200 transition-colors">
                    Dashboard
                </Link>
            </nav>

            <div className="max-w-3xl mx-auto px-6 pt-28 pb-20">
                <div className="text-center mb-12">
                    <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                        AI Vision Demo
                    </h1>
                    <p className="text-xl text-zinc-400">
                        Upload a photo of any monument and our AI will identify it instantly
                    </p>
                </div>

                <div className="bg-zinc-900/50 rounded-2xl p-8 border border-white/10 backdrop-blur-sm">
                    {/* Upload Area */}
                    <div className="mb-8">
                        <label className="block text-sm font-medium text-zinc-400 mb-3">
                            Select an image
                        </label>
                        <div className="relative">
                            <input
                                type="file"
                                accept="image/*"
                                onChange={handleFileSelect}
                                className="block w-full text-sm text-zinc-400
                                    file:mr-4 file:py-3 file:px-6
                                    file:rounded-full file:border-0
                                    file:text-sm file:font-semibold
                                    file:bg-gradient-to-r file:from-blue-500 file:to-purple-500 file:text-white
                                    hover:file:opacity-90
                                    cursor-pointer"
                            />
                        </div>
                    </div>

                    {/* Preview */}
                    {preview && (
                        <div className="mb-8 relative rounded-xl overflow-hidden border border-white/10">
                            <img src={preview} alt="Preview" className="w-full h-auto object-cover max-h-96" />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent pointer-events-none" />
                        </div>
                    )}

                    {/* Identify Button */}
                    <button
                        onClick={handleIdentify}
                        disabled={!selectedFile || loading}
                        className={`w-full py-4 rounded-xl font-bold text-lg transition-all
                            ${!selectedFile || loading
                                ? 'bg-zinc-700 cursor-not-allowed opacity-50'
                                : 'bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 hover:scale-[1.02] active:scale-[0.98]'}`}
                    >
                        {loading ? (
                            <span className="flex items-center justify-center gap-2">
                                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                </svg>
                                Analyzing with AI...
                            </span>
                        ) : (
                            '🔍 Identify Monument'
                        )}
                    </button>

                    {/* Error */}
                    {error && (
                        <div className="mt-6 p-4 bg-red-900/30 border border-red-500/30 rounded-xl text-red-400">
                            <p className="font-medium">Error</p>
                            <p className="text-sm mt-1">{error}</p>
                        </div>
                    )}

                    {/* Results */}
                    {result && (
                        <div className="mt-8 p-6 bg-gradient-to-br from-green-900/30 to-blue-900/30 rounded-xl border border-green-500/20">
                            <div className="flex items-start gap-4">
                                <div className="text-4xl">🏛️</div>
                                <div className="flex-1">
                                    <h3 className="text-2xl font-bold text-white mb-2">
                                        {result.identified_monument}
                                    </h3>
                                    <div className="flex items-center gap-2 mb-3">
                                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${result.confidence >= 0.7
                                            ? 'bg-green-500/20 text-green-400'
                                            : 'bg-yellow-500/20 text-yellow-400'
                                            }`}>
                                            {(result.confidence * 100).toFixed(0)}% Confidence
                                        </span>
                                        {result.location && (
                                            <span className="text-zinc-400 text-sm">📍 {result.location}</span>
                                        )}
                                    </div>
                                    {result.description && (
                                        <p className="text-zinc-300 mb-3">{result.description}</p>
                                    )}
                                    {result.fun_fact && (
                                        <p className="text-sm text-blue-400 italic">💡 {result.fun_fact}</p>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* CTA */}
                <div className="text-center mt-12">
                    <p className="text-zinc-500 mb-4">Want the full experience?</p>
                    <Link
                        href="/dashboard"
                        className="inline-block px-8 py-3 bg-white text-black font-bold rounded-full hover:bg-zinc-200 transition-all hover:scale-105"
                    >
                        Get Started Free →
                    </Link>
                </div>
            </div>
        </div>
    );
}
