from curse_api import SimpleCurseAPI, CurseAPI
from curse_api.clients.aiohttp import AiohttpFactory
from curse_api.clients.httpx import HttpxFactory
import pytest
import os


@pytest.mark.asyncio
@pytest.mark.parametrize("factory", [HttpxFactory, AiohttpFactory])
async def test_curseapi(factory):
    id = 285109
    async with CurseAPI(factory(os.environ["CF_API_KEY"])) as api:  # type: ignore
        mod = await api.get_mod(id)
        assert mod.id == id, "Invalid modid"


@pytest.mark.asyncio
@pytest.mark.parametrize("factory", [HttpxFactory, AiohttpFactory])
async def test_simplecurseapi(factory):
    id = 285109
    async with SimpleCurseAPI(os.environ["CF_API_KEY"], factory=factory) as api:  # type: ignore
        mod = await api.get_mod(id)
        assert mod.id == id, "Invalid modid"
