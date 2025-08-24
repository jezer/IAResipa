#!/bin/bash
#
# Script para configurar as variáveis de ambiente do PostgreSQL para ambientes Linux/Container.
#
# IMPORTANTE: Substitua os valores abaixo pelas suas credenciais reais do Supabase PostgreSQL.

export PG_HOST="db.yourprojectid.supabase.co"
export PG_PORT="5432"
export PG_DBNAME="postgres"
export PG_USER="postgres"
export PG_PASSWORD="your_supabase_password"

echo "Variáveis de ambiente do PostgreSQL configuradas. Verifique e substitua os valores de exemplo."
echo "Para aplicar, execute: source ./configure_container_env.sh"
