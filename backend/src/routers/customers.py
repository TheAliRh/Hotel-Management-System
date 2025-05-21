from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from dal.customer import Customer, CustomerDAL


router = APIRouter(prefix="/api/customers", tags=["customers"])


"""
Base validation models
"""


class CustomerCreate(BaseModel):
    firstname: str = Field(..., ge=2, le=20)
    lastname: str = Field(..., ge=2, le=20)
    customer_id: str = Field(..., ge=10, le=10)
    phone: str = Field(..., ge=8, le=12)
    nationality: str = Field(..., ge=4, le=20)


class CustomerUpdate(BaseModel):
    firstname: str = Field(..., ge=2, le=20)
    lastname: str = Field(..., ge=2, le=20)
    customer_id: str = Field(..., ge=10, le=10)
    phone: str = Field(..., ge=8, le=12)
    nationality: str = Field(..., ge=4, le=20)
    customer_status: str = Field(..., regex="^(inactive|present|absent)$")


# -----------Endpoints----------


"""
Create new customer
"""


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_customer(
    customer: CustomerCreate,
    dal: CustomerDAL = Depends(lambda: router.app.customer_dal),
) -> str:
    customer_status = "present"
    return await dal.create_customer(
        firstname=customer.firstname,
        lastname=customer.lastname,
        customer_id=customer.customer_id,
        phone=customer.phone,
        nationality=customer.nationality,
        customer_status=customer_status,
    )


"""
List all customers
"""


@router.get("", status_code=status.HTTP_200_OK, response_model=list[Customer])
async def get_customers(
    dal: CustomerDAL = Depends(lambda: router.app.customer_dal),
) -> list:
    return await dal.list_customers()


"""
Show customer
"""


@router.get("/{customer_id}", status_code=status.HTTP_200_OK, response_model=Customer)
async def get_customer(
    customer_id: str, dal: CustomerDAL = Depends(lambda: router.app.customer_dal)
) -> Customer:
    return await dal.get_customer(customer_id)


"""
Update customer
"""


@router.put("/{customer_id}", status_code=status.HTTP_200_OK, response_model=Customer)
async def update_customer(
    payload: CustomerUpdate,
    dal: CustomerDAL = Depends(lambda: router.app.customer_dal),
) -> Customer:
    return await dal.update_customer(customer_id=payload.customer_id)


"""
Delete customer
"""


@router.delete(
    "/{customer_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=bool
)
async def delete_customer(
    id: int,
    customer_id: str,
    dal: CustomerDAL = Depends(lambda: router.app.customer_dal),
) -> bool:
    return await dal.delete_customer(customer_id)
