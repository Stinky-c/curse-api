try:
    import aiohttp
except ImportError:
    raise Exception("HTTPX is not installed")

from typing import Dict, Any, Optional, AsyncIterator

from ..abc import APIFactory

__all__ = [
    "AiohttpFactory",
]


class AiohttpFactory(APIFactory):
    """An httpx impl for APIfactory"""

    def __init__(self, api_key: str, base_url: str, user_agent: str) -> None:
        """A basic factory handling API requests
            CurseAPI will accept a subclass, but have `_get` and `_post` methods


        Args:
            api_key (str): A valid CurseForge API key
            base_url (str): The base URL for handling requests
            user_agent (str): A user agent for requests
            settings: extra httpx settings
        """

        _headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "user-agent": user_agent,
        }
        self._sess = aiohttp.ClientSession(
            base_url=base_url,
            headers=_headers,
        )
        self._sess.trace_configs

    async def close(self):
        await self._sess.close()

    async def get(
        self, url: str, params: Optional[dict] = None, **kwargs
    ) -> Dict[Any, Any]:
        """get method

        Args:
            url (str): the url to get
            params (dict): a dict of parameters
            kwargs (any): unpacked into requests get method
        """
        res = await self._sess.get(url, params=params, **kwargs)
        res.raise_for_status()
        return await res.json()

    async def post(
        self, url: str, params: Optional[dict] = None, **kwargs
    ) -> Dict[Any, Any]:
        """post method

        Args:
            url (str): the url to get
            params (dict): the json data to send
            kwargs (any): unpacked into requests get method
        """
        res = await self._sess.post(url, json=params, **kwargs)
        res.raise_for_status()
        return await res.json()

    async def download(self, url: str, chunk_size: int) -> AsyncIterator[bytes]:
        res = await self._sess.get(url, allow_redirects=True)
        res.raise_for_status()
        return res.content.iter_chunked(chunk_size)

    @property
    def session(self):
        return self._sess
