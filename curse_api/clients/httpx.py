try:
    import httpx
    from httpx._config import DEFAULT_TIMEOUT_CONFIG
    from httpx._types import TimeoutTypes
except ImportError:
    from ..errors import MissingImportException

    raise MissingImportException("missing httpx")

from typing import Dict, Any, Optional, AsyncIterator

from ..abc import APIFactory


class HttpxFactory(APIFactory):
    """An httpx impl for APIfactory"""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        user_agent: str,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    ) -> None:
        """A basic factory handling API requests using httpx


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
        self._sess = httpx.AsyncClient(
            base_url=base_url,
            headers=_headers,
            timeout=timeout,
        )

    async def close(self):
        await self._sess.aclose()

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
        return res.json()

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
        return res.json()

    async def download(self, url: str, chunk_size: int) -> AsyncIterator[bytes]:
        res = await self._sess.get(url, follow_redirects=True)
        res.raise_for_status()
        return res.aiter_bytes(chunk_size)

    @property
    def session(self):
        return self._sess
