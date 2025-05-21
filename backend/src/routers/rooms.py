from fastapi import APIRouter, Depends, status

from dal.room import Room, RoomDAL

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


"""
Create new room
"""


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_new_room(
    number: int,
    type: str,
    room_status: str,
    dal: RoomDAL = Depends(lambda: router.app.room_dal),
) -> str:
    return await dal.create_room(number=number, type=type, room_status=room_status)


"""
List all rooms
"""


@router.get("", status_code=status.HTTP_200_OK, response_model=list[Room])
async def list_rooms(dal: RoomDAL = Depends(lambda: router.app.room_dal)) -> Room:
    return await dal.list_rooms()


"""
Show room info
"""


@router.get("/{room_number}", status_code=status.HTTP_200_OK, response_model=Room)
async def show_room(
    room_number: int, dal: RoomDAL = Depends(lambda: router.app.room_dal)
) -> Room:
    return await dal.get_room(room_number)


"""
Update room
"""


@router.put("/{room_number}", status_code=status.HTTP_200_OK, response_model=Room)
async def update_room(
    room_number: int,
    room_status: str,
    dal: RoomDAL = Depends(lambda: router.app.room_dal),
) -> Room:
    return await dal.update_room(number=room_number)


"""
Delete room
"""


@router.delete(
    "/{room_number}", status_code=status.HTTP_204_NO_CONTENT, response_model=bool
)
async def delete_room(
    room_number: int, dal: RoomDAL = Depends(lambda: router.app.room_dal)
) -> bool:
    return await dal.delete_room(number=room_number)
