from typing import Callable, List, Optional, Type, Tuple

import httpx

from .enums import (
    Games,
    MinecraftCategories,
    ModLoaderType,
    ModsSearchSortField,
    SortOrder,
)
from .models import (
    File,
    FingerprintsMatchesResult,
    MinecraftGameVersion,
    MinecraftModLoaderIndex,
    MinecraftModLoaderVersion,
    Mod,
    Pagination,
    BaseCurseModel,
)

"""
TODO: write more doc strings
IDEA: make APIFactory a class with class methods and class variables
"""


class APIFactory:
    def __init__(
        self, api_key: str, base_url: str, user_agent: str, **settings
    ) -> None:
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
            **settings,
        )
        # read timeout overide because getting json data takes a while some times
        # switch to different json parser?
        todict = self._sess.timeout.as_dict()
        todict["read"] = 15
        self._sess.timeout = httpx.Timeout(**todict)

    async def close(self):
        await self._sess.aclose()
        ...

    async def _get(
        self, url: str, params: Optional[dict] = None, **kwargs
    ) -> httpx.Response:
        """internal get method

        Args:
            url (str): the url to get
            params (dict): a dict of parameters
            kwargs (any): unpacked into requests get method
        """
        res = await self._sess.get(url, params=params, **kwargs)
        return res

    async def _post(
        self, url: str, params: Optional[dict] = None, **kwargs
    ) -> httpx.Response:
        """internal post method

        Args:
            url (str): the url to get
            params (dict): the json data to send
            kwargs (any): unpacked into requests get method
        """
        res = await self._sess.post(url, json=params, **kwargs)
        return res

    @property
    def session(self):
        return self._sess

    def set_request_hook(self, func: Callable):
        """
        uses httpx event hooks
        func must take a request object
        https://www.python-httpx.org/advanced/#event-hooks
        """
        self._sess.event_hooks["request"] += [func]
        pass

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


class CurseAPI:
    """The main class for api requests.
    Cannot handle the download of API banned mods

    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.curseforge.com",
        user_agent: str = "stinky-c/curse-api",
        factory: Type[APIFactory] = APIFactory,
        # loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(), # Do I really need this?
        **settings,
    ) -> None:
        self._api: APIFactory = factory(
            api_key=api_key, base_url=base_url, user_agent=user_agent, **settings
        )
        """The main factory for handling requests
        accepts additional kwargs passing to the creation of the factory

        Args:
            API_KEY (str): Required. get one from here: https://docs.curseforge.com/#accessing-the-service.
            API_BASE (str, optional): An overide of the url base. Defaults to "https://api.curseforge.com".
            user_agent (str, optional): user_agent used for requests. Defaults to "stinky-c/curse-api".
            factory (APIFactory): a factory for handling API requests Defaults to APIFactory.
        """

    @property
    def api(self):
        return self._api

    async def health_check(self, **k) -> httpx.Response:
        res = await self._api._get("/")
        return res

    async def minecraft_versions(self) -> List[MinecraftGameVersion]:
        """Returns all minecraft version data from curseforge.
        Use `get_specific_minecraft_version` with the game version string to get more detailed data.
        """
        res = await self._api._get("/v1/minecraft/version")
        res.raise_for_status()
        return self.hydrate_list(res.json()["data"], MinecraftGameVersion)

    async def get_specific_minecraft_version(
        self, gameVersionString: str
    ) -> MinecraftGameVersion:
        res = await self._api._get(f"/v1/minecraft/version/{gameVersionString}")
        res.raise_for_status()
        return self.hydrate(res.json()["data"], MinecraftGameVersion)

    async def modloader_versions(self) -> List[MinecraftModLoaderIndex]:
        """
        Returns all minecraft modloader data from curseforge.
        Use `get_specific_minecraft_modloader` with the slug to get more detailed data.
        """
        res = await self._api._get(
            "/v1/minecraft/modloader", params={"includeAll": True}
        )
        res.raise_for_status()
        return self.hydrate_list(res.json()["data"], MinecraftModLoaderIndex)

    async def get_specific_minecraft_modloader(
        self, modLoaderName: str
    ) -> MinecraftModLoaderVersion:
        res = await self._api._get(f"/v1/minecraft/modloader/{modLoaderName}")
        res.raise_for_status()
        return self.hydrate(res.json()["data"], MinecraftModLoaderVersion)

    async def search_mods(
        self,
        gameId: Games = Games.Minecraft,
        classId: Optional[int] = None,
        categoryId: Optional[MinecraftCategories] = None,
        gameVersion: Optional[str] = None,
        searchFilter: Optional[str] = None,
        sortField: Optional[ModsSearchSortField] = None,
        sortOrder: Optional[SortOrder] = None,
        modLoaderType: Optional[ModLoaderType] = None,
        gameVersionTypeId: Optional[int] = None,
        slug: Optional[str] = None,
        index: Optional[int] = 0,
        pageSize: Optional[int] = 50,
    ) -> Tuple[List[Mod], Pagination]:
        """https://docs.curseforge.com/#search-mods


        Args:
            gameId (Games, optional): Filter by game id. Defaults to `Games.Minecraft`.
            classId (int, optional): Filter by section id (discoverable via Categories). Defaults to None.
            categoryId (MinecraftCategories, optional): Filter by category id. Defaults to None.
            gameVersion (str, optional): Filter by game version string. Defaults to None.
            searchFilter (str, optional): Filter by free text search in the mod name and author. Defaults to None.
            sortField (ModsSearchSortField, optional): Filter by `ModsSearchSortField` enumeration. Defaults to None.
            sortOrder (SortOrder, optional): Filter by `SortOrder` enumeration. Defaults to None.
            modLoaderType (ModLoaderType, optional): Filter only mods associated to a given modloader. Must be coupled with gameVersion. Defaults to None.
            gameVersionTypeId (int, optional): Filter only mods that contain files tagged with versions of the given gameVersionTypeId. Defaults to None.
            slug (str, optional): Filter by slug (coupled with classId will result in a unique result). Defaults to None.
            index (int, optional): A zero based index of the first item to include in the response. Defaults to 0.
            pageSize (int, optional): The number of items to include in the response. Defaults to 50.

        Returns:
            tuple[List[Mod], Pagination]: A List of mods and pagination data
        """
        build = {
            "gameId": gameId.value,
            "classId": classId,
            "categoryId": categoryId,
            "gameVersion": gameVersion,
            "searchFilter": searchFilter,
            "sortField": sortField,
            "sortOrder": sortOrder,
            "modLoaderType": modLoaderType,
            "gameVersionTypeId": gameVersionTypeId,
            "slug": slug,
            "index": index,
            "pageSize": pageSize,
        }

        res = await self._api._get(
            "/v1/mods/search",
            params={k: v for k, v in build.items() if v is not None},
        )
        res.raise_for_status()
        d = res.json()
        return self.hydrate_list(d["data"], Mod), self.hydrate(
            d["pagination"], Pagination
        )

    async def get_mod(self, modId: int) -> Mod:
        res = await self._api._get(f"/v1/mods/{modId}")
        res.raise_for_status()
        return self.hydrate(res.json()["data"], Mod)

    async def get_mods(self, modIdList: List[int]) -> List[Mod]:
        res = await self._api._post("/v1/mods", params={"modIds": modIdList})
        res.raise_for_status()
        return self.hydrate_list(res.json()["data"], Mod)

    async def get_mod_description(self, modId: int) -> str:
        res = await self._api._get(f"/v1/mods/{modId}/description")
        res.raise_for_status()
        return res.json()["data"]

    async def get_fingerprints(self, fingerprints: List[int]):
        """Only supports addons.
        Minecraft modpacks do not function
        I dont really know a use for this, but I can easily support it."""
        res = await self._api._post(
            "/v1/fingerprints", params={"fingerprints": fingerprints}
        )
        res.raise_for_status()
        return self.hydrate(res.json()["data"], FingerprintsMatchesResult)

    async def get_files(self, fileList: List[int]) -> List[File]:
        res = await self._api._post("/v1/mods/files", params={"fileIds": fileList})
        res.raise_for_status()
        return self.hydrate_list(res.json()["data"], File)

    async def get_mod_files(
        self,
        modId: int,
        gameVersion: Optional[str] = None,
        modLoaderType: Optional[ModLoaderType] = None,
        gameVersionTypeId: Optional[int] = None,
        index: int = 0,
        pageSize: int = 50,
    ) -> Tuple[List[File], Pagination]:
        res = await self._api._get(
            f"/v1/mods/{modId}/files",
            params={
                "gameVersion": gameVersion,
                "modLoaderType": modLoaderType,
                "gameVersionTypeId": gameVersionTypeId,
                "index": index,
                "pageSize": pageSize,
            },
        )
        res.raise_for_status()
        d = res.json()
        return self.hydrate_list(d["data"], File), self.hydrate(
            d["pagination"], Pagination
        )

    async def get_mod_file(self, modId: int, fileId: int) -> File:
        res = await self._api._get(f"/v1/mods/{modId}/files/{fileId}")
        res.raise_for_status()
        return self.hydrate(res.json()["data"], File)

    async def get_mod_file_changelog(self, modId: int, fileId: int) -> str:
        res = await self._api._get(f"/v1/mods/{modId}/files/{fileId}/changelog")
        res.raise_for_status()
        return res.json()["data"]

    async def get_mod_file_download_url(self, modId: int, fileId: int) -> str:
        res = await self._api._get(f"/v1/mods/{modId}/files/{fileId}/download-url")
        res.raise_for_status()
        return res.json()["data"]

    async def close(self):
        return await self._api.close()

    @staticmethod
    def hydrate(data: dict, model: Type[BaseCurseModel]):
        """hydrates a model from a dict"""
        return model.from_dict(data)

    @staticmethod
    def hydrate_list(data: List[dict], model: Type[BaseCurseModel]):
        """hydrates a list of models from a list of dicts"""
        return [model.from_dict(i) for i in data]

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self.close()
