from pydantic import BaseModel


class CreateDiscRequestDto(BaseModel):
    name: str
    artist: str
    year_of_release: int
    genre: str
    quantity: int
