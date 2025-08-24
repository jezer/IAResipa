-- SQL Script para criação de tabelas no Supabase
-- Gerado automaticamente com base em 03.src/resipa/A_db/db_00_supabase_schema_config.py
drop table if exists public.reservas ;
drop table if exists public.lista_espera; 
drop table if exists public.recursos ;
drop table if exists public.cadastro_pessoas_fisica;


-- Tabela: cadastro_pessoas_fisica
CREATE TABLE IF NOT EXISTS public.cadastro_pessoas_fisica (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number TEXT UNIQUE,
    name TEXT,
    email TEXT UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela: recursos
CREATE TABLE IF NOT EXISTS public.recursos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE,
    type TEXT,
    capacity INTEGER,
    location TEXT,
    is_available BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela: reservas
CREATE TABLE IF NOT EXISTS public.reservas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    resource_id UUID,
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    status TEXT,
    pix_txid TEXT UNIQUE,
    amount NUMERIC(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Adicionar chaves estrangeiras se houver tabelas de referência
    FOREIGN KEY (user_id) REFERENCES public.cadastro_pessoas_fisica(id),
    FOREIGN KEY (resource_id) REFERENCES public.recursos(id)
);

-- Tabela: lista_espera
CREATE TABLE IF NOT EXISTS public.lista_espera (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    resource_id UUID,
    requested_time TIMESTAMP WITH TIME ZONE,
    status TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Adicionar chaves estrangeiras se houver tabelas de referência
    FOREIGN KEY (user_id) REFERENCES public.cadastro_pessoas_fisica(id),
    FOREIGN KEY (resource_id) REFERENCES public.recursos(id)
);
