-- CBSE circulars schema.
-- This migration intentionally creates only the circulars table.

create extension if not exists pgcrypto;

create table public.circulars (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text,
  content text,
  category text not null default 'general',
  target_audience text[] not null default '{}',
  publish_date timestamptz not null default now(),
  document_url text,
  source_url text,
  created_at timestamptz not null default now()
);

create index circulars_publish_date_idx on public.circulars (publish_date desc);
create index circulars_category_idx on public.circulars (category);

create table public.news (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text,
  category text not null default 'general',
  publish_date timestamptz not null default now(),
  source_url text,
  created_at timestamptz not null default now()
);

create index news_publish_date_idx on public.news (publish_date desc);
create index news_category_idx on public.news (category);

create table public.important_dates (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text,
  event_date date not null,
  category text not null default 'general',
  target_audience text[] not null default '{}',
  source_url text,
  created_at timestamptz not null default now()
);

create index important_dates_event_date_idx on public.important_dates (event_date);
create index important_dates_category_idx on public.important_dates (category);

create table public.services (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text,
  category text not null default 'general',
  target_audience text[] not null default '{}',
  url text not null,
  icon text,
  created_at timestamptz not null default now()
);

create index services_category_idx on public.services (category);
create index services_target_audience_idx on public.services using gin (target_audience);

-- Application profile records only; authentication will be added separately.
create table public.users (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text not null,
  role text not null default 'student',
  class text,
  school text,
  created_at timestamptz not null default now()
);

create index users_email_idx on public.users (email);
create index users_role_idx on public.users (role);

create table public.notifications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  title text not null,
  message text not null,
  category text not null default 'general',
  priority text not null default 'normal',
  read boolean not null default false,
  created_at timestamptz not null default now()
);

create index notifications_user_id_idx on public.notifications (user_id);
create index notifications_created_at_idx on public.notifications (created_at desc);
create index notifications_read_idx on public.notifications (read);
