from fastapi import APIRouter, Depends

from dal.customer import Customer, CustomerDAL


router = APIRouter(prefix="/api/customers", tags=["customers"])


"""
Create new customer
"""


@router.post("/api/customers/new")
async def post_customer(
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


@router.get("/api/customers")
async def get_customers(dal: CustomerDAL = Depends(lambda: router.app.customer_dal)):
    return await dal.list_customers()


"""
Show customer
"""


@router.get("/api/customers/{customer_id}")
async def get_customer_by_id(
    customer_id: int, dal: CustomerDAL = Depends(lambda: router.app.customer_dal)
) -> Customer:
    return await dal.get_customer(customer_id)


"""
Update customer
"""


@router.put("/api/customers/{customer_id}")
async def update_customer(
    customer_id: str,
    firstname: str,
    lastname: str,
    id: str,
    nationality: str,
    status: str,
    dal: CustomerDAL = Depends(lambda: router.app.customer_dal),
):
    return await dal.update_customer(customer_id)


"""
Delete customer
"""


@router.delete("/api/customers/{customer_id}")
async def delete_customer(
    id: int,
    customer_id: str,
    dal: CustomerDAL = Depends(lambda: router.app.customer_dal),
):
    return await dal.delete_customer(customer_id)
