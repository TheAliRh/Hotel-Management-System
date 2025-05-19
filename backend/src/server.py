from fastapi import FastAPI, status
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from bson import ObjectId
import uvicorn

from contextlib import asynccontextmanager
from datetime import datetime
import os
import sys

from routers.customers import router as customers_router
from routers.rooms import router as rooms_router
from dal.customer import CustomerDAL
from dal.room import RoomDAL

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


app.include_router(customers_router)
app.include_router(rooms_router)


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
