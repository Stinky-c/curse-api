from curse_api import CurseAPI
import os
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def api():
    yield CurseAPI(os.environ["CF_API_KEY"], timeout=8)
