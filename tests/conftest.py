from curse_api import CurseAPI
from curse_api.clients.httpx import HttpxFactory
from curse_api.clients.aiohttp import AiohttpFactory
from curse_api.ext import ManifestParser
import os
import pytest
import asyncio
from dotenv import load_dotenv

load_dotenv()


# TODO: fix event loop closing early
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", params=[HttpxFactory, AiohttpFactory])
async def api(request):
    async with CurseAPI(os.environ["CF_API_KEY"], factory=request.param) as api:
        yield api
        await api.close()


@pytest.fixture(scope="session")
async def manifest_parser(api: CurseAPI):
    yield ManifestParser(api)
