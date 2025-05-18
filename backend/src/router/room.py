from fastapi import APIRouter, Depends

from dal.room import Room, RoomDAL

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


"""
Create new room
"""


@router.post("/api/rooms/new")
async def create_new_room(
    number: int,
    type: str,
    status: str,
    dal: RoomDAL = Depends(lambda: router.app.room_dal),
) -> str:
    return await dal.create_room(number=number, type=type, status=status)


"""
List all rooms
"""


@router.get("/api/rooms")
async def list_rooms(dal: RoomDAL = Depends(lambda: router.app.room_dal)):
    return await dal.list_rooms()


"""
Show room info
"""


@router.get("/api/rooms/{room_number}")
async def show_room(
    room_number: int, dal: RoomDAL = Depends(lambda: router.app.room_dal)
) -> Room:
    return await dal.get_room(room_number)


"""
Update room
"""


@router.put("/api/rooms/{room_number}")
async def update_room(
    room_number: int, status: str, dal: RoomDAL = Depends(lambda: router.app.room_dal)
):
    return await dal.update_room(number=room_number)


"""
Delete room
"""


@router.delete("/api/rooms/{room_number}")
async def delete_room(
    room_number: int, dal: RoomDAL = Depends(lambda: router.app.room_dal)
):
    return await dal.delete_room(number=room_number)
