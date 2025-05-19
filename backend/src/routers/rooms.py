from fastapi import APIRouter, Depends

from dal.room import Room, RoomDAL

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


"""
Create new room
"""


@router.post("/new", response_model=str)
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


@router.get("", response_model=list[Room])
async def list_rooms(dal: RoomDAL = Depends(lambda: router.app.room_dal)) -> Room:
    return await dal.list_rooms()


"""
Show room info
"""


@router.get("/{room_number}", response_model=Room)
async def show_room(
    room_number: int, dal: RoomDAL = Depends(lambda: router.app.room_dal)
) -> Room:
    return await dal.get_room(room_number)


"""
Update room
"""


@router.put("/{room_number}", response_model=Room)
async def update_room(
    room_number: int, status: str, dal: RoomDAL = Depends(lambda: router.app.room_dal)
) -> Room:
    return await dal.update_room(number=room_number)


"""
Delete room
"""


@router.delete("/{room_number}", response_model=bool)
async def delete_room(
    room_number: int, dal: RoomDAL = Depends(lambda: router.app.room_dal)
) -> bool:
    return await dal.delete_room(number=room_number)
