"""
Isolated data access layer of customers.
"""

from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

# -----------Model----------


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


# ---------DAL----------


class CustomerDAL:
    def __init__(self, customer_collection: AsyncIOMotorCollection):

        self._customer_collection = customer_collection

    """
    Create new customer
    """

    async def create_customer(
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
        response = await self._customer_collection.insert_one(
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

    """
    List customers
    """

    async def list_customers(self, session=None) -> Customer:
        doc = await self._customer_collection.find({}, {}, session=session)
        return Customer.from_doc(doc)

    """
    Show customer
    """

    async def get_customer(
        self,
        id: str | ObjectId = None,
        session=None,
    ) -> Customer:
        doc = await self._customer_collection.find_one(
            {
                "id": id,
            },
            session=session,
        )
        return Customer.from_doc(doc)

    """
    Update customer
    """

    async def update_customer(
        self,
        id: str = None,
        session=None,
    ) -> Customer:
        doc = await self._customer_collection.find_one(
            {
                "id": id,
            },
            session=session,
        )
        return Customer.from_doc(doc)

    """
    Delete customer
    """

    async def delete_customer(
        self,
        id: str = None,
        session=None,
    ) -> bool:
        response = await self._customer_collection.delete_one(
            {
                "id": id,
            },
            session=session,
        )
        return response.deleted_count == 1
