-- Keep tem o próprio banco. Não usa as tabelas da Avalon.
-- Uma empresa pode ter vários domínios. A pessoa só lê o painel
-- depois de confirmar o e-mail: a conta do Auth e a membership ficam OK.

create table public.keep_companies (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz not null default now()
);

create table public.keep_domains (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references public.keep_companies(id) on delete cascade,
  host text not null,
  created_at timestamptz not null default now(),
  unique (host)
);

create table public.keep_members (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references public.keep_companies(id) on delete cascade,
  user_id uuid references auth.users(id) on delete cascade,
  email text not null,
  status text not null default 'pending' check (status in ('pending', 'ok')),
  email_confirmed_at timestamptz,
  created_at timestamptz not null default now(),
  unique (company_id, email)
);

create table public.keep_collaborations (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references public.keep_companies(id) on delete cascade,
  guest_email text not null,
  guest_user_id uuid references auth.users(id) on delete set null,
  invite_token text not null default encode(extensions.gen_random_bytes(16), 'hex'),
  status text not null default 'pending' check (status in ('pending', 'accepted', 'revoked')),
  accepted_at timestamptz,
  created_at timestamptz not null default now()
);

create unique index keep_collaborations_one_open_email
  on public.keep_collaborations (company_id, guest_email)
  where status <> 'revoked';

create table public.keep_properties (
  id uuid primary key default gen_random_uuid(),
  domain_id uuid not null references public.keep_domains(id) on delete cascade,
  provider text not null check (provider in ('search_console', 'google_analytics')),
  external_id text not null,
  created_at timestamptz not null default now(),
  unique (domain_id, provider)
);

create table public.keep_connection_secrets (
  id uuid primary key default gen_random_uuid(),
  company_id uuid not null references public.keep_companies(id) on delete cascade,
  refresh_token text not null,
  created_at timestamptz not null default now()
);

create table public.keep_pages (
  id uuid primary key default gen_random_uuid(),
  domain_id uuid not null references public.keep_domains(id) on delete cascade,
  url text not null,
  title text not null default '',
  published_on date,
  unique (domain_id, url)
);

create table public.keep_metrics (
  id uuid primary key default gen_random_uuid(),
  page_id uuid not null references public.keep_pages(id) on delete cascade,
  month date not null,
  gsc_clicks integer not null default 0,
  gsc_position numeric,
  ga_landing_sessions integer not null default 0,
  unique (page_id, month)
);

alter table public.keep_companies enable row level security;
alter table public.keep_domains enable row level security;
alter table public.keep_members enable row level security;
alter table public.keep_collaborations enable row level security;
alter table public.keep_properties enable row level security;
alter table public.keep_pages enable row level security;
alter table public.keep_metrics enable row level security;
alter table public.keep_connection_secrets enable row level security;

revoke all on public.keep_connection_secrets from public, anon, authenticated;

create or replace function public.keep_email_is_confirmed()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from auth.users
    where id = auth.uid()
      and email_confirmed_at is not null
  );
$$;

create or replace function public.keep_company_ids()
returns setof uuid
language sql
stable
security definer
set search_path = public
as $$
  select company_id
  from public.keep_members
  where user_id = auth.uid()
    and status = 'ok'
    and email_confirmed_at is not null
  union
  select company_id
  from public.keep_collaborations
  where guest_user_id = auth.uid()
    and status = 'accepted'
    and public.keep_email_is_confirmed();
$$;

create or replace function public.keep_mark_email_ok()
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  _email text;
  _confirmed timestamptz;
begin
  select email, email_confirmed_at
    into _email, _confirmed
  from auth.users
  where id = auth.uid();

  if _confirmed is null then
    raise exception 'Confirme o e-mail antes de entrar no Keep.';
  end if;

  update public.keep_members
     set user_id = auth.uid(),
         status = 'ok',
         email_confirmed_at = _confirmed
   where lower(email) = lower(_email);

  -- A primeira pessoa confirmada vira membro das empresas já criadas.
  -- Quem chega depois só entra por convite.
  if not exists (
    select 1 from public.keep_members where status = 'ok'
  ) then
    insert into public.keep_members (company_id, user_id, email, status, email_confirmed_at)
    select id, auth.uid(), _email, 'ok', _confirmed
    from public.keep_companies;
  end if;

  update public.keep_collaborations
     set guest_user_id = auth.uid(),
         status = 'accepted',
         accepted_at = coalesce(accepted_at, now())
   where lower(guest_email) = lower(_email)
     and status = 'pending';
end;
$$;

revoke all on function public.keep_mark_email_ok() from public, anon;
grant execute on function public.keep_mark_email_ok() to authenticated;

grant select on public.keep_companies, public.keep_domains, public.keep_pages, public.keep_metrics, public.keep_properties to authenticated;
grant select, insert, update on public.keep_members to authenticated;
grant select, insert, update on public.keep_collaborations to authenticated;

create policy keep_companies_read on public.keep_companies
  for select to authenticated
  using (id in (select public.keep_company_ids()));

create policy keep_domains_read on public.keep_domains
  for select to authenticated
  using (company_id in (select public.keep_company_ids()));

create policy keep_pages_read on public.keep_pages
  for select to authenticated
  using (domain_id in (
    select id from public.keep_domains
    where company_id in (select public.keep_company_ids())
  ));

create policy keep_metrics_read on public.keep_metrics
  for select to authenticated
  using (page_id in (
    select p.id
    from public.keep_pages p
    join public.keep_domains d on d.id = p.domain_id
    where d.company_id in (select public.keep_company_ids())
  ));

create policy keep_properties_read on public.keep_properties
  for select to authenticated
  using (domain_id in (
    select id from public.keep_domains
    where company_id in (select public.keep_company_ids())
  ));

create policy keep_members_read on public.keep_members
  for select to authenticated
  using (
    user_id = auth.uid()
    or company_id in (
      select company_id from public.keep_members
      where user_id = auth.uid() and status = 'ok'
    )
  );

create policy keep_collaborations_owner on public.keep_collaborations
  for all to authenticated
  using (company_id in (
    select company_id from public.keep_members
    where user_id = auth.uid() and status = 'ok'
  ))
  with check (company_id in (
    select company_id from public.keep_members
    where user_id = auth.uid() and status = 'ok'
  ));

create policy keep_collaborations_guest_read on public.keep_collaborations
  for select to authenticated
  using (guest_user_id = auth.uid() or lower(guest_email) = lower(coalesce(auth.email(), '')));

insert into public.keep_companies (name) values ('Avalon'), ('Adfert');

insert into public.keep_domains (company_id, host)
select id, 'avalonx.co' from public.keep_companies where name = 'Avalon';

insert into public.keep_domains (company_id, host)
select id, host
from public.keep_companies
cross join (values ('adfert.com.br'), ('intrivia.com.br')) as domains(host)
where name = 'Adfert';
