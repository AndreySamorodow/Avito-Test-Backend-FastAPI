from src.database.crud import add_slug_to_database, get_long_url_by_slug_from_database
from src.shortener import generate_random_slug
from src.exception import NotFoundLongUrl, SlugAlredyExistError, URLNotValid, CustomSlugNotValid
import validators

from sqlalchemy.ext.asyncio import AsyncSession

async def generate_short_url(long_url: str, session: AsyncSession, custom_slug: str = None) -> str:
    if not validators.url(long_url):
        raise URLNotValid

    if custom_slug is not None:
        if len(custom_slug) != 6:
            raise CustomSlugNotValid
        
        existing_url = await get_long_url_by_slug_from_database(custom_slug, session)
        if existing_url:
            raise SlugAlredyExistError
        
        await add_slug_to_database(custom_slug, long_url, session)
        return custom_slug

    for attempt in range(5):
        slug = generate_random_slug()
        
        existing_url = await get_long_url_by_slug_from_database(slug, session)
        if not existing_url:
            await add_slug_to_database(slug, long_url, session)
            return slug
            
        if attempt == 4:
            raise SlugAlredyExistError("Could not generate unique slug after 5 attempts")
    
    return slug
    

async def get_url_by_slug(slug:str, session: AsyncSession) -> str:
    long_url = await get_long_url_by_slug_from_database(slug, session)
    if not long_url:
        raise NotFoundLongUrl()
    return long_url
