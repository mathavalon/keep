-- Contatos da homepage. Quem ainda não tem conta pode deixar nome, e-mail e site.
-- A lista não fica legível no navegador.

create table public.keep_leads (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text not null,
  site text,
  created_at timestamptz not null default now(),
  check (char_length(name) between 2 and 80),
  check (email ~* '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
  check (site is null or char_length(site) <= 200)
);

alter table public.keep_leads enable row level security;

revoke all on public.keep_leads from public, anon, authenticated;
grant insert on public.keep_leads to anon, authenticated;

create policy keep_leads_insert on public.keep_leads
  for insert to anon, authenticated
  with check (true);
