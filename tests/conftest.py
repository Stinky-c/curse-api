from curse_api import AsyncCurseAPI
import os
import pytest
import asyncio
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def api():
    yield AsyncCurseAPI(os.environ["CF_API_KEY"], timeout=8)

@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()