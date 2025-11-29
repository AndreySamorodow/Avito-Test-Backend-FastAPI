from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.exception import CustomSlugNotValid, NotFoundLongUrl, SlugAlredyExistError, URLNotValid

from database.db import engine, new_session
from database.models import Base
from sqlalchemy.ext.asyncio import AsyncSession

from src.service import generate_short_url, get_url_by_slug


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


class ShortUrlRequest(BaseModel):
    long_url: str
    custom_slug: str = None

@app.get("/")
async def root():
    return {"status": "ok", "message": "URL shortener API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/short_url")
async def generate_slug(
    request: ShortUrlRequest,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    try:
        new_slug = await generate_short_url(request.long_url, session, request.custom_slug)
        return {"data": new_slug}
    
    except SlugAlredyExistError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The slug is already in use")
    except URLNotValid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL not valid")
    except CustomSlugNotValid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Custom short URL not valid")

@app.get("/{slug}")
async def redirect_to_url(
    slug: str,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    try:
        long_url = await get_url_by_slug(slug, session)
    except NotFoundLongUrl:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)