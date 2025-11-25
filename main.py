from fastapi import FastAPI, Body, status, HTTPException
from fastapi.responses import RedirectResponse

from contextlib import asynccontextmanager

from database.db import engine
from database.models import Base

from service import generate_short_url, get_url_by_slug

from exception import CustomSlugNotValid, NotFoundLongUrl, SlugAlredyExistError, URLNotValid

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)



@app.post("/short_url")
async def generate_slug(long_url: str, custom_slug: str = None):
    try:
        new_slug = await generate_short_url(long_url, custom_slug)
        return {"data":new_slug}
    
    except SlugAlredyExistError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except URLNotValid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL not valid")
    except CustomSlugNotValid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Custom short URL not valid")


@app.get("/{slug}")
async def redirect_to_url(slug: str):
    try:
        long_url = await get_url_by_slug(slug)
    except NotFoundLongUrl:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)