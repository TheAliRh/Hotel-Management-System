# Test class


class Room:
    number: int = None
    type: str = None
    status: str = None


class Customer:
    firstname: str = None
    lastname: str = None
    id: str = None
    nationality: str = None
    status: str = None


class Reservation:
    id: str = None
    firstname: str = None
    lastname: str = None
    customer_id: str = None
    checkin_date: str = None
    checkout_date: str = None
    room_number: int = None


# Test data

users = {1: {"username": "admin", "password": "admin"}}

customers = {
    1: {
        "firstname": "john",
        "lastname": "doe",
        "id": "059 999 99 99",
        "nationality": "Iran",
        "status": "present",
    }
}

rooms = {1: {"room_number": 1, "type": "master", "status": "empty"}}

reservations = {
    1: {
        "reserve_id": "1",
        "firstname": "john",
        "lastname": "doe",
        "id": "059 999 99 99",
        "checkin_date": "1-1-2025",
        "checkout_date": "1-2-2025",
        "room_number": 1,
    }
}
