from typing import TypedDict, Literal

class ReservationState(TypedDict):
    """Representa o estado da conversa sobre reservas."""
    user_message: str
    phone_number: str
    intent: Literal[
        "check_user", "check_availability", "make_reservation",
        "cancel_reservation", "check_reservations", "join_waitlist",
        "general_query", ""
    ]
    sql_query: str | None
    sql_result: dict | None
    response: str | None
    user_id: int | None
    is_registered: bool