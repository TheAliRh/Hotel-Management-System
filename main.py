from fastapi import FastAPI

# making an instance of the FastAPI
app = FastAPI()

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
def login(
    username: str, password: str
):  # Needs database implementation and creating authentication
    for user in users:
        if users[user]["username"] == username and users[user]["password"] == password:
            return {"Error": f"User {username} already exists!"}
    return {"Message": f"User {username} loged in successfully!"}


@app.post("/api/sign-up")  # Creating new user
def post_user(
    username: str, password: str
):  # Needs database implementation and creating authentication
    return {"Message": f"new user {username} added successfully!"}


@app.post("/api/new-customer")  # Creating new customer
def post_customer(
    firstname: str, lastname: str, id: str, nationality: str, new_customer=Customer
):
    for customer in customers:
        if customers[customer]["id"] == id:
            return {"Error": f"Customer with id {id} already exists"}
    new_customer.firstname = firstname
    new_customer.lastname = lastname
    new_customer.id = id
    new_customer.nationality = nationality
    new_customer.status = "present"
    return {"Message": "customer successfully added!"}


@app.post("/api/new-room")  # Creating new room
def post_room(number: int, type: str, status: str, room=Room):
    if number in rooms:
        return {"Error": f"room number {number} already exists"}
    room.number = number
    room.type = type
    room.status = status
    return {"Message": "room successfully added!"}


# GET methods


@app.get("/api/customers")  # Return all customers
def get_customers():
    return customers


@app.get("/api/customer/{customer_id}")  # Return customer info by id
def get_customer_by_id(customer_id: int):
    return customers[customer_id]


@app.get("/api/rooms")  # Return all rooms
def get_rooms():
    return rooms


@app.get("/api/room/{room_number}")  # Return room by number
def get_room_by_number(room_number: int):
    return rooms[room_number]


@app.get("/api/users")  # Return all users
def get_users():
    return users


@app.get("/api/user/{user_id}")  # Return user by id
def get_user(user_id: int):
    return users[user_id]


# PUT methods


@app.put("/api/room/{room_number}")
def update_room(room_number: int, status: str):
    rooms[room_number]["status"] = status
    return {"Message": "Room updated successfully!"}


# Delete methods
