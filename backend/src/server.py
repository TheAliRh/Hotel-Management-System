from fastapi import FastAPI
from pymongo import MongoClient

# Mongo database config

client = MongoClient("localhost", 27017)


# making the FastAPI app
app = FastAPI()

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


@app.get("/api/customers/{customer_id}")  # Return customer info by id
def get_customer_by_id(customer_id: int):
    return customers[customer_id]


@app.get("/api/rooms")  # Return all rooms
def get_rooms():
    return rooms


@app.get("/api/rooms/{room_number}")  # Return room by number
def get_room_by_number(room_number: int):
    return rooms[room_number]


@app.get("/api/users")  # Return all users
def get_users():
    return users


@app.get("/api/users/{user_id}")  # Return user by id
def get_user(user_id: int):
    return users[user_id]


@app.get("/api/reservations")  # Return all reservarions
def get_reservations():
    return reservations


@app.get("/api/reservations/{reserve_id}")  # Return reservation
def get_reservation(reserve_id):
    for reserve in reservations:
        if reservations[reserve]["id"] == reserve_id:
            return reservations[reserve]


# PUT methods


@app.put("/api/rooms/{room_number}")  # Update room info
def update_room(room_number: int, status: str):
    rooms[room_number]["status"] = status
    return {"Message": "Room updated successfully!"}


@app.put("/api/customers/{customer_id}")  # Update customer info
def update_customer(
    customer_id: str,
    firstname: str,
    lastname: str,
    id: str,
    nationality: str,
    status: str,
):
    for customer in customers:
        if customers[customer]["id"] == customer_id:
            customers[customer]["firstname"] = firstname
            customers[customer]["lastname"] = lastname
            customers[customer]["id"] = id
            customers[customer]["nationality"] = nationality
            customers[customer]["status"] = status
    return {"Message": "Customer updated successfully!"}


@app.put("/api/users/{user_id}")  # Update user info
def update_user(user_id: int, username: str, password: str):
    users[user_id]["username"] = username
    users[user_id]["password"] = password
    return {"Message": "User updated successfully!"}


@app.put("/api/reservations/{reserve_id}")  # Update reservation info
def update_reservation(
    reserve_id: str,
    firstname: str,
    lastname: str,
    customer_id: str,
    checkin_date: str,
    checkout_date: str,
    room_number: int,
):
    for reserve in reservations:
        if reservations[reserve]["reserve_id"] == reserve_id:
            reservations[reserve]["firstname"] = firstname
            reservations[reserve]["lastname"] = lastname
            reservations[reserve]["customer_id"] = customer_id
            reservations[reserve]["checkin_date"] = checkin_date
            reservations[reserve]["checkout_date"] = checkout_date
            reservations[reserve]["room_number"] = room_number

    return {"Message": "Reservation updated successfully!"}


# Delete methods


@app.delete("/api/users/{user_id}")  # Delete user
def delete_user(user_id: int, username: str, password: str):
    if (
        users[user_id]["username"] == username
        and users[user_id]["password"] == password
    ):
        del users[user_id]
        return {"Message": f"User '{username}' deleted successfully!"}


@app.delete("/api/customers/{customer_id}")  # Delete customer
def delete_customer(id: int, customer_id: str):
    if customers[id]["id"] == customer_id:
        del customers[id]
        return {"Message": f"Customer '{customer_id}' deleted successfully!"}


@app.delete("/api/reservations/{reserve_id}")  # Delete reservation
def delete_reseravtion(reserve_id: str):
    for reserve in reservations:
        if reservations[reserve]["reserve_id"] == reserve_id:
            del reservations[reserve]
            return {"Message": f"Reservation '{reserve_id}' deleted successfully!"}


@app.delete("/api/rooms/{room_number}")  # Delete room
def delete_room(room_number: int):
    del rooms[room_number]
    {"Message": f"Room '{room_number}' deleted successfully!"}
