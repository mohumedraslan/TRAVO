'use client';
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
        // Fetch destinations to compute count
        const destinationsRes = await client.get('/recommendations/destinations?limit=50');
        const destinations = Array.isArray(destinationsRes.data) ? destinationsRes.data : [];
        const destinationsCount = destinations.length;

        // Fetch attractions for the first destination (if available) to compute count
        let attractionsCount = 0;
        if (destinations.length > 0 && destinations[0]?.id) {
          const destinationId = destinations[0].id as string;
          try {
            const attractionsRes = await client.get(`/recommendations/destinations/${destinationId}/attractions?limit=50`);
            const attractions = Array.isArray(attractionsRes.data) ? attractionsRes.data : [];
            attractionsCount = attractions.length;
          } catch (innerErr) {
            console.error('Failed to fetch attractions for destination', destinationId, innerErr);
          }
        }

        // Users count placeholder until endpoint exists
        const usersCount = 0;

        setSummary({ destinationsCount, attractionsCount, usersCount });
      } catch (err) {
        console.error('Failed to fetch dashboard summary', err);
        setSummary({ destinationsCount: 0, attractionsCount: 0, usersCount: 0 });
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