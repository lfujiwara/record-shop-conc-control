from fastapi import FastAPI, Depends, HTTPException

from api.deps import deps
from lea_record_shop.services.disc_crud import CreateDiscRequestDto, DiscCrud

app = FastAPI()


@app.get("/")
def hello():
    return "hello"


@app.post("/discs")
async def create_disc(data: CreateDiscRequestDto, crud_svc: DiscCrud = Depends(deps)):
    return await crud_svc.create_disc(data)


@app.get("/discs/{_id}")
async def get_disc(_id: str, crud_svc: DiscCrud = Depends(deps)):
    result = await crud_svc.get_disc(_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Disc not found")
    return result
