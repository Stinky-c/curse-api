from curse_api import Games, CurseAPI
from curse_api.models import Mod, Pagination
import pytest


@pytest.mark.asyncio
async def test_health_check(api: CurseAPI):
    res = await api.health_check()
    assert res.status_code == 200, "API unavailable"


@pytest.mark.asyncio
async def test_get_mod(api: CurseAPI):
    id = 285109
    res = await api.get_mod(id)
    assert isinstance(res, Mod), "Invalid type"
    res.download_latest
    assert res.id == id, "Invalid ID"


@pytest.mark.asyncio
async def test_get_mods(api: CurseAPI):
    id = 285109
    res = await api.get_mods([id, 452013])
    assert isinstance(res, list), "Not a list"
    assert len(res) > 0, " Does not contain mods"
    assert res[0].id == id, "Got the wrong mod"


@pytest.mark.asyncio
async def test_search_mods_slug(api: CurseAPI):
    res, page = await api.search_mods(Games.Minecraft, slug="jei")
    assert isinstance(res, list), "Not a list"
    assert len(res) > 0, "No mods in list"
    assert isinstance(page, Pagination), "Invalid Pagination"


@pytest.mark.asyncio
async def test_search_mods_page_size(api: CurseAPI):
    res, page = await api.search_mods(Games.Minecraft, slug="jei", pageSize=5)
    assert page.pageSize <= 5, "Page data is too long"
    assert page.resultCount == len(res), "The api returned invalid page data"


# TODO find API banned mod
# async def test_invalid_mod_files(api:AsyncCurseAPI):
#     with pytest.raises(APIBanned):
#         res = api.get_mod_file(247217, 2740774)
#         res.download()
