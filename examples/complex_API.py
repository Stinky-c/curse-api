from curse_api import CurseAPI
from curse_api.abc import APIFactory
from typing import Any, Optional, Dict, AsyncIterator

"""
A theoretical class for a http client
not intended to run
"""


class HttpClient(APIFactory):  # APIfactory defines the required methods
    def __init__(self, client) -> None:  # can be any http client
        self._client = client

    """
    The builtin clients natively supported follow this flow
    but user made classes may follow a different stragey as long as only valid data is passed on
    """

    async def get(self, url: str, params: Optional[dict] = None) -> Dict[Any, Any]:
        response = await self._client.get(url, params)  # fetch data
        response.raise_for_status()  # error handle
        return response.to_json()  # return a dict of data

    async def post(self, url: str, params: Optional[dict] = None) -> Dict[Any, Any]:
        response = await self._client.get(url, params)
        response.raise_for_status()
        return response.to_json()

    async def download(self, url: str, chunk_size: int) -> AsyncIterator[bytes]:
        response = await self._client.get(url, allow_redirects=True)
        response.raise_for_status()
        return response.aiter_bytes(chunk_size)

    async def close(self):
        await self._client.close()


async def main():

    session = HttpClient(...)  # a premade http client

    # session is just a wrapper allowing `CurseAPI` to only handle data and not invalid http states
    api = CurseAPI(session)

    mod = await api.search_mods(slug="jei")

    await api.close()
