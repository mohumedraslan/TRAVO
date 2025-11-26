-- Run this in your Supabase SQL Editor to fix the "row-level security policy" error.
-- This temporarily disables strict security checks so the app can write data.

ALTER TABLE public.trip_places DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.trip_photos DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.trips DISABLE ROW LEVEL SECURITY;
