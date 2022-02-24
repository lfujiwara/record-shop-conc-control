from pydantic import BaseModel


class UpdateDiscRequestDto(BaseModel):
    id: str = None
    name: str
    artist: str
    year_of_release: int
    genre: str
    quantity: int
