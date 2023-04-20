from curse_api import Games, SimpleCurseAPI
from curse_api.models import Mod, Pagination
from curse_api.categories import Minecraft_Categories
import pytest


@pytest.mark.asyncio
async def test_get_mod(api: SimpleCurseAPI):
    id = 285109
    res = await api.get_mod(id)
    assert isinstance(res, Mod), "Invalid type"
    assert res.id == id, "Invalid ID"


@pytest.mark.asyncio
async def test_get_mods(api: SimpleCurseAPI):
    id = 285109
    res = await api.get_mods([id, 452013])
    assert isinstance(res, list), "Not a list"
    assert len(res) > 0, " Does not contain mods"
    assert res[0].id == id, "Got the wrong mod"


@pytest.mark.asyncio
async def test_search_mods_slug(api: SimpleCurseAPI):
    res, page = await api.search_mods(Games.minecraft, slug="jei")
    assert isinstance(res, list), "Not a list"
    assert len(res) > 0, "No mods in list"
    assert isinstance(page, Pagination), "Invalid Pagination"


@pytest.mark.asyncio
async def test_search_mods_page_size(api: SimpleCurseAPI):
    res, page = await api.search_mods(Games.minecraft, slug="jei", pageSize=5)
    assert page.pageSize <= 5, "Page data is too long"
    assert page.resultCount == len(res), "The api returned invalid page data"


@pytest.mark.asyncio
async def test_search_mods_category(api: SimpleCurseAPI):
    res, _ = await api.search_mods(
        Games.minecraft,
        slug="multiblock-madness",
        categoryId=Minecraft_Categories.modpacks,
    )


@pytest.mark.asyncio
async def test_mod_page_url(api: SimpleCurseAPI):
    mcmod = await api.get_mod(388909)
    assert (
        mcmod.modPageURL == "https://www.curseforge.com/minecraft/mc-mods/explosiont"
    ), "Invalid Minecraft Mod Page URL"

    wowmod = await api.get_mod(688930)
    assert (
        wowmod.modPageURL
        == "https://www.curseforge.com/wow/addons/advanced-raid-frame-settings"
    ), "Invalid WoW Mod Page URL"

    simsmod = await api.get_mod(810784)
    assert (
        simsmod.modPageURL
        == "https://www.curseforge.com/sims4/build-buy/garden-at-home-pack"
    ), "Invalid Sims Mod Page URL"


# TODO find API banned mod
# async def test_invalid_mod_files(api:AsyncSimpleCurseAPI):
#     with pytest.raises(APIBanned):
#         res = api.get_mod_file(247217, 2740774)
#         res.download()
