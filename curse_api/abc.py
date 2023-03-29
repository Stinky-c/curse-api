from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Optional, AsyncIterator


class APIFactory(metaclass=ABCMeta):
    """required types"""

    def __init__(self, api_key: str, base_url: str, user_agent: str, **kwargs) -> None:
        ...

    @abstractmethod
    async def close(self):
        ...

    @abstractmethod
    async def get(self, url: str, params: Optional[dict] = None) -> Dict[Any, Any]:
        ...

    @abstractmethod
    async def post(self, url: str, params: Optional[dict] = None) -> Dict[Any, Any]:
        ...

    @abstractmethod
    async def download(self, url: str, chunk_size: int) -> AsyncIterator[bytes]:
        ...
