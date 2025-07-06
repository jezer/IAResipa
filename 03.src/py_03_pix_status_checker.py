import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class PixStatusChecker:
    def __init__(self):
        pass

    def check_and_update_pix_status(self, transaction_id):
        print(f"Checking status for transaction ID: {transaction_id}")
        # In a real scenario, you would call the Pix API to get the actual status
        # For demonstration, we'll simulate a successful payment.
        
        # Simulate fetching payment status from an external API
        simulated_payment_status = "completed"

        if simulated_payment_status == "completed":
            # Update reservation status in Supabase
            try:
                # Find the reservation associated with the transaction_id
                # This assumes 'payments' table has 'transaction_id' and 'reservation_id'
                # And 'reservations' table has 'id' and 'status'
                
                # First, get reservation_id from payments table
                payment_data = supabase.from_('payments').select('reservation_id').eq('transaction_id', transaction_id).execute()
                
                if payment_data.data and len(payment_data.data) > 0:
                    reservation_id = payment_data.data[0]['reservation_id']
                    print(f"Found reservation ID {reservation_id} for transaction {transaction_id}")
                    
                    # Update the reservation status
                    update_response = supabase.from_('reservations').update({'status': 'confirmed'}).eq('id', reservation_id).execute()
                    print("Supabase update response:", update_response)
                    
                    if update_response.data:
                        return {"status": "success", "message": f"Reservation {reservation_id} confirmed for transaction {transaction_id}"}
                    else:
                        return {"status": "error", "message": f"Failed to update reservation {reservation_id} status: {update_response.error}"}
                else:
                    return {"status": "error", "message": f"No payment found for transaction ID: {transaction_id}"}
            except Exception as e:
                return {"status": "error", "message": f"Database error: {e}"}
        else:
            return {"status": "info", "message": f"Payment for transaction {transaction_id} is {simulated_payment_status}"}

if __name__ == "__main__":
    # Example Usage:
    checker = PixStatusChecker()
    
    # Simulate a transaction ID from a Pix payment
    test_transaction_id = "CEL_5511987654321_PED_12345"
    result = checker.check_and_update_pix_status(test_transaction_id)
    print("Result:", result)
