-- Script para limpar dados de teste no Supabase

DELETE FROM public.reservas WHERE user_id IN (SELECT id FROM public.cadastro_pessoas_fisica WHERE phone_number LIKE '5511%');
DELETE FROM public.lista_espera WHERE user_id IN (SELECT id FROM public.cadastro_pessoas_fisica WHERE phone_number LIKE '5511%');
DELETE FROM public.cadastro_pessoas_fisica WHERE phone_number LIKE '5511%';
DELETE FROM public.recursos WHERE name LIKE 'Quiosque Teste%' OR name LIKE 'Quadra Teste%';
