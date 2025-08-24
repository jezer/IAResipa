import pytest
import os
from supabase import Client
import uuid
import sys
from pathlib import Path

# Add the project's src directory to the Python path
# This assumes the test is run from the project root or a subdirectory
project_root = Path(__file__).resolve().parents[2] # Adjust as needed to point to C:/source/IAResipa
sys.path.insert(0, str(project_root / '03.src'))

from resipaia import get_supabase_client

@pytest.fixture(scope="module")
def supabase_client():
    """Fixture to get the Supabase client, skipping tests if credentials are not set."""
    # The hardcoded values in db_00_supabase_config.py will be used,
    # so we don't need to check os.environ here for this specific setup.
    try:
        client = get_supabase_client()
        return client
    except Exception as e:
        pytest.fail(f"Failed to get Supabase client: {e}")

@pytest.fixture(scope="function")
def temp_table_name(supabase_client: Client):
    """Fixture to create and clean up a temporary table for each test function."""
    table_name = f"test_table_{uuid.uuid4().hex}"
    
    # Create table (Supabase doesn't have direct 'CREATE TABLE' via client,
    # but inserting into a non-existent table usually creates it if RLS allows,
    # or we rely on pre-existing schema for real-world scenarios.
    # For testing, we'll simulate by just using a unique name and assuming
    # the schema allows dynamic table creation or we're testing against
    # a pre-configured test schema.)
    
    # For a more robust test, you'd typically have a way to create schema
    # or use a dedicated test database. For this exercise, we'll assume
    # the table can be "created" by the first insert.

    yield table_name

    # Clean up: delete the table or all rows from it
    try:
        # Attempt to delete all rows from the table
        # This is safer than trying to drop the table if it's not truly dynamic
        supabase_client.from_(table_name).delete().gt("id", 0).execute()
        print(f"\n[INFO] Cleaned up data from temporary table: {table_name}")
    except Exception as e:
        print(f"\n[WARNING] Could not clean up temporary table {table_name}: {e}")

def test_insert_data(supabase_client: Client, temp_table_name: str):
    """Test inserting data into a temporary Supabase table and verifying its presence."""
    data_to_insert = {"name": "Test User", "email": "test@example.com"}
    
    print(f"\n[INFO] Inserting data into {temp_table_name}: {data_to_insert}")
    response = supabase_client.from_(temp_table_name).insert(data_to_insert).execute()
    
    assert response.data is not None, "Insert operation failed: No data returned."
    assert len(response.data) == 1, "Insert operation returned unexpected number of rows."
    
    # Verify by reading
    print(f"[INFO] Verifying inserted data from {temp_table_name}...")
    read_response = supabase_client.from_(temp_table_name).select("*").eq("email", "test@example.com").execute()
    assert read_response.data is not None, "Verification read failed: No data returned."
    assert len(read_response.data) == 1, "Verification read returned unexpected number of rows."
    assert read_response.data[0]["name"] == data_to_insert["name"], "Verification data mismatch."
    print(f"[INFO] Data successfully inserted and verified in {temp_table_name}.")

def test_read_data(supabase_client: Client, temp_table_name: str):
    """Test reading data from a Supabase table after insertion."""
    initial_data = [
        {"name": "User A", "email": "user_a@example.com"},
        {"name": "User B", "email": "user_b@example.com"}
    ]
    
    print(f"\n[INFO] Inserting initial data for read test into {temp_table_name}: {initial_data}")
    supabase_client.from_(temp_table_name).insert(initial_data).execute()
    
    print(f"[INFO] Reading all data from {temp_table_name}...")
    response = supabase_client.from_(temp_table_name).select("*").execute()
    
    assert response.data is not None, "Read operation failed: No data returned."
    assert len(response.data) == 2, "Read operation returned unexpected number of rows."
    
    # Verify specific data
    names = {row["name"] for row in response.data}
    assert "User A" in names and "User B" in names, "Read data mismatch."
    print(f"[INFO] Data successfully read and verified from {temp_table_name}.")

def test_update_data(supabase_client: Client, temp_table_name: str):
    """Test updating data in a Supabase table and verifying the update."""
    data_to_insert = {"name": "Old Name", "email": "update@example.com"}
    insert_response = supabase_client.from_(temp_table_name).insert(data_to_insert).execute()
    
    assert insert_response.data is not None and len(insert_response.data) == 1, "Failed to insert initial data for update test."
    
    updated_name = "New Name"
    print(f"\n[INFO] Updating data in {temp_table_name} for email 'update@example.com' to name '{updated_name}'")
    update_response = supabase_client.from_(temp_table_name).update({"name": updated_name}).eq("email", "update@example.com").execute()
    
    assert update_response.data is not None, "Update operation failed: No data returned."
    assert len(update_response.data) == 1, "Update operation returned unexpected number of rows."
    assert update_response.data[0]["name"] == updated_name, "Updated data mismatch."
    
    # Verify by reading
    print(f"[INFO] Verifying updated data from {temp_table_name}...")
    read_response = supabase_client.from_(temp_table_name).select("*").eq("email", "update@example.com").execute()
    assert read_response.data is not None, "Verification read failed after update."
    assert len(read_response.data) == 1, "Verification read returned unexpected number of rows after update."
    assert read_response.data[0]["name"] == updated_name, "Verification data mismatch after update."
    print(f"[INFO] Data successfully updated and verified in {temp_table_name}.")

def test_delete_data(supabase_client: Client, temp_table_name: str):
    """Test deleting data from a Supabase table and verifying its removal."""
    data_to_insert = {"name": "To Be Deleted", "email": "delete@example.com"}
    insert_response = supabase_client.from_(temp_table_name).insert(data_to_insert).execute()
    
    assert insert_response.data is not None and len(insert_response.data) == 1, "Failed to insert initial data for delete test."
    
    print(f"\n[INFO] Deleting data from {temp_table_name} for email 'delete@example.com'")
    delete_response = supabase_client.from_(temp_table_name).delete().eq("email", "delete@example.com").execute()
    
    assert delete_response.data is not None, "Delete operation failed: No data returned."
    assert len(delete_response.data) == 1, "Delete operation returned unexpected number of rows."
    
    # Verify by reading
    print(f"[INFO] Verifying data removal from {temp_table_name}...")
    read_response = supabase_client.from_(temp_table_name).select("*").eq("email", "delete@example.com").execute()
    assert read_response.data is not None, "Verification read failed after delete."
    assert len(read_response.data) == 0, "Data was not successfully deleted."
    print(f"[INFO] Data successfully deleted and verified from {temp_table_name}.")
