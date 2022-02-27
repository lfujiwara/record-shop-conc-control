import datetime

from pydantic import BaseModel


class UpdateCustomerRequestDto(BaseModel):
    id: str = None
    document: str
    name: str
    birth_date: datetime.date
    email: str
    phone: str
    is_active: bool
