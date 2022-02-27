from pydantic import BaseModel


class SignUpCustomerRequestDto(BaseModel):
    document: str
    name: str
    birth_date: str
    email: str
    phone: str
