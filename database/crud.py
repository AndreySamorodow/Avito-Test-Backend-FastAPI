from database.db import new_session
from database.models import ShortURL

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from exception import SlugAlredyExistError


async def add_slug_to_database(slug: str, long_url: str):
    async with new_session() as session:
        new_slug = ShortURL(slug = slug, long_url=long_url)
        session.add(new_slug)
        try:
            await session.commit()
        except IntegrityError:
            raise SlugAlredyExistError
            

async def get_long_url_by_slug_from_database(slug: str):
    async with new_session() as session:
        query = select(ShortURL).filter_by(slug=slug)
        result = await session.execute(query)
        res: ShortURL | None = result.scalar_one_or_none()
        return res.long_url if res.long_url else None
