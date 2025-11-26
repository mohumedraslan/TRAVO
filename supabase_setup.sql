-- Create a table for public profiles if it doesn't exist
create table if not exists public.profiles (
  id uuid references auth.users not null primary key,
  updated_at timestamp with time zone,
  username text unique,
  full_name text,
  avatar_url text,
  website text,
  interests text[],
  trip_dates jsonb,
  language text default 'en',
  constraint username_length check (char_length(username) >= 3)
);

-- Set up Row Level Security (RLS)
alter table public.profiles enable row level security;

-- Create policies only if they don't exist
do $$
begin
    if not exists (select 1 from pg_policies where tablename = 'profiles' and policyname = 'Public profiles are viewable by everyone.') then
        create policy "Public profiles are viewable by everyone." on profiles for select using ( true );
    end if;

    if not exists (select 1 from pg_policies where tablename = 'profiles' and policyname = 'Users can insert their own profile.') then
        create policy "Users can insert their own profile." on profiles for insert with check ( auth.uid() = id );
    end if;

    if not exists (select 1 from pg_policies where tablename = 'profiles' and policyname = 'Users can update own profile.') then
        create policy "Users can update own profile." on profiles for update using ( auth.uid() = id );
    end if;
end
$$;

-- Set up a trigger to automatically create a profile entry when a new user signs up via Supabase Auth
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, full_name, avatar_url, username)
  values (new.id, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url', new.raw_user_meta_data->>'username')
  on conflict (id) do nothing;
  return new;
end;
$$ language plpgsql security definer;

-- Drop trigger if exists to avoid error on recreation
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
