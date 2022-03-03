import datetime
from typing import Optional

from pydantic import BaseModel


class UpdateCustomerRequestDto(BaseModel):
    id: Optional[str] = None
    document: Optional[str]
    name: Optional[str]
    birth_date: Optional[datetime.date]
    email: Optional[str]
    phone: Optional[str]
    is_active: Optional[bool]
