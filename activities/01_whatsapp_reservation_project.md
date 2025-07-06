# 1. Checklist do Projeto: Sistema de Reserva via WhatsApp

Para o desenvolvimento do sistema de reserva via WhatsApp, as seguintes atividades devem ser realizadas e evidenciadas:

## 1.1. Fase de Planejamento e Configuração Inicial

### 1.1.1. Definição do Esquema do Banco de Dados no Supabase
- [ ] **Ação:** Definir e criar o esquema completo do banco de dados no Supabase, incluindo tabelas para usuários, quiosques, quadras, reservas, pagamentos e lista de espera.
  - **Evidência:** Script SQL de criação do esquema (`supabase_schema.sql`) e/ou screenshots da interface do Supabase mostrando as tabelas criadas.

### 1.1.2. Configuração do Ambiente Docker Compose
- [ ] **Ação:** Criar o arquivo `docker-compose.yml` para orquestrar os serviços Waha e n8n.
  - **Evidência:** Arquivo `docker-compose.yml`.
- [ ] **Ação:** Configurar o Waha para integração com o WhatsApp (obtenção de credenciais, webhook para n8n).
  - **Evidência:** Arquivo de configuração do Waha e/ou logs de inicialização do contêiner Waha mostrando conexão bem-sucedida.
- [ ] **Ação:** Configurar o n8n para integração com o Supabase (credenciais de acesso, URL da API).
  - **Evidência:** Screenshots das configurações de credenciais do Supabase no n8n.

## 1.2. Fase de Desenvolvimento dos Workflows n8n

### 1.2.1. Workflow de Recebimento de Mensagens do WhatsApp
- [ ] **Ação:** Implementar o workflow inicial no n8n para receber mensagens do WhatsApp via webhook do Waha.
  - **Evidência:** Exportação JSON do workflow do n8n (`n8n_whatsapp_receiver.json`).

### 1.2.2. Workflow de Verificação de Cadastro de Usuário
- [ ] **Ação:** Desenvolver o workflow no n8n para consultar a tabela `cadastro_pessoas_fisica` no Supabase e verificar se o número de celular do remetente está cadastrado.
  - **Evidência:** Exportação JSON do workflow do n8n (`n8n_user_registration_check.json`) e logs de execução mostrando consultas bem-sucedidas ao Supabase.

### 1.2.3. Workflow de Consulta de Disponibilidade de Recursos
- [ ] **Ação:** Criar o workflow no n8n para consultar a disponibilidade de quiosques e quadras de beach tennis no Supabase, considerando datas e horários.
  - **Evidência:** Exportação JSON do workflow do n8n (`n8n_resource_availability.json`) e logs de execução mostrando resultados de consulta de disponibilidade.

### 1.2.4. Workflow de Criação de Reserva
- [ ] **Ação:** Implementar o workflow no n8n para registrar uma nova reserva no Supabase, após a seleção do usuário e verificação de disponibilidade.
  - **Evidência:** Exportação JSON do workflow do n8n (`n8n_create_reservation.json`) e logs de execução mostrando inserções de reservas no Supabase.

### 1.2.5. Workflow de Iniciação de Pagamento Pix
- [ ] **Ação:** Desenvolver o workflow no n8n para gerar um QR Code Pix ou link de pagamento e enviá-lo ao usuário.
  - **Evidência:** Exportação JSON do workflow do n8n (`n8n_pix_initiation.json`) e logs de chamadas à API Pix.

### 1.2.6. Workflow de Verificação de Status de Pagamento Pix
- [ ] **Ação:** Implementar o workflow no n8n para verificar o status do pagamento Pix (via webhook de callback da API Pix ou consulta periódica).
  - **Evidência:** Exportação JSON do workflow do n8n (`n8n_pix_status_check.json`) e logs de callbacks/consultas da API Pix.

### 1.2.7. Workflow de Cancelamento de Reserva
- [ ] **Ação:** Criar o workflow no n8n para permitir que o usuário cancele uma reserva, atualizando o status no Supabase.
  - **Evidência:** Exportação JSON do workflow do n8n (`n8n_cancel_reservation.json`) e logs de execução mostrando atualizações de status no Supabase.

### 1.2.8. Workflow de Notificação da Lista de Espera
- [ ] **Ação:** Desenvolver o workflow no n8n para notificar o próximo usuário na lista de espera quando uma reserva é cancelada.
  - **Evidência:** Exportação JSON do workflow do n8n (`n8n_waiting_list_notification.json`) e logs de envio de mensagens WhatsApp para usuários da lista de espera.

### 1.2.9. Workflow de Integração Gemini para Respostas Inteligentes
- [ ] **Ação:** Implementar o workflow no n8n para integrar com a API Gemini, formatando consultas SQL para o Supabase com base nas perguntas do usuário e retornando as respostas.
  - **Evidência:** Exportação JSON do workflow do n8n (`n8n_gemini_integration.json`) e logs de chamadas à API Gemini e consultas ao Supabase.

## 1.3. Fase de Testes

### 1.3.1. Testes de Ponta a Ponta
- [ ] **Ação:** Realizar testes completos de todo o fluxo de reserva, desde o início da conversa no WhatsApp até a confirmação da reserva, pagamento, cancelamento e notificação da lista de espera.
  - **Evidência:** Relatório de testes detalhado, screenshots e/ou gravação de vídeo demonstrando o fluxo completo.
