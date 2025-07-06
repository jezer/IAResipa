import os
from supabase import create_client, Client
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class UserRegistrationLogic:
    def __init__(self):
        pass

    def _validate_whatsapp_number(self, whatsapp_number):
        # Basic validation for WhatsApp number (e.g., digits only, min/max length)
        # This can be expanded with more robust regex for international numbers
        if not re.fullmatch(r'^\d{10,15}$', whatsapp_number):
            return False
        return True

    def register_or_update_user(self, whatsapp_number, name=None):
        if not self._validate_whatsapp_number(whatsapp_number):
            return {"status": "error", "message": "Invalid WhatsApp number format."}

        try:
            # Check if user already exists
            existing_user = supabase.from_('users').select('*').eq('whatsapp_number', whatsapp_number).execute()

            if existing_user.data and len(existing_user.data) > 0:
                # User exists, update their information if name is provided
                if name:
                    print(f"User with WhatsApp number {whatsapp_number} already exists. Updating name to {name}.")
                    update_response = supabase.from_('users').update({'name': name, 'updated_at': 'now()'}).eq('whatsapp_number', whatsapp_number).execute()
                    if update_response.data:
                        return {"status": "success", "action": "updated", "user": update_response.data[0]}
                    else:
                        return {"status": "error", "message": f"Failed to update user: {update_response.error}"}
                else:
                    print(f"User with WhatsApp number {whatsapp_number} already exists. No update needed.")
                    return {"status": "success", "action": "no_change", "user": existing_user.data[0]}
            else:
                # User does not exist, create new user
                print(f"Registering new user with WhatsApp number {whatsapp_number} and name {name}.")
                insert_data = {'whatsapp_number': whatsapp_number}
                if name: insert_data['name'] = name

                insert_response = supabase.from_('users').insert(insert_data).execute()
                if insert_response.data:
                    return {"status": "success", "action": "created", "user": insert_response.data[0]}
                else:
                    return {"status": "error", "message": f"Failed to register user: {insert_response.error}"}
        except Exception as e:
            return {"status": "error", "message": f"Database error: {e}"}

if __name__ == "__main__":
    registrar = UserRegistrationLogic()

    # Example Usage:
    # Register a new user
    new_user_result = registrar.register_or_update_user("5511999998888", "Alice Silva")
    print("New User Registration Result:", new_user_result)

    # Try to register the same user again (should update if name is different, or no change)
    existing_user_update_result = registrar.register_or_update_user("5511999998888", "Alice Updated")
    print("Existing User Update Result:", existing_user_update_result)

    # Register another new user without a name
    another_new_user_result = registrar.register_or_update_user("5521987654321")
    print("Another New User Registration Result:", another_new_user_result)

    # Try with invalid number
    invalid_number_result = registrar.register_or_update_user("123")
    print("Invalid Number Result:", invalid_number_result)
