from pydantic import BaseModel


class PlacePurchaseOrderRequestDto(BaseModel):
    disc_id: str
    customer_id: str
    quantity: int
