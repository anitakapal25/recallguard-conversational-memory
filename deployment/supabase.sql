-- Dedicated demo table; never imports or modifies existing local memories.
begin;
create table if not exists public.recallguard_memories (
  id uuid primary key,
  owner_id text not null,
  document text not null check (length(document) between 1 and 4000),
  embedding double precision[] not null check (array_length(embedding,1)=384),
  metadata jsonb not null,
  expires_at timestamptz not null,
  check (metadata->>'user_id' = owner_id)
);
create index if not exists recallguard_owner_expiry on public.recallguard_memories(owner_id,expires_at);
alter table public.recallguard_memories enable row level security;
revoke all on public.recallguard_memories from public, anon, authenticated;
grant select, insert, update, delete on public.recallguard_memories to service_role;

create or replace function public.recallguard_list(p_owner text, p_ids uuid[] default null)
returns table(id uuid, document text, metadata jsonb)
language sql security invoker set search_path = '' as $$
  select m.id,m.document,m.metadata from public.recallguard_memories m
  where m.owner_id=p_owner and (p_ids is null or m.id=any(p_ids)) order by m.id limit 500;
$$;

create or replace function public.recallguard_write(p_id uuid,p_owner text,p_document text,
  p_embedding double precision[],p_metadata jsonb,p_update boolean default false)
returns boolean language plpgsql security invoker set search_path = '' as $$
begin
  if coalesce(p_owner,'')='' or p_metadata->>'user_id' is distinct from p_owner then
    raise exception 'Invalid owner';
  end if;
  perform pg_catalog.pg_advisory_xact_lock(728416320);
  if p_update then
    update public.recallguard_memories set document=p_document,embedding=p_embedding,metadata=p_metadata
      where id=p_id and owner_id=p_owner and expires_at>now();
    if not found then raise exception 'Record unavailable'; end if;
  else
    delete from public.recallguard_memories where expires_at<=now();
    if (select count(*) from public.recallguard_memories where owner_id=p_owner)>=500
      or (select count(*) from public.recallguard_memories)>=5000 then
      raise exception 'Demo storage quota exceeded';
    end if;
    if (p_metadata->>'expires_at')::timestamptz > now()+interval '7 days 1 minute'
      or (p_metadata->>'expires_at')::timestamptz <=now() then raise exception 'Invalid retention'; end if;
    insert into public.recallguard_memories values
      (p_id,p_owner,p_document,p_embedding,p_metadata,(p_metadata->>'expires_at')::timestamptz);
  end if;
  return true;
end; $$;

create or replace function public.recallguard_delete(p_owner text,p_ids uuid[])
returns integer language plpgsql security invoker set search_path = '' as $$
declare removed integer;
begin
  delete from public.recallguard_memories where owner_id=p_owner and id=any(p_ids);
  get diagnostics removed = row_count;
  return removed;
end; $$;

create or replace function public.recallguard_search(p_owner text,p_ids uuid[],
  p_embedding double precision[],p_limit integer)
returns table(id uuid,document text,metadata jsonb,distance double precision)
language sql security invoker set search_path = '' as $$
  select m.id,m.document,m.metadata,
    (select sum((v.x-v.y)*(v.x-v.y)) from unnest(m.embedding,p_embedding) as v(x,y)) as distance
  from public.recallguard_memories m
  where m.owner_id=p_owner and m.id=any(p_ids) and m.expires_at>now()
    and array_length(p_embedding,1)=384
  order by distance,m.id limit greatest(1,least(p_limit,100));
$$;

create or replace function public.recallguard_ready()
returns bigint language sql security invoker set search_path = '' as $$
  select count(*) from public.recallguard_memories;
$$;

revoke all on function public.recallguard_list(text,uuid[]) from public,anon,authenticated;
revoke all on function public.recallguard_write(uuid,text,text,double precision[],jsonb,boolean) from public,anon,authenticated;
revoke all on function public.recallguard_delete(text,uuid[]) from public,anon,authenticated;
revoke all on function public.recallguard_search(text,uuid[],double precision[],integer) from public,anon,authenticated;
revoke all on function public.recallguard_ready() from public,anon,authenticated;
grant execute on function public.recallguard_list(text,uuid[]) to service_role;
grant execute on function public.recallguard_write(uuid,text,text,double precision[],jsonb,boolean) to service_role;
grant execute on function public.recallguard_delete(text,uuid[]) to service_role;
grant execute on function public.recallguard_search(text,uuid[],double precision[],integer) to service_role;
grant execute on function public.recallguard_ready() to service_role;
commit;
