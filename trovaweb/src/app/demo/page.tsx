'use client';
import React, { useState } from 'react';

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

            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_BASE || 'http://localhost:8000';
            const response = await fetch(`${backendUrl}/vision/identify_upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}`);
            }

            const data = await response.json();
            setResult(data);
        } catch (err: any) {
            console.error(err);
            setError(err.message || 'Failed to identify image');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-black text-white p-6 font-sans">
            <div className="max-w-2xl mx-auto pt-20">
                <h1 className="text-3xl font-bold mb-8 text-center bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                    Vision Demo
                </h1>

                <div className="bg-zinc-900 rounded-xl p-8 border border-white/10">
                    <div className="mb-6">
                        <label className="block text-sm font-medium text-zinc-400 mb-2">Upload an image</label>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleFileSelect}
                            className="block w-full text-sm text-zinc-400
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-600 file:text-white
                hover:file:bg-blue-700
                cursor-pointer"
                        />
                    </div>

                    {preview && (
                        <div className="mb-6 relative rounded-lg overflow-hidden border border-white/10">
                            <img src={preview} alt="Preview" className="w-full h-auto object-cover max-h-80" />
                        </div>
                    )}

                    <button
                        onClick={handleIdentify}
                        disabled={!selectedFile || loading}
                        className={`w-full py-3 rounded-lg font-bold text-white transition-all
              ${!selectedFile || loading
                                ? 'bg-zinc-700 cursor-not-allowed opacity-50'
                                : 'bg-blue-600 hover:bg-blue-500 hover:scale-[1.02]'}`}
                    >
                        {loading ? 'Analyzing...' : 'Identify Monument'}
                    </button>

                    {error && (
                        <div className="mt-6 p-4 bg-red-900/20 border border-red-500/20 rounded-lg text-red-400">
                            Error: {error}
                        </div>
                    )}

                    {result && (
                        <div className="mt-8 p-6 bg-black rounded-lg border border-white/10">
                            <h3 className="text-xl font-bold mb-4 text-green-400">Result</h3>
                            <div className="space-y-2">
                                <p><span className="text-zinc-500">Identified:</span> <span className="text-white font-semibold">{result.identified_monument}</span></p>
                                <p><span className="text-zinc-500">Confidence:</span> <span className="text-white">{(result.confidence * 100).toFixed(1)}%</span></p>
                                {result.description && (
                                    <p className="text-sm text-zinc-400 mt-2">{result.description}</p>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
