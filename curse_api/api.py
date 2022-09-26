from functools import cache
from typing import Any, Callable, List

import httpx
from chili import init_dataclass

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
)

"""
TODO
    make important methods private
"""


class APIFactory:
    def __init__(self, API_KEY: str, base_url: str) -> None:
        _headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        self._sess = httpx.Client(base_url=base_url, headers=_headers)

    def _get(self, url: str, params: dict = None, **kwargs) -> httpx.Response:
        """internal get method

        Args:
            url (str): the url to get
            params (dict): a dict of parameters
            kwargs (any): unpacked into requests get method
        """
        res = self._sess.get(url, params=params, **kwargs)
        return res

    def _post(self, url: str, params=None, **kwargs) -> httpx.Response:
        """internal post method

        Args:
            url (str): the url to get
            params (dict): the json data to send
            kwargs (any): unpacked into requests get method
        """
        res = self._sess.post(url, json=params, **kwargs)
        return res

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


class CurseAPI(APIFactory):
    """The main class for api requests
    Cannot handle the download of API banned mods

    """

    def __init__(
        self,
        API_KEY: str,
        API_BASE: str = "https://api.curseforge.com",
        extra_data: Any = None,
    ) -> None:
        super().__init__(API_KEY, API_BASE)
        """The main factory for handling requests

        Args:
            API_KEY (str): Required. get one from here: https://docs.curseforge.com/#accessing-the-service.
            API_BASE (str, optional): An overide of the url base. Defaults to "https://api.curseforge.com".
            headers_overide (dict, optional): headers to overide the default. Defaults to None.
            extra_data (any, optional): any extra data
        """

        self.extra_data = extra_data

    # def _get(self, *args, **kwargs):
    #     return self._api._get(*args, **kwargs)

    # def _post(self, *args, **kwargs):
    #     return self._api._post(*args, **kwargs)

    def health_check(self) -> httpx.Response:
        res = self._get("/")
        return res

    @cache
    def minecraft_versions(self) -> list[MinecraftGameVersion]:
        res = self._get("/v1/minecraft/version")
        res.raise_for_status()
        return [init_dataclass(x, MinecraftGameVersion) for x in res.json()["data"]]

    def get_specific_minecraft_version(
        self, gameVersionString: str
    ) -> MinecraftGameVersion:
        res = self._get(f"/v1/minecraft/version/{gameVersionString}")
        res.raise_for_status()
        return init_dataclass(res.json()["data"], MinecraftGameVersion)

    @cache
    def modloader_versions(self) -> list[MinecraftModLoaderIndex]:
        # very big data
        res = self._get("/v1/minecraft/modloader")
        res.raise_for_status()
        return [init_dataclass(x, MinecraftModLoaderIndex) for x in res.json()["data"]]

    def get_specific_minecraft_modloader(
        self, modLoaderName: str
    ) -> MinecraftModLoaderVersion:
        res = self._get(f"/v1/minecraft/modloader/{modLoaderName}")
        res.raise_for_status()
        return init_dataclass(res.json()["data"], MinecraftModLoaderVersion)

    def search_mods(
        self,
        gameId: Games = Games.Minecraft,
        classId: int = None,
        categoryId: MinecraftCategories = None,
        gameVersion: str = None,
        searchFilter: str = None,
        sortField: ModsSearchSortField = None,
        sortOrder: SortOrder = None,
        modLoaderType: ModLoaderType = None,
        gameVersionTypeId: int = None,
        slug: str = None,
        index: int = 0,
        pageSize: int = 50,
    ) -> tuple[List[Mod], Pagination]:
        """https://docs.curseforge.com/#search-mods


        Args:
            gameId (Games, optional): Filter by game id.. Defaults to Games.Minecraft.
            classId (int, optional): Filter by section id (discoverable via Categories). Defaults to None.
            categoryId (MinecraftCategories, optional): Filter by category id. Defaults to None.
            gameVersion (str, optional): Filter by game version string. Defaults to None.
            searchFilter (str, optional): Filter by free text search in the mod name and author. Defaults to None.
            sortField (ModsSearchSortField, optional): Filter by ModsSearchSortField enumeration. Defaults to None.
            sortOrder (SortOrder, optional): Filter by SortOrder enumeration. Defaults to None.
            modLoaderType (ModLoaderType, optional): Filter only mods associated to a given modloader. Must be coupled with gameVersion.. Defaults to None.
            gameVersionTypeId (int, optional): Filter only mods that contain files tagged with versions of the given gameVersionTypeId. Defaults to None.
            slug (str, optional): Filter by slug (coupled with classId will result in a unique result). Defaults to None.
            index (int, optional): A zero based index of the first item to include in the response. Defaults to 0.
            pageSize (int, optional): The number of items to include in the response. Defaults to 50.

        Returns:
            tuple[List[Mod], Pagination]: A list of mods and pagination data
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

        res = self._get(
            "/v1/mods/search",
            params={k: v for k, v in build.items() if v is not None},
        )
        res.raise_for_status()
        d = res.json()
        return [init_dataclass(x, Mod) for x in d["data"]], init_dataclass(
            d["pagination"], Pagination
        )

    def get_mod(self, modId: int) -> Mod:
        res = self._get(f"/v1/mods/{modId}")
        res.raise_for_status()
        return init_dataclass(res.json()["data"], Mod)

    def get_mods(self, modIdList: list[int]) -> list[Mod]:
        res = self._post("/v1/mods", params={"modIds": modIdList})
        res.raise_for_status()
        return [init_dataclass(x, Mod) for x in res.json()["data"]]

    def get_mod_description(self, modId: int) -> str:
        res = self._get(f"/v1/mods/{modId}/description")
        res.raise_for_status()
        return res.json()["data"]

    def get_fingerprints(self, fingerprints: list[int]):
        """Only supports addons.
        Minecraft modpacks do not function
        I dont really know a use for this, but I can easily support it."""
        res = self._post("/v1/fingerprints", params={"fingerprints": fingerprints})
        res.raise_for_status()
        return init_dataclass(res.json()["data"], FingerprintsMatchesResult)

    def get_files(self, fileList: list[int]) -> list[File]:
        res = self._post("/v1/mods/files", params={"fileIds": fileList})
        res.raise_for_status()
        return [init_dataclass(x, File) for x in res.json()["data"]]

    def get_mod_files(
        self,
        modId: int,
        gameVersion: str = None,
        modLoaderType: ModLoaderType = None,
        gameVersionTypeId: int = None,
        index: int = 0,
        pageSize: int = 50,
    ) -> list[File]:
        res = self._get(
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
        return [init_dataclass(x, File) for x in res.json()["data"]]

    def get_mod_file(self, modId: int, fileId: int) -> File:
        res = self._get(f"/v1/mods/{modId}/files/{fileId}")
        res.raise_for_status()
        return init_dataclass(res.json()["data"], File)

    def get_mod_file_changelog(self, modId: int, fileId: int) -> str:
        res = self._get(f"/v1/mods/{modId}/files/{fileId}/changelog")
        res.raise_for_status()
        return res.json()["data"]

    def get_mod_file_download_url(self, modId: int, fileId: int) -> str:
        res = self._get(f"/v1/mods/{modId}/files/{fileId}/download-url")
        res.raise_for_status()
        return res.json()["data"]
