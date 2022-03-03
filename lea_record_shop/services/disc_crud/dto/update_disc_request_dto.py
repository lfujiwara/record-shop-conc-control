from typing import Optional

from pydantic import BaseModel


class UpdateDiscRequestDto(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    artist: Optional[str]
    year_of_release: Optional[int]
    genre: Optional[str]
    quantity: Optional[int]
