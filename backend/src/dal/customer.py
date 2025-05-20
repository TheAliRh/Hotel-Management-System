"""
Isolated data access layer of customers.
"""

from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import HTTPException, status
from bson import ObjectId

# -----------Model----------


class Customer(BaseModel):
    firstname: str = None
    lastname: str = None
    id: str = None
    phone: str = None
    nationality: str = None
    customer_status: bool = None  # Active=true, Inactive=False
    room: int = None

    @staticmethod
    def from_doc(doc):
        return Customer(
            firstname=str(doc["firstname"]),
            lastname=str(doc["lastname"]),
            id=str(doc["id"]),
            phone=str(doc["phone"]),
            nationality=str(doc["nationality"]),
            customer_status=bool(doc["status"]),
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
        customer_status: bool = None,
        room: int = None,
        session=None,
    ) -> str:
        existing = await self._customer_collection.find_one({"id": id})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"customer with id '{id}' already exists.",
            )

        response = await self._customer_collection.insert_one(
            {
                "firstname": firstname,
                "lastname": lastname,
                "id": id,
                "phone": phone,
                "nationality": nationality,
                "status": customer_status,
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
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"customer id '{id}' not found.",
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
        doc = await self._customer_collection.update_one(
            {
                "id": id,
            },
            session=session,
        )
        if doc.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"customer id '{id}' not found.",
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
        if response.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"customer id '{id}' not found.",
            )
        return response.deleted_count == 1
