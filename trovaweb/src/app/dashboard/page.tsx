import React, { useEffect, useState } from 'react';
import client from '@/api/client';

interface Summary {
  destinationsCount: number;
  attractionsCount: number;
  usersCount: number;
}

export default function DashboardPage() {
  const [summary, setSummary] = useState<Summary | null>(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const res = await client.get('/analytics/summary');
        setSummary(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchSummary();
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-zinc-600 dark:text-zinc-400">Overview of system metrics</p>

        {summary ? (
          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
              <h3 className="text-lg font-semibold">Destinations</h3>
              <p className="text-2xl">{summary.destinationsCount}</p>
            </div>
            <div className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
              <h3 className="text-lg font-semibold">Attractions</h3>
              <p className="text-2xl">{summary.attractionsCount}</p>
            </div>
            <div className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
              <h3 className="text-lg font-semibold">Users</h3>
              <p className="text-2xl">{summary.usersCount}</p>
            </div>
          </div>
        ) : (
          <p className="mt-6">Loading metrics...</p>
        )}
      </div>
    </div>
  );
}