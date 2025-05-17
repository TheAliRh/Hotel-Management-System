from fastapi import FastAPI, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from bson import ObjectId
import uvicorn

from contextlib import asynccontextmanager
from datetime import datetime
import os
import sys

from dal import ToDoDAL, Room, Customer, Reservation

# Static variables

COLLECTION_NAME = "hotel_management"
MONGODB_URI = ""
DEBUG = os.environ.get("DEBUGE", "").strip().lower() in {"1", "true", "on", "yes"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    client = AsyncIOMotorClient(MONGODB_URI)
    database = client.get_default_database()

    # Ensure the database is available:
    pong = await database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Cluster connection is not okay!")
    hotel_collection = database.get_collection(COLLECTION_NAME)
    app.tododal = ToDoDAL(hotel_collection)

    # Yield back to fastapi application:
    yield

    # Shutdown:
    client.close()


app = FastAPI(lifespan=lifespan, debug=DEBUG)


# Customer methods


@app.post("/api/new-customer")
async def post_customer(
    firstname: str,
    lastname: str,
    id: str,
    phone: str,
    nationality: str,
    new_customer: Customer,
) -> Customer:
    new_customer.status = "present"
    return await app.tododal.create_customer(
        firstname, lastname, id, phone, nationality, new_customer.status
    )


@app.get("/api/customers")
def get_customers():
    pass
    # return customers


@app.get("/api/customers/{customer_id}")
async def get_customer_by_id(customer_id: int) -> Customer:
    return await app.tododal.get_customer(customer_id)


@app.put("/api/customers/{customer_id}")
def update_customer(
    customer_id: str,
    firstname: str,
    lastname: str,
    id: str,
    nationality: str,
    status: str,
):
    # for customer in customers:
    #     if customers[customer]["id"] == customer_id:
    #         customers[customer]["firstname"] = firstname
    #         customers[customer]["lastname"] = lastname
    #         customers[customer]["id"] = id
    #         customers[customer]["nationality"] = nationality
    #         customers[customer]["status"] = status
    return {"Message": "Customer updated successfully!"}


@app.delete("/api/customers/{customer_id}")
def delete_customer(id: int, customer_id: str):
    # if customers[id]["id"] == customer_id:
    #     del customers[id]
    return {"Message": f"Customer '{customer_id}' deleted successfully!"}


# Room methods

"""
Create new room
"""


@app.post("/api/new-room")
async def create_new_room(number: int, type: str, status: str) -> str:
    return await app.tododal.create_room(number=number, type=type, status=status)


"""
List all rooms
"""


# @app.get("/api/rooms")
# async def list_rooms():
#     return rooms


"""
Show room info
"""


@app.get("/api/rooms/{room_number}")
async def show_room(room_number: int) -> Room:
    return await app.tododal.get_room(room_number)


# @app.put("/api/rooms/{room_number}")
# def update_room(room_number: int, status: str):
#     rooms[room_number]["status"] = status
#     return {"Message": "Room updated successfully!"}


# @app.delete("/api/rooms/{room_number}")
# def delete_room(room_number: int):
#     del rooms[room_number]
#     {"Message": f"Room '{room_number}' deleted successfully!"}


def main(argv=sys.argv[1:]):
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
