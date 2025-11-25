from database.crud import add_slug_to_database, get_long_url_by_slug_from_database
from shortener import generate_random_slug
from exception import NotFoundLongUrl, SlugAlredyExistError

async def generate_short_url(long_url:str) -> str:
    async def generate(long_url:str):
        slug = generate_random_slug()
        await add_slug_to_database(slug, long_url)
        return slug

    for attempt in range(5):
        try:
            slug = await generate(long_url)
            return slug
        except SlugAlredyExistError as ex:
            if attempt == 4:
                raise SlugAlredyExistError from ex
    return slug
            



    

async def get_url_by_slug(slug:str) -> str:
    long_url = await get_long_url_by_slug_from_database(slug)
    if not long_url:
        raise NotFoundLongUrl()
    return long_url