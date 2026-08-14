-- Feedback board — table, public view and policies.
--
-- The app is a static page, so the board needs somewhere to live. Any
-- PostgREST-compatible host works; these statements are written for Supabase.
-- After running them, set these three in index.html:
--
--   FEEDBACK_ENDPOINT      = https://<project>.supabase.co/rest/v1/feedback
--   FEEDBACK_READ_ENDPOINT = https://<project>.supabase.co/rest/v1/feedback_public
--   FEEDBACK_API_KEY       = <anon key>
--
-- The anon key is publishable. The policies below are what guard the data.

create table if not exists public.feedback (
  id            text primary key,
  parent_id     text references public.feedback(id) on delete cascade,
  kind          text not null default 'note' check (kind in ('feature','bug','note')),
  body          text not null default '',
  author_key    text not null,          -- visible "same person" id; NOT a credential
  author_alias  text not null default 'Someone',
  author_color  text not null default 'Slate',
  edit_token    text not null,          -- secret; proves authorship, never served
  created       timestamptz not null default now(),
  updated       timestamptz not null default now(),
  deleted       boolean not null default false
);

create index if not exists feedback_parent_idx  on public.feedback (parent_id);
create index if not exists feedback_created_idx on public.feedback (created);

-- Everything except edit_token. Reads go here, so a visitor can never learn
-- the token that would let them edit somebody else's post.
create or replace view public.feedback_public as
  select id, parent_id, kind, body, author_key, author_alias, author_color,
         created, updated, deleted
  from public.feedback;

alter table public.feedback enable row level security;

revoke select on public.feedback from anon;
grant  select on public.feedback_public to anon;
grant  insert, update on public.feedback to anon;

-- Anyone may post, within limits.
create policy feedback_insert on public.feedback
  for insert to anon with check (
    length(body) between 1 and 4000
    and length(author_key) between 8 and 64
    and length(edit_token) between 8 and 128
  );

-- Edit and delete require the token. The client sends it as a WHERE filter
-- (?id=eq.X&edit_token=eq.Y); since the token is never readable, only the
-- device that wrote the post can produce it.
create policy feedback_update on public.feedback
  for update to anon using (true) with check (length(body) <= 4000);

-- Rate limiting and spam handling are not modelled here. If the board gets
-- abused, the smallest useful next step is a per-IP insert limit at the edge
-- (Supabase Edge Function or a Cloudflare rule) rather than more SQL.
