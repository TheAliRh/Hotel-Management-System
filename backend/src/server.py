from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import uvicorn

from contextlib import asynccontextmanager
from datetime import datetime
import os
import logging
import sys

from routers.customers import router as customers_router
from routers.rooms import router as rooms_router
from exceptions import BusinessRuleViolation
from dal.customer import CustomerDAL
from dal.room import RoomDAL

# Static variables

logger = logging.getLogger("uvicorn.error")

MONGODB_URI = ""
DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "on", "yes"}


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


"""
Mount routers
"""


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
Global error handler
"""


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exception: Exception):
    logger.exception(f"Unhandled error at {request.url}: {exception}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": (
                str(exception)
                if DEBUG
                else "Internal server error. Please try again later."
            )
        },
    )


"""
Business rules handler
"""


@app.exception_handler(BusinessRuleViolation)
async def business_rule_handler(request: Request, exception: BusinessRuleViolation):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exception.message},
    )


"""
Server health check status
"""


@app.get("/")
async def healthcheck():
    return {"status": "ok"}


if __name__ == "__main__":
    main()
