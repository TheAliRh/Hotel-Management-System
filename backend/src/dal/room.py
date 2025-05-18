"""
Isolated data access layer of rooms.
"""

from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection


# -------Model--------


class Room(BaseModel):
    number: int = None
    type: str = None
    status: bool = None  # Empty=True, Full=False

    @staticmethod
    def from_doc(doc):
        return Room(
            number=int(doc["number"]), type=str(doc["type"]), status=bool(doc["status"])
        )


# ---------DAL--------


class RoomDAL:
    def __init__(self, room_collection: AsyncIOMotorCollection):
        self._room_collection = room_collection

    """
    Create room
    """

    async def create_room(
        self, number: int = None, type: str = None, status: str = None, session=None
    ) -> str:
        response = await self._room_collection.insert_one(
            {"number": number, "type": type, "status": status}, session=session
        )
        return str(response.inserted_id)

    """
    List all rooms
    """

    async def list_rooms(self, session=None):
        doc = await self._room_collection.find({}, {}, session=session)
        return Room.from_doc(doc)

    """
    Show room
    """

    async def get_room(self, number: int = None, session=None) -> Room:
        doc = await self._room_collection.find_one({"number": number}, session=session)
        return Room.from_doc(doc)

    """
    Update room
    """

    async def update_room(self, number: int = None, session=None) -> Room:
        doc = await self._room_collection.find_one({"number": number}, session=session)
        return Room.from_doc(doc)

    """
    Delete room
    """

    async def delete_room(self, number: int = None, session=None) -> bool:
        response = await self._room_collection.delete_one(
            {"number": number}, session=session
        )
        return response.deleted_count == 1
