import pytest
import os
from resipaia import get_supabase_client, SupabaseSchema, check_active_reservations, check_availability, create_provisional_reservation, manage_existing_reservations, add_to_waiting_list, notify_waiting_list
import uuid
from datetime import datetime, timedelta

@pytest.fixture(scope="module")
def supabase_client():
    if "SUPABASE_URL" not in os.environ or "SUPABASE_KEY" not in os.environ:
        pytest.skip("Variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não configuradas para testes de integração.")
    
    client = get_supabase_client()
    yield client
    # Limpeza: Remover dados de teste criados por este módulo
    try:
        client.from_(SupabaseSchema.RESERVAS.name).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        client.from_(SupabaseSchema.CADASTRO_PESSOAS_FISICA.name).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        client.from_(SupabaseSchema.RECURSOS.name).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        client.from_(SupabaseSchema.LISTA_ESPERA.name).delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
    except Exception as e:
        print(f"Erro durante a limpeza do Supabase: {e}")

def generate_unique_id():
    return str(uuid.uuid4())

@pytest.fixture
def setup_user_and_resource(supabase_client):
    user_id = generate_unique_id()
    resource_id = generate_unique_id()
    phone_number = f"+551199999{uuid.uuid4().hex[:6]}" # Generate a unique phone number

    # Inserir usuário de teste
    supabase_client.from_(SupabaseSchema.CADASTRO_PESSOAS_FISICA.name).insert({"id": user_id, "phone_number": phone_number}).execute()
    # Inserir recurso de teste
    resource_name = f"Quadra Teste {uuid.uuid4().hex[:6]}"
    supabase_client.from_(SupabaseSchema.RECURSOS.name).insert({"id": resource_id, "name": resource_name, "type": "quadra", "is_available": True}).execute()
    
    return user_id, resource_id, resource_name

def test_check_active_reservations_found(supabase_client, setup_user_and_resource):
    user_id, resource_id, _ = setup_user_and_resource
    reservation_id = generate_unique_id()
    
    # Inserir uma reserva ativa para o usuário de teste
    supabase_client.from_(SupabaseSchema.RESERVAS.name).insert({
        "id": reservation_id,
        "user_id": user_id,
        "resource_id": resource_id,
        "status": "ativa",
        "start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "amount": 100.00,
        "pix_txid": generate_unique_id()
    }).execute()

    message_details = {"user_id": user_id}
    response = check_active_reservations(supabase_client, message_details)
    assert response["status"] == "active_reservations_found"
    assert len(response["reservations"]) == 1

def test_check_active_reservations_not_found(supabase_client, setup_user_and_resource):
    user_id, _, _ = setup_user_and_resource
    message_details = {"user_id": user_id}
    response = check_active_reservations(supabase_client, message_details)
    assert response["status"] == "no_active_reservations"

def test_check_availability_found(supabase_client, setup_user_and_resource):
    _, resource_id, resource_name = setup_user_and_resource
    message_details = {"resource_type": "quadra"}
    response = check_availability(supabase_client, message_details)
    assert response["status"] == "available"
    assert f"{resource_name} (quadra)" in response["options"]

def test_check_availability_not_found(supabase_client):
    message_details = {"resource_type": "tipo_inexistente"}
    response = check_availability(supabase_client, message_details)
    assert response["status"] == "not_available"

def test_create_provisional_reservation_success(supabase_client, setup_user_and_resource):
    user_id, resource_id, _ = setup_user_and_resource
    message_details = {
        "user_id": user_id,
        "resource_id": resource_id,
        "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "amount": 150.00
    }
    response = create_provisional_reservation(supabase_client, message_details)
    assert response["status"] == "provisional_created"
    assert response["reservation_id"] is not None

def test_manage_existing_reservations_view(supabase_client, setup_user_and_resource):
    user_id, resource_id, _ = setup_user_and_resource
    reservation_id = generate_unique_id()
    supabase_client.from_(SupabaseSchema.RESERVAS.name).insert({
        "id": reservation_id,
        "user_id": user_id,
        "resource_id": resource_id,
        "status": "ativa",
        "start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "amount": 100.00,
        "pix_txid": generate_unique_id()
    }).execute()

    message_details = {"user_id": user_id, "action": "view"}
    response = manage_existing_reservations(supabase_client, message_details)
    assert response["status"] == "success"
    assert len(response["reservations"]) == 1

def test_manage_existing_reservations_cancel(supabase_client, setup_user_and_resource):
    user_id, resource_id, _ = setup_user_and_resource
    reservation_id = generate_unique_id()
    supabase_client.from_(SupabaseSchema.RESERVAS.name).insert({
        "id": reservation_id,
        "user_id": user_id,
        "resource_id": resource_id,
        "status": "ativa",
        "start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "amount": 100.00,
        "pix_txid": generate_unique_id()
    }).execute()

    message_details = {"user_id": user_id, "action": "cancel", "reservation_id": reservation_id}
    response = manage_existing_reservations(supabase_client, message_details)
    assert response["status"] == "success"
    assert "cancelada com sucesso" in response["message"]
    
    # Verificar o status no banco de dados
    result = supabase_client.from_(SupabaseSchema.RESERVAS.name).select("status").eq("id", reservation_id).single().execute()
    assert result.data["status"] == "cancelada"

def test_manage_existing_reservations_modify(supabase_client, setup_user_and_resource):
    user_id, resource_id, _ = setup_user_and_resource
    reservation_id = generate_unique_id()
    supabase_client.from_(SupabaseSchema.RESERVAS.name).insert({
        "id": reservation_id,
        "user_id": user_id,
        "resource_id": resource_id,
        "status": "ativa",
        "start_time": (datetime.now() - timedelta(hours=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(hours=1)).isoformat(),
        "amount": 100.00,
        "pix_txid": generate_unique_id()
    }).execute()

    new_start_time = (datetime.now() + timedelta(days=2)).replace(microsecond=0).isoformat()
    new_end_time = (datetime.now() + timedelta(days=2, hours=2)).replace(microsecond=0).isoformat()
    message_details = {"user_id": user_id, "action": "modify", "reservation_id": reservation_id, "new_data": {"start_time": new_start_time, "end_time": new_end_time}}
    response = manage_existing_reservations(supabase_client, message_details)
    assert response["status"] == "success"
    assert "modificada com sucesso" in response["message"]

    # Verificar o status no banco de dados
    result = supabase_client.from_(SupabaseSchema.RESERVAS.name).select("start_time", "end_time").eq("id", reservation_id).single().execute()
    assert datetime.fromisoformat(result.data["start_time"].replace("+00:00", "")) == datetime.fromisoformat(new_start_time)
    assert datetime.fromisoformat(result.data["end_time"].replace("+00:00", "")) == datetime.fromisoformat(new_end_time)

def test_add_to_waiting_list_success(supabase_client, setup_user_and_resource):
    user_id, resource_id, _ = setup_user_and_resource
    message_details = {
        "user_id": user_id,
        "resource_id": resource_id,
        "requested_time": (datetime.now() + timedelta(days=3)).isoformat()
    }
    response = add_to_waiting_list(supabase_client, message_details)
    assert response["status"] == "added_to_waiting_list"
    assert response["waiting_id"] is not None

def test_notify_waiting_list_found(supabase_client, setup_user_and_resource):
    user_id, resource_id, _ = setup_user_and_resource
    # Adicionar um usuário à lista de espera
    supabase_client.from_(SupabaseSchema.LISTA_ESPERA.name).insert({
        "user_id": user_id,
        "resource_id": resource_id,
        "requested_time": (datetime.now() + timedelta(days=4)).isoformat(),
        "status": "pendente"
    }).execute()

    response = notify_waiting_list(supabase_client, resource_id)
    assert response["status"] == "notification_sent"
    assert len(response["notified_users"]) == 1
    assert user_id in response["notified_users"]

def test_notify_waiting_list_not_found(supabase_client):
    resource_id = generate_unique_id()
    response = notify_waiting_list(supabase_client, resource_id)
    assert response["status"] == "no_waiting_users"
