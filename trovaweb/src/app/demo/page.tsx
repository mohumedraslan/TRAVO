'use client';

import React, { useState } from 'react';
import axios from 'axios';

export default function DemoPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  // Allow overriding the backend host via environment variable for device/emulator testing.
  // Example for Android emulator: set NEXT_PUBLIC_BACKEND_BASE=http://10.0.2.2:8000/api
  const BACKEND_BASE = process.env.NEXT_PUBLIC_BACKEND_BASE || 'http://127.0.0.1:8000/api';
  const IDENTIFY_PATH = '/vision/identify';

  const onFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0] || null;
    setFile(f);
    setError(null);
    setResult(null);
    if (f) {
      const reader = new FileReader();
      reader.onload = () => setImagePreview(reader.result as string);
      reader.readAsDataURL(f);
    } else {
      setImagePreview(null);
    }
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError('Please select an image first.');
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const form = new FormData();
      form.append('image', file);

      const response = await axios.post(IDENTIFY_PATH, form, {
        baseURL: BACKEND_BASE,
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResult(response.data);
    } catch (err: any) {
      console.error('Identify request failed:', err);
      const message = err?.response?.data?.detail || err?.message || 'Request failed';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black text-zinc-900 dark:text-zinc-100">
      <div className="mx-auto max-w-3xl px-6 py-10">
        <h1 className="text-3xl font-bold">Monument Identification Demo</h1>
        <p className="mt-2 text-zinc-600 dark:text-zinc-400">Upload an image of a monument to identify it using the backend service.</p>

        <form onSubmit={onSubmit} className="mt-6 space-y-4">
          <div>
            <input type="file" accept="image/*" onChange={onFileChange} className="block w-full text-sm" />
            {imagePreview && (
              <div className="mt-3">
                <img src={imagePreview} alt="Preview" className="max-h-64 rounded-md border border-zinc-200 dark:border-zinc-800" />
              </div>
            )}
          </div>
          <button
            type="submit"
            disabled={loading}
            className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Identifying…' : 'Identify Monument'}
          </button>
        </form>

        {error && (
          <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700 dark:border-red-800 dark:bg-red-900/30 dark:text-red-400">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-6 rounded-lg border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <h2 className="text-xl font-semibold">Result</h2>
            <pre className="mt-2 overflow-auto text-sm"><code>{JSON.stringify(result, null, 2)}</code></pre>
          </div>
        )}
      </div>
    </div>
  );
}
