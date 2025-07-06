import os
from supabase import create_client, Client

# Initialize Supabase client
# These values would typically come from environment variables for security
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://resipaia.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNxdWFyeXlycWx5cG16ZmFqYmhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE4MzY3NzcsImV4cCI6MjA2NzQxMjc3N30.rd-CWbup_U-9DYFbmpGXaxlbyEOcBoTaIM6SMUAu5gk")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_tables():
    print("--- Creating 'users' table ---")
    # Users table: Stores user information
    # id: Primary key, auto-generated UUID
    # whatsapp_number: User's WhatsApp number (unique)
    # name: User's name
    # created_at: Timestamp of user creation
    # updated_at: Timestamp of last update
    print(supabase.rpc('execute_sql', {'sql_query': '''
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            whatsapp_number VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    '''}).execute())

    print("--- Creating 'kiosks' table ---")
    # Kiosks table: Stores information about different kiosks/locations
    # id: Primary key, auto-generated UUID
    # name: Kiosk name
    # location: Kiosk physical location
    # description: Kiosk description
    print(supabase.rpc('execute_sql', {'sql_query': '''
        CREATE TABLE IF NOT EXISTS kiosks (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(255) NOT NULL,
            location TEXT,
            description TEXT
        );
    '''}).execute())

    print("--- Creating 'courts' table ---")
    # Courts table: Stores information about available courts/resources
    # id: Primary key, auto-generated UUID
    # kiosk_id: Foreign key to kiosks table
    # name: Court name/identifier
    # type: Type of court (e.g., "tennis", "padel", "football")
    # capacity: Maximum capacity of the court
    # price_per_hour: Price for one hour of reservation
    print(supabase.rpc('execute_sql', {'sql_query': '''
        CREATE TABLE IF NOT EXISTS courts (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            kiosk_id UUID REFERENCES kiosks(id),
            name VARCHAR(255) NOT NULL,
            type VARCHAR(50),
            capacity INTEGER,
            price_per_hour DECIMAL(10, 2),
            PRIMARY KEY (id, kiosk_id)
        );
    '''}).execute())

    print("--- Creating 'reservations' table ---")
    # Reservations table: Stores reservation details
    # id: Primary key, auto-generated UUID
    # user_id: Foreign key to users table
    # court_id: Foreign key to courts table
    # start_time: Reservation start time
    # end_time: Reservation end time
    # status: Reservation status (e.g., "pending", "confirmed", "cancelled")
    # created_at: Timestamp of reservation creation
    # updated_at: Timestamp of last update
    print(supabase.rpc('execute_sql', {'sql_query': '''
        CREATE TABLE IF NOT EXISTS reservations (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id),
            court_id UUID REFERENCES courts(id),
            start_time TIMESTAMP WITH TIME ZONE NOT NULL,
            end_time TIMESTAMP WITH TIME ZONE NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    '''}).execute())

    print("--- Creating 'payments' table ---")
    # Payments table: Stores payment details for reservations
    # id: Primary key, auto-generated UUID
    # reservation_id: Foreign key to reservations table
    # amount: Payment amount
    # currency: Currency (e.g., "BRL")
    # method: Payment method (e.g., "PIX")
    # status: Payment status (e.g., "pending", "completed", "failed")
    # transaction_id: External transaction ID (e.g., Pix transaction ID)
    # created_at: Timestamp of payment creation
    print(supabase.rpc('execute_sql', {'sql_query': '''
        CREATE TABLE IF NOT EXISTS payments (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            reservation_id UUID REFERENCES reservations(id),
            amount DECIMAL(10, 2) NOT NULL,
            currency VARCHAR(10) DEFAULT 'BRL',
            method VARCHAR(50),
            status VARCHAR(50) DEFAULT 'pending',
            transaction_id VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    '''}).execute())

    print("--- Creating 'waiting_list' table ---")
    # Waiting List table: Stores users waiting for a specific court/time slot
    # id: Primary key, auto-generated UUID
    # user_id: Foreign key to users table
    # court_id: Foreign key to courts table
    # desired_time: Desired time for reservation
    # created_at: Timestamp of entry to waiting list
    print(supabase.rpc('execute_sql', {'sql_query': '''
        CREATE TABLE IF NOT EXISTS waiting_list (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id UUID REFERENCES users(id),
            court_id UUID REFERENCES courts(id),
            desired_time TIMESTAMP WITH TIME ZONE NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    '''}).execute())

    print("--- Tables creation script finished ---")

if __name__ == "__main__":
    # This script is intended to be run manually to set up the schema.
    # It uses RPC to execute SQL, which requires a Supabase function 'execute_sql'
    # that takes a 'sql_query' parameter and executes it.
    # For actual schema migration, consider using Supabase migrations or direct SQL execution.
    print("This script generates SQL commands for Supabase table creation.")
    print("Please ensure you have the 'supabase-py' library installed (`pip install supabase-py`).")
    print("You will need to manually execute these commands in your Supabase SQL editor or via a custom RPC function.")
    # To run this, you would typically call create_tables() after setting up the Supabase client.
    # For demonstration, we're just showing the structure.
    # create_tables() # Uncomment to attempt execution if a 'execute_sql' RPC is available.
