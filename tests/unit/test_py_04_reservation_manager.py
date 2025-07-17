import pytest
from unittest.mock import MagicMock, patch
from resipaia import check_active_reservations, check_availability, create_provisional_reservation, manage_existing_reservations, add_to_waiting_list, notify_waiting_list

@pytest.fixture
def mock_supabase_client():
    return MagicMock()

@pytest.fixture
def mock_message_details():
    return {
        "from": "+5511999998888",
        "user_id": "user_test_uuid",
        "resource_id": "resource_test_uuid",
        "start_time": "2025-07-10T10:00:00Z",
        "end_time": "2025-07-10T12:00:00Z",
        "amount": 150.00,
        "pix_txid": "TXID_TEST_123",
        "requested_time": "2025-07-09T15:00:00Z",
        "body": ""
    }

def test_check_active_reservations_found(mock_supabase_client, mock_message_details):
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = [{'id': 'res1', 'user_id': 'user_test_uuid', 'status': 'ativa'}]
    response = check_active_reservations(mock_supabase_client, mock_message_details)
    assert response["status"] == "active_reservations_found"
    assert len(response["reservations"]) == 1

def test_check_active_reservations_not_found(mock_supabase_client, mock_message_details):
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = []
    response = check_active_reservations(mock_supabase_client, mock_message_details)
    assert response["status"] == "no_active_reservations"

def test_check_availability_found(mock_supabase_client, mock_message_details):
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{'name': 'Quadra A', 'type': 'quadra'}]
    response = check_availability(mock_supabase_client, mock_message_details)
    assert response["status"] == "available"
    assert "Quadra A (quadra)" in response["options"]

def test_check_availability_not_found(mock_supabase_client, mock_message_details):
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    response = check_availability(mock_supabase_client, mock_message_details)
    assert response["status"] == "not_available"

def test_create_provisional_reservation_success(mock_supabase_client, mock_message_details):
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value.data = [{'id': 'new_res_uuid'}]
    response = create_provisional_reservation(mock_supabase_client, mock_message_details)
    assert response["status"] == "provisional_created"
    assert response["reservation_id"] == "new_res_uuid"

def test_manage_existing_reservations_view(mock_supabase_client, mock_message_details):
    mock_message_details["action"] = "view"
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{'id': 'res_view', 'user_id': 'user_test_uuid'}]
    response = manage_existing_reservations(mock_supabase_client, mock_message_details)
    assert response["status"] == "success"
    assert len(response["reservations"]) == 1

def test_manage_existing_reservations_cancel(mock_supabase_client, mock_message_details):
    mock_message_details["action"] = "cancel"
    mock_message_details["reservation_id"] = "res_cancel_uuid"
    mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{'id': 'res_cancel_uuid'}]
    response = manage_existing_reservations(mock_supabase_client, mock_message_details)
    assert response["status"] == "success"
    assert "cancelada com sucesso" in response["message"]

def test_manage_existing_reservations_modify(mock_supabase_client, mock_message_details):
    mock_message_details["action"] = "modify"
    mock_message_details["reservation_id"] = "res_modify_uuid"
    mock_message_details["new_data"] = {"status": "confirmada"}
    mock_supabase_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{'id': 'res_modify_uuid', 'status': 'confirmada'}]
    response = manage_existing_reservations(mock_supabase_client, mock_message_details)
    assert response["status"] == "success"
    assert "modificada com sucesso" in response["message"]

def test_add_to_waiting_list_success(mock_supabase_client, mock_message_details):
    mock_supabase_client.table.return_value.insert.return_value.execute.return_value.data = [{'id': 'waiting_uuid'}]
    response = add_to_waiting_list(mock_supabase_client, mock_message_details)
    assert response["status"] == "added_to_waiting_list"
    assert response["waiting_id"] == "waiting_uuid"

def test_notify_waiting_list_found(mock_supabase_client):
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = [{'user_id': 'user1'}, {'user_id': 'user2'}]
    response = notify_waiting_list(mock_supabase_client, "resource_id_test")
    assert response["status"] == "notification_sent"
    assert len(response["notified_users"]) == 2

def test_notify_waiting_list_not_found(mock_supabase_client):
    mock_supabase_client.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = []
    response = notify_waiting_list(mock_supabase_client, "resource_id_test")
    assert response["status"] == "no_waiting_users"
