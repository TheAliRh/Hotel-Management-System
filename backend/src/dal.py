# Data Access Layer (DAL)
# Responsible for handling interaction between database and application

from bson import ObjectId
from pymongo import ReturnDocument
from pydantic import BaseModel


class Room(BaseModel):
    number: int = None
    type: str = None
    status: bool = None  # Empty=True, Full=False


class Customer(BaseModel):
    firstname: str = None
    lastname: str = None
    id: str = None
    phone: str = None
    nationality: str = None
    status: bool = None  # Active=true, Inactive=False
    room: int = None


class Reservation(BaseModel):
    id: str = None
    firstname: str = None
    lastname: str = None
    customer_id: str = None
    checkin_date: str = None
    checkout_date: str = None
    room_number: int = None


class User(BaseModel):
    fullname: str = None
    phone: str = None
    username: str = None
    password: str = None


class Employee(BaseModel):
    id: str = None
    firstname: str = None
    lastname: str = None
    employee_id: str = None
    phone: str = None
    address: dict = None
