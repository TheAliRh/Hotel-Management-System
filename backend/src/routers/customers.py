from fastapi import APIRouter, Depends, status

from dal.customer import Customer, CustomerDAL


router = APIRouter(prefix="/api/customers", tags=["customers"])


"""
Create new customer
"""


@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=Customer)
async def create_customer(
    firstname: str,
    lastname: str,
    id: str,
    phone: str,
    nationality: str,
    new_customer: Customer,
    dal: CustomerDAL = Depends(lambda: router.app.customer_dal),
) -> Customer:
    new_customer.status = "present"
    return await dal.create_customer(
        firstname, lastname, id, phone, nationality, new_customer.status
    )


"""
List all customers
"""


@router.get("", status_code=status.HTTP_200_OK, response_model=list[Customer])
async def get_customers(
    dal: CustomerDAL = Depends(lambda: router.app.customer_dal),
) -> Customer:
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
    customer_id: str,
    firstname: str,
    lastname: str,
    id: str,
    nationality: str,
    customer_status: str,
    dal: CustomerDAL = Depends(lambda: router.app.customer_dal),
) -> Customer:
    return await dal.update_customer(customer_id)


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
