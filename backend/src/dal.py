# Data Access Layer (DAL)
# Responsible for handling interaction between database and application

# from bson import ObjectId
# from pymongo import ReturnDocument
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection


class Room(BaseModel):
    number: int = None
    type: str = None
    status: bool = None  # Empty=True, Full=False

    @staticmethod
    def from_doc(doc):
        return Room(
            number=int(doc["number"]), type=str(doc["type"]), status=bool(doc["status"])
        )


class Customer(BaseModel):
    firstname: str = None
    lastname: str = None
    id: str = None
    phone: str = None
    nationality: str = None
    status: bool = None  # Active=true, Inactive=False
    room: int = None

    @staticmethod
    def from_doc(doc):
        return Customer(
            firstname=str(doc["firstname"]),
            lastname=str(doc["lastname"]),
            id=str(doc["id"]),
            phone=str(doc["phone"]),
            nationality=str(doc["nationality"]),
            status=bool(doc["status"]),
            room=int(doc["room"]),
        )


class Reservation(BaseModel):
    id: str = None
    firstname: str = None
    lastname: str = None
    customer_id: str = None
    checkin_date: str = None
    checkout_date: str = None
    room_number: int = None

    @staticmethod
    def from_doc(doc):
        return Reservation(
            id=str(doc["_id"]),
            firstname=str(doc["firstname"]),
            lastname=str(doc["lastname"]),
            customer_id=str(doc["customer_id"]),
            checkin_date=str(doc["checkin_date"]),
            checkout_date=str(doc["checkout_date"]),
            room_number=int(doc["room_number"]),
        )


# class User(BaseModel):
#     fullname: str = None
#     phone: str = None
#     username: str = None
#     password: str = None

#     @staticmethod
#     def form_doc(doc):
#         return User(
#             fullname=str(doc["fullname"]),
#             phone=str(doc["phone"]),
#             username=str(doc["username"]),
#             password=str(doc["password"]),
#         )


# class Employee(BaseModel):
#     id: str = None
#     firstname: str = None
#     lastname: str = None
#     employee_id: str = None
#     phone: str = None
#     address: dict = None

#     @staticmethod
#     def from_doc(doc):
#         return Employee(
#             id=str(doc["_id"]),
#             firstname=str(doc["firstname"]),
#             lastname=str(doc["lastname"]),
#             employee_id=str(doc["employee_id"]),
#             phone=str(doc["phone"]),
#             address=doc["address"],
#         )


class ToDoDAL:
    def __init__(self, hotel_collection: AsyncIOMotorCollection):
        self._hotel_collection = hotel_collection

    # Customer section

    async def create_customer(  # Create customer
        self,
        firstname: str = None,
        lastname: str = None,
        id: str = None,
        phone: str = None,
        nationality: str = None,
        status: bool = None,
        room: int = None,
        session=None,
    ) -> str:
        response = await self._hotel_collection.insert_one(
            {
                "firstname": firstname,
                "lastname": lastname,
                "id": id,
                "phone": phone,
                "nationality": nationality,
                "status": status,
                "room": room,
            },
            session=session,
        )
        return str(response.inserted_id)

    async def get_customer(  # Find customer
        self,
        id: str = None,
        session=None,
    ) -> Customer:
        doc = await self._hotel_collection.find_one(
            {
                "id": id,
            },
            session=session,
        )
        return Customer.from_doc(doc)

    async def update_customer(  # Update customer
        self,
        id: str = None,
        session=None,
    ) -> Customer:
        doc = await self._hotel_collection.find_one(
            {
                "id": id,
            },
            session=session,
        )
        return Customer.from_doc(doc)

    async def delete_customer(  # Delete customer
        self,
        id: str = None,
        session=None,
    ) -> bool:
        response = await self._hotel_collection.delete_one(
            {
                "id": id,
            },
            session=session,
        )
        return response.deleted_count == 1

    # Room section

    async def create_room(
        self, number: int = None, type: str = None, status: str = None, session=None
    ) -> str:
        response = await self._hotel_collection.insert_one(
            {"number": number, "type": type, "status": status}, session=session
        )
        return str(response.inserted_id)

    async def update_room(self, number: int = None, session=None) -> Room:
        doc = await self._hotel_collection.find_one({"number": number}, session=session)
        return Room.from_doc(doc)

    async def get_room(self, number: int = None, session=None) -> Room:
        doc = await self._hotel_collection.find_one({"number": number}, session=session)
        return Room.from_doc(doc)

    async def delete_room(self, number: int = None, session=None) -> bool:
        response = await self._hotel_collection.delete_one(
            {"number": number}, session=session
        )
        return response.deleted_count == 1

    # Reservation section
