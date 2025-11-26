-- Migration for TRAVO Pivot: Automatic Travel Diary

-- 1. Create Trips table
create table if not exists public.trips (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users not null,
  title text,
  start_time timestamp with time zone default now(),
  end_time timestamp with time zone,
  status text default 'active', -- 'active', 'completed'
  created_at timestamp with time zone default now()
);

-- 2. Create Trip Places table (Locations visited)
create table if not exists public.trip_places (
  id uuid default gen_random_uuid() primary key,
  trip_id uuid references public.trips not null,
  place_name text not null,
  gps_lat double precision,
  gps_lon double precision,
  address text,
  created_at timestamp with time zone default now()
);

-- 3. Create Trip Photos table (Photos taken at places)
create table if not exists public.trip_photos (
  id uuid default gen_random_uuid() primary key,
  trip_place_id uuid references public.trip_places not null,
  photo_url text not null,
  caption text,
  created_at timestamp with time zone default now()
);

-- 4. Enable RLS
alter table public.trips enable row level security;
alter table public.trip_places enable row level security;
alter table public.trip_photos enable row level security;

-- 5. Create Policies (Simple: Users can manage their own data)
create policy "Users can manage their own trips" on public.trips
  for all using (auth.uid() = user_id);

create policy "Users can manage their own trip places" on public.trip_places
  for all using (
    exists (select 1 from public.trips where id = trip_places.trip_id and user_id = auth.uid())
  );

create policy "Users can manage their own trip photos" on public.trip_photos
  for all using (
    exists (
      select 1 from public.trip_places
      join public.trips on trips.id = trip_places.trip_id
      where trip_places.id = trip_photos.trip_place_id and trips.user_id = auth.uid()
    )
  );
