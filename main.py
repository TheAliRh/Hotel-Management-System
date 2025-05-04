from fastapi import FastAPI

# making an instance of the FastAPI
app = FastAPI()

# Test class


class Room:
    number: int = None
    type: str = None
    status: str = None


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

# POST methods


@app.post("/api/login")  # Login authentication
def login(username: str, password: str):
    for user in users:
        if user["username"] == username and user["password"] == password:
            return {"Message": f"User {username} loged in successfully!"}


@app.post("/api/sign-up")  # Creating new user
def post_user(username: str, password: str):
    return {"Message": f"new user {username} added successfully!"}


@app.post("/api/new-customer")  # Creating new customer
def post_customer():
    return {"Message": "customer successfully added!"}


@app.post("/api/new-room")  # Creating new room
def post_room():
    return {"Message": "room successfully added!"}


# GET methods


@app.get("/api/customers")
def get_customers():
    return customers


@app.get("/api/rooms")
def get_rooms():
    return rooms


# PUT methods


@app.put("/api/room/{room_number}")
def update_room(room_number: int, status: str):
    rooms[room_number]["status"] = status
    return {"Message": "Room updated successfully!"}


# Delete methods
