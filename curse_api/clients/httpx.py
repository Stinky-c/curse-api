try:
    import httpx
except ImportError:
    raise Exception("HTTPX is not installed")

from typing import Dict, Any, Optional, AsyncIterator

from ..abc import APIFactory


class HttpxFactory(APIFactory):
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
        self._sess = httpx.AsyncClient(
            base_url=base_url,
            headers=_headers,
        )
        # read timeout overide because getting json data takes a while some times
        # switch to different json parser?
        todict = self._sess.timeout.as_dict()
        todict["read"] = 15
        self._sess.timeout = httpx.Timeout(**todict)

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
        res = await self._sess.get(url,follow_redirects=True)
        res.raise_for_status()
        return res.aiter_bytes(chunk_size)

    @property
    def session(self):
        return self._sess


'''
    def set_request_hook(self, func: Callable):
        """
        uses httpx event hooks
        func must take a request object
        https://www.python-httpx.org/advanced/#event-hooks
        """
        self._sess.event_hooks["request"] += [func]

    def pop_request_hooks(self) -> List[Callable]:
        """
        pops all request hooks
        """
        r, self._sess.event_hooks["request"][:] = (
            self._sess.event_hooks["request"][:],
            [],
        )
        return r

    def set_response_hook(self, func: Callable):
        """
        uses httpx event hooks
        func must take a response object
        https://www.python-httpx.org/advanced/#event-hooks
        """
        self._sess.event_hooks["response"] += [func]

    def pop_response_hooks(self) -> List[Callable]:
        """
        pops all response hooks
        """
        r, self._sess.event_hooks["response"][:] = (
            self._sess.event_hooks["response"][:],
            [],
        )
        return r

    @property
    def response_hooks(self) -> List[Callable]:
        """response event hooks"""
        return self._sess.event_hooks["response"]

    @property
    def request_hooks(self) -> List[Callable]:
        """request event hooks"""
        return self._sess.event_hooks["request"]

    @property
    def client_timeout(self) -> httpx.Timeout:
        return self._sess.timeout

    def set_client_timeout(
        self, read: float = 5, connect: float = 5, pool: float = 5, default: float = 5
    ):
        """Sets the clients timeouts
        https://www.python-httpx.org/advanced/#timeout-configuration
        """
        self._sess.timeout = httpx.Timeout(
            default, read=read, connect=connect, pool=pool
        )

'''
