-- =============================================================
-- Migration: 001_pgvector_circulars.sql
-- Purpose  : Enable pgvector and create the circular_embeddings
--            table + similarity-search function used by the
--            CBSE AI/RAG layer.
--
-- Run once in the Supabase SQL editor (or via supabase db push).
-- =============================================================

-- 1. Enable the pgvector extension (requires Supabase pg_vector add-on).
create extension if not exists vector;


-- 2. Create the embeddings table.
--    - content   : the page_content string passed to the LLM.
--    - metadata  : all structured fields (title, category, etc.) as JSON.
--    - embedding : 768-dimensional vector from nomic-embed-text.
create table if not exists circular_embeddings (
    id        bigserial primary key,
    content   text             not null,
    metadata  jsonb            not null default '{}',
    embedding vector(768)
);


-- 3. Create an IVFFlat index to speed up approximate nearest-neighbour
--    search.  Build the index after inserting a reasonable number of rows
--    (at least a few hundred) for best results.
create index if not exists circular_embeddings_embedding_idx
    on circular_embeddings
    using ivfflat (embedding vector_cosine_ops)
    with (lists = 100);


-- 4. Create the RPC function used by LangChain's SupabaseVectorStore.
--    Returns the top-k most similar documents for a given query vector.
create or replace function match_circular_embeddings(
    query_embedding vector(768),
    match_count     int     default 5,
    filter          jsonb   default '{}'
)
returns table (
    id         bigint,
    content    text,
    metadata   jsonb,
    similarity float
)
language plpgsql
as $$
begin
    return query
    select
        circular_embeddings.id,
        circular_embeddings.content,
        circular_embeddings.metadata,
        1 - (circular_embeddings.embedding <=> query_embedding) as similarity
    from circular_embeddings
    where circular_embeddings.metadata @> filter
    order by circular_embeddings.embedding <=> query_embedding
    limit match_count;
end;
$$;


-- 5. (Optional) Enable Row Level Security.
--    Uncomment and adapt these policies once you have authenticated users.
-- alter table circular_embeddings enable row level security;
-- create policy "Public read access"
--     on circular_embeddings for select using (true);
-- create policy "Service role insert"
--     on circular_embeddings for insert
--     with check (auth.role() = 'service_role');
