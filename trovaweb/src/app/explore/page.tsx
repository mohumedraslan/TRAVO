import React, { useEffect, useState } from 'react';
import client from '@/api/client';
import Card from '@/components/shared/Card';

interface Item {
  id: string;
  name: string;
  description?: string;
}

export default function ExplorePage() {
  const [destinations, setDestinations] = useState<Item[]>([]);
  const [attractions, setAttractions] = useState<Item[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const destRes = await client.get('/recommendations/destinations');
        const attrRes = await client.get('/recommendations/destinations/1/attractions');
        setDestinations(destRes.data?.items || []);
        setAttractions(attrRes.data?.items || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-5xl px-6 py-10">
        <h1 className="text-3xl font-bold">Explore</h1>
        <p className="text-zinc-600 dark:text-zinc-400">Discover destinations and attractions</p>

        {loading && <p className="mt-6">Loading...</p>}

        {!loading && (
          <div className="mt-8 grid grid-cols-1 gap-4 md:grid-cols-2">
            <div>
              <h2 className="mb-2 text-xl font-semibold">Recommended Destinations</h2>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                {destinations.map((d) => (
                  <Card key={d.id} title={d.name} description={d.description || 'Beautiful destination'} />
                ))}
              </div>
            </div>
            <div>
              <h2 className="mb-2 text-xl font-semibold">Attractions</h2>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                {attractions.map((a) => (
                  <Card key={a.id} title={a.name} description={a.description || 'Top attraction'} />
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}