import pytest
import sys
import os

# Adiciona o diretório pai ao sys.path para permitir importações relativas


from resipaia import SupabaseSchema, SupabaseTable

def test_supabase_table_creation():
    table = SupabaseTable("test_table", ["col1", "col2"])
    assert table.name == "test_table"
    assert table.columns == ["col1", "col2"]

def test_supabase_schema_cadastro_pessoas_fisica():
    assert SupabaseSchema.CADASTRO_PESSOAS_FISICA.name == "cadastro_pessoas_fisica"
    assert "phone_number" in SupabaseSchema.CADASTRO_PESSOAS_FISICA.columns

def test_supabase_schema_recursos():
    assert SupabaseSchema.RECURSOS.name == "recursos"
    assert "type" in SupabaseSchema.RECURSOS.columns

def test_supabase_schema_reservas():
    assert SupabaseSchema.RESERVAS.name == "reservas"
    assert "status" in SupabaseSchema.RESERVAS.columns

def test_supabase_schema_lista_espera():
    assert SupabaseSchema.LISTA_ESPERA.name == "lista_espera"
    assert "requested_time" in SupabaseSchema.LISTA_ESPERA.columns

def test_get_table_columns_existing_table():
    columns = SupabaseSchema.get_table_columns("cadastro_pessoas_fisica")
    assert "phone_number" in columns
    assert "name" in columns

def test_get_table_columns_non_existing_table():
    columns = SupabaseSchema.get_table_columns("non_existent_table")
    assert columns == []
