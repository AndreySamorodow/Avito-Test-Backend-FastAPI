from httpx import AsyncClient

slug = None

async def test_generate_slug(ac: AsyncClient):
    result = await ac.post("/short_url", json={"long_url": "https://my-sitetest.com"})
    global slug
    slug = result
    assert result.status_code == 200


#async def test_redirect_to_url(ac: AsyncClient):
    #result = await ac.get(f"/{slug}")
    #assert result.status_code == 302
   