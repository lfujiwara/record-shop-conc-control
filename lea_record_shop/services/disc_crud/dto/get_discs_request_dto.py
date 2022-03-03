from typing import Optional

from pydantic import BaseModel


class GetDiscsRequestDto(BaseModel):
    name: Optional[str] = None
    name_exact: Optional[str] = None
    artist: Optional[str] = None
    artist_exact: Optional[str] = None
    year_of_release_min: Optional[int] = None
    year_of_release_max: Optional[int] = None
    genre: Optional[str] = None
    genre_exact: Optional[str] = None

    offset: int = 0
    limit: int = 20
