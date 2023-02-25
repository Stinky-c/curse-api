from curse_api import CurseAPI
import os
import pytest
import asyncio
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def api(event_loop: asyncio.AbstractEventLoop):
    api = CurseAPI(os.environ["CF_API_KEY"], timeout=8)
    yield api
    event_loop.run_until_complete(api.close())
