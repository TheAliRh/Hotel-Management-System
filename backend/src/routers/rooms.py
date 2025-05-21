from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from dal.room import Room, RoomDAL


router = APIRouter(prefix="/api/rooms", tags=["rooms"])


"""
Base validation models
"""


class RoomCreate(BaseModel):
    number: int = Field(..., ge=1, le=1000)
    type: str = Field(..., min_length=2, max_length=10)
    room_status: str = Field(..., regex="^(available|occupied|reserved)$")


class RoomUpdate(BaseModel):
    room_status: str = Field(..., regex="^(available|occupied|reserved)$")


# ---------Endpoints---------


"""
Create new room
"""


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_new_room(
    room: RoomCreate,
    dal: RoomDAL = Depends(lambda: router.app.room_dal),
) -> str:
    return await dal.create_room(
        number=room.number, type=room.type, room_status=room.room_status
    )


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
    payload: RoomUpdate,
    dal: RoomDAL = Depends(lambda: router.app.room_dal),
) -> Room:
    return await dal.update_room(number=room_number, room_status=payload.room_status)


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
