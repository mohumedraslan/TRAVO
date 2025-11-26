-- Drop existing policies to avoid conflicts and errors
drop policy if exists "Allow authenticated uploads to trip_photos" on storage.objects;
drop policy if exists "Allow public viewing of trip_photos" on storage.objects;
drop policy if exists "Allow individual update own photos" on storage.objects;
drop policy if exists "Allow individual delete own photos" on storage.objects;

-- Policy to allow uploads to 'trip_photos' for authenticated users
create policy "Allow authenticated uploads to trip_photos"
on storage.objects
for insert
to authenticated
with check ( bucket_id = 'trip_photos' );

-- Policy to allow viewing photos (if not covered by Public bucket setting)
create policy "Allow public viewing of trip_photos"
on storage.objects
for select
to public
using ( bucket_id = 'trip_photos' );

-- Policy to allow updates (optional, for replacing photos)
create policy "Allow individual update own photos"
on storage.objects
for update
to authenticated
using ( bucket_id = 'trip_photos' and owner = auth.uid() );

-- Policy to allow deletion
create policy "Allow individual delete own photos"
on storage.objects
for delete
to authenticated
using ( bucket_id = 'trip_photos' and owner = auth.uid() );
