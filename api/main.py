from fastapi import FastAPI, Depends, HTTPException

from api.deps import deps
from lea_record_shop.services.disc_crud import CreateDiscRequestDto, DiscCrud, GetDiscsRequestDto, UpdateDiscRequestDto, \
    disc_crud_exceptions

app = FastAPI()


@app.post("/discs")
async def create_disc(data: CreateDiscRequestDto, crud_svc: DiscCrud = Depends(deps)):
    return await crud_svc.create_disc(data)


@app.get("/discs/{_id}")
async def get_disc(_id: str, crud_svc: DiscCrud = Depends(deps)):
    result = await crud_svc.get_disc(_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Disc not found")
    return result


@app.get("/discs")
async def get_discs(name_exact: str = None, name: str = None, artist_exact: str = None, artist: str = None,
                    genre_exact: str = None, genre: str = None, year_of_release_min: int = None,
                    year_of_release_max: int = None, offset: int = 0, limit: int = 100,
                    crud_svc: DiscCrud = Depends(deps)):
    params = GetDiscsRequestDto()
    params.name_exact = name_exact
    params.name = name
    params.artist_exact = artist_exact
    params.artist = artist
    params.genre_exact = genre_exact
    params.genre = genre
    params.year_of_release_min = year_of_release_min
    params.year_of_release_max = year_of_release_max
    params.offset = offset
    params.limit = limit

    return await crud_svc.get_discs(params)


@app.put("/discs/{_id}")
async def update_disc(_id: str, data: UpdateDiscRequestDto, crud_svc: DiscCrud = Depends(deps)):
    data.id = _id
    try:
        return await crud_svc.update_disc(data)
    except disc_crud_exceptions.RequestedDiscNotFound:
        # Re-raising here so that the application layer doesn't need to know sh**
        # about http status codes
        raise HTTPException(status_code=404, detail="Disc not found")


@app.delete("/discs/{_id}")
async def delete_disc(_id: str, crud_svc: DiscCrud = Depends(deps)):
    try:
        return await crud_svc.delete_disc(_id)
    except disc_crud_exceptions.RequestedDiscNotFound:
        raise HTTPException(status_code=404, detail="Disc not found")
