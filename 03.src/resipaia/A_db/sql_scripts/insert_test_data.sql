-- Script para inserir dados de teste no Supabase

-- Inserir um usuário de teste (se não existir)
INSERT INTO public.cadastro_pessoas_fisica (id, phone_number, name, email)
VALUES (gen_random_uuid(), '5511999999999', 'Usuario Teste', 'usuario.teste@example.com')
ON CONFLICT (phone_number) DO NOTHING;

-- Inserir um recurso de teste (quiosque, se não existir)
INSERT INTO public.recursos (id, name, type, capacity, location, is_available)
VALUES (gen_random_uuid(), 'Quiosque Teste A', 'quiosque', 10, 'Area Comum', TRUE)
ON CONFLICT (name) DO NOTHING;

-- Inserir outro recurso de teste (quadra, se não existir)
INSERT INTO public.recursos (id, name, type, capacity, location, is_available)
VALUES (gen_random_uuid(), 'Quadra Teste B', 'quadra', 4, 'Area Esportiva', TRUE)
ON CONFLICT (name) DO NOTHING;
