import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class ReservationManager:
    def __init__(self):
        pass

    def check_resource_availability(self, resource_type, date, start_time, end_time):
        print(f"Checking availability for {resource_type} on {date} from {start_time} to {end_time}")
        # This is a placeholder for actual availability logic.
        # In a real scenario, you would query the 'courts' and 'reservations' tables
        # to find available slots.
        
        # Simulate availability
        available_resources = [
            {"id": "court_1_uuid", "name": "Quadra 1", "type": "beach_tennis", "price_per_hour": 50.00},
            {"id": "kiosk_a_uuid", "name": "Quiosque A", "type": "kiosk", "price_per_hour": 30.00}
        ]
        return {"status": "success", "available_resources": available_resources}

    def create_provisional_reservation(self, user_id, court_id, start_time, end_time):
        print(f"Creating provisional reservation for user {user_id} on court {court_id} from {start_time} to {end_time}")
        try:
            response = supabase.from_('reservations').insert({
                'user_id': user_id,
                'court_id': court_id,
                'start_time': start_time,
                'end_time': end_time,
                'status': 'provisional'
            }).execute()
            
            if response.data:
                return {"status": "success", "reservation": response.data[0]}
            else:
                return {"status": "error", "message": response.error}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_user_reservations(self, user_id):
        print(f"Fetching reservations for user {user_id}")
        try:
            response = supabase.from_('reservations').select('*').eq('user_id', user_id).execute()
            if response.data:
                return {"status": "success", "reservations": response.data}
            else:
                return {"status": "error", "message": response.error}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_reservation(self, reservation_id, new_start_time=None, new_end_time=None, new_status=None):
        print(f"Updating reservation {reservation_id}")
        update_data = {}
        if new_start_time: update_data['start_time'] = new_start_time
        if new_end_time: update_data['end_time'] = new_end_time
        if new_status: update_data['status'] = new_status

        try:
            response = supabase.from_('reservations').update(update_data).eq('id', reservation_id).execute()
            if response.data:
                return {"status": "success", "reservation": response.data[0]}
            else:
                return {"status": "error", "message": response.error}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def cancel_reservation(self, reservation_id):
        print(f"Cancelling reservation {reservation_id}")
        return self.update_reservation(reservation_id, new_status='cancelled')

    def add_to_waiting_list(self, user_id, court_id, desired_time):
        print(f"Adding user {user_id} to waiting list for court {court_id} at {desired_time}")
        try:
            response = supabase.from_('waiting_list').insert({
                'user_id': user_id,
                'court_id': court_id,
                'desired_time': desired_time
            }).execute()
            if response.data:
                return {"status": "success", "waiting_list_entry": response.data[0]}
            else:
                return {"status": "error", "message": response.error}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_waiting_list_for_resource(self, court_id):
        print(f"Fetching waiting list for court {court_id}")
        try:
            response = supabase.from_('waiting_list').select('*').eq('court_id', court_id).order('created_at').execute()
            if response.data:
                return {"status": "success", "waiting_list": response.data}
            else:
                return {"status": "error", "message": response.error}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def notify_waiting_list_user(self, user_id, court_id, available_time):
        print(f"Notifying user {user_id} about availability of court {court_id} at {available_time}")
        # This would involve sending a WhatsApp message via Waha/n8n
        return {"status": "success", "message": "Notification sent (simulated)"}

if __name__ == "__main__":
    manager = ReservationManager()

    # Example Usage:
    user_id = "some_user_uuid"
    court_id = "some_court_uuid"
    current_time = datetime.now()
    future_time = current_time + timedelta(hours=2)

    # Check availability
    availability = manager.check_resource_availability("beach_tennis", "2025-07-06", "10:00", "12:00")
    print("Availability:", availability)

    # Create provisional reservation
    provisional_res = manager.create_provisional_reservation(user_id, court_id, current_time.isoformat(), future_time.isoformat())
    print("Provisional Reservation:", provisional_res)

    # Get user reservations
    user_res = manager.get_user_reservations(user_id)
    print("User Reservations:", user_res)

    # Cancel reservation (assuming provisional_res was successful)
    if provisional_res["status"] == "success":
        cancel_res = manager.cancel_reservation(provisional_res["reservation"]['id'])
        print("Cancelled Reservation:", cancel_res)

    # Add to waiting list
    waiting_list_entry = manager.add_to_waiting_list(user_id, court_id, future_time.isoformat())
    print("Waiting List Entry:", waiting_list_entry)

    # Get waiting list for a resource
    waiting_list = manager.get_waiting_list_for_resource(court_id)
    print("Waiting List:", waiting_list)

    # Notify waiting list user
    if waiting_list["status"] == "success" and waiting_list["waiting_list"]:
        first_in_list = waiting_list["waiting_list"][0]
        notification = manager.notify_waiting_list_user(first_in_list['user_id'], first_in_list['court_id'], first_in_list['desired_time'])
        print("Notification:", notification)
