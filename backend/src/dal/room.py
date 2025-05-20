"""
Isolated data access layer of rooms.
"""

from fastapi import HTTPException, status
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorCollection


# -------Model--------


class Room(BaseModel):
    number: int = None
    type: str = None
    room_status: bool = None  # Empty=True, Full=False

    @staticmethod
    def from_doc(doc):
        return Room(
            number=int(doc["number"]),
            type=str(doc["type"]),
            room_status=bool(doc["status"]),
        )


# ---------DAL--------


class RoomDAL:
    def __init__(self, room_collection: AsyncIOMotorCollection):
        self._room_collection = room_collection

    """
    Create room
    """

    async def create_room(
        self,
        number: int = None,
        type: str = None,
        room_status: str = None,
        session=None,
    ) -> str:
        existing = await self._room_collection.find_one({"number": number})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Room number '{number}' already exists.",
            )
        response = await self._room_collection.insert_one(
            {"number": number, "type": type, "status": room_status}, session=session
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
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room '{number}' not found.",
            )
        return Room.from_doc(doc)

    """
    Update room
    """

    async def update_room(self, number: int = None, session=None) -> Room:
        doc = await self._room_collection.update_one(
            {"number": number}, session=session
        )
        if doc.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room '{number}' not found.",
            )
        return Room.from_doc(doc)

    """
    Delete room
    """

    async def delete_room(self, number: int = None, session=None) -> bool:
        response = await self._room_collection.delete_one(
            {"number": number}, session=session
        )
        if response.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room '{number}' not found.",
            )

        return response.deleted_count == 1
