from pydantic import BaseModel


class GetDiscsRequestDto(BaseModel):
    name: str = None
    name_exact: str = None
    artist: str = None
    artist_exact: str = None
    year_of_release_min: int = None
    year_of_release_max: int = None
    genre: str = None
    genre_exact: str = None

    offset: int = 0
    limit: int = 20
