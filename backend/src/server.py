from fastapi import FastAPI, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from bson import ObjectId
import uvicorn

from contextlib import asynccontextmanager
from datetime import datetime
import os
import sys

from dal.customer import Customer, CustomerDAL
from dal.room import Room, RoomDAL

# Static variables

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

    customers_collection = database.get_collection("customers_collection")
    rooms_collection = database.get_collection("rooms_collection")

    app.customer_dal = CustomerDAL(customers_collection)
    app.room_dal = RoomDAL(rooms_collection)

    # Yield back to fastapi application:
    yield

    # Shutdown:
    client.close()


app = FastAPI(lifespan=lifespan, debug=DEBUG)


# Customer methods


"""
Create new customer
"""


@app.post("/api/customers/new")
async def post_customer(
    firstname: str,
    lastname: str,
    id: str,
    phone: str,
    nationality: str,
    new_customer: Customer,
) -> Customer:
    new_customer.status = "present"
    return await app.customer_dal.create_customer(
        firstname, lastname, id, phone, nationality, new_customer.status
    )


"""
List all customers
"""


@app.get("/api/customers")
async def get_customers():
    return await app.customer_dal.list_customers()


"""
Show customer
"""


@app.get("/api/customers/{customer_id}")
async def get_customer_by_id(customer_id: int) -> Customer:
    return await app.customer_dal.get_customer(customer_id)


"""
Update customer
"""


@app.put("/api/customers/{customer_id}")
async def update_customer(
    customer_id: str,
    firstname: str,
    lastname: str,
    id: str,
    nationality: str,
    status: str,
):
    return await app.customer_dal.update_customer(customer_id)


"""
Delete customer
"""


@app.delete("/api/customers/{customer_id}")
async def delete_customer(id: int, customer_id: str):
    return await app.customer_dal.delete_customer(customer_id)


# Room methods


"""
Create new room
"""


@app.post("/api/rooms/new")
async def create_new_room(number: int, type: str, status: str) -> str:
    return await app.room_dal.create_room(number=number, type=type, status=status)


"""
List all rooms
"""


@app.get("/api/rooms")
async def list_rooms():
    return await app.room_dal.list_rooms()


"""
Show room info
"""


@app.get("/api/rooms/{room_number}")
async def show_room(room_number: int) -> Room:
    return await app.room_dal.get_room(room_number)


"""
Update room
"""


@app.put("/api/rooms/{room_number}")
async def update_room(room_number: int, status: str):
    return await app.room_dal.update_room(number=room_number)


"""
Delete room
"""


@app.delete("/api/rooms/{room_number}")
async def delete_room(room_number: int):
    return await app.room_dal.delete_room(number=room_number)


"""
Run the code
"""


def main(argv=sys.argv[1:]):
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=DEBUG)
    except KeyboardInterrupt:
        pass


"""
Server health check status
"""


@app.get("/")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    main()
