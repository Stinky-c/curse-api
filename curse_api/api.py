from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)
from enum import Enum
from .categories import BaseCategory

from .abc import APIFactory
from .enums import (
    Games,
    ModLoaderType,
    ModsSearchSortField,
    SortOrder,
)
from .models import (
    BaseCurseModel,
    File,
    FingerprintsMatchesResult,
    MinecraftGameVersion,
    MinecraftModLoaderIndex,
    MinecraftModLoaderVersion,
    Mod,
    Pagination,
)

"""
TODO: write more doc strings
"""

U = TypeVar("U", bound=BaseCurseModel)


# TODO: fix passing in enums
class CurseAPI:
    """The main class for api requests.
    Cannot handle the download of API banned mods

    """

    def __init__(
        self,
        client: "APIFactory",
    ) -> None:
        """The main factory for handling requests
        accepts additional kwargs passing to the creation of the factory

        Args:
            client: An instance of an client wrapper. Use `SimpleCurseAPI` to skip manual client instantiation.

        """
        if not issubclass(type(client), APIFactory):
            raise TypeError("factory or session must be provided")
        self._api: "APIFactory" = client

    @property
    def api(self):
        return self._api

    async def minecraft_versions(self) -> List[MinecraftGameVersion]:
        """Returns all minecraft version data from curseforge.
        Use `get_specific_minecraft_version` with the game version string to get more detailed data.
        """
        res = await self._api.get("/v1/minecraft/version")
        return self.hydrate_list(res["data"], MinecraftGameVersion)

    async def get_specific_minecraft_version(
        self, gameVersionString: str
    ) -> MinecraftGameVersion:
        res = await self._api.get(f"/v1/minecraft/version/{gameVersionString}")

        return self.hydrate(res["data"], MinecraftGameVersion)

    async def modloader_versions(self) -> List[MinecraftModLoaderIndex]:
        """
        Returns all minecraft modloader data from curseforge.
        Use `get_specific_minecraft_modloader` with the slug to get more detailed data.
        """
        res = await self._api.get(
            "/v1/minecraft/modloader", params={"includeAll": True}
        )

        return self.hydrate_list(res["data"], MinecraftModLoaderIndex)

    async def get_specific_minecraft_modloader(
        self, modLoaderName: str
    ) -> MinecraftModLoaderVersion:
        res = await self._api.get(f"/v1/minecraft/modloader/{modLoaderName}")

        return self.hydrate(res["data"], MinecraftModLoaderVersion)

    async def search_mods(
        self,
        gameId: Games = Games.minecraft,
        classId: Optional[int] = None,
        categoryId: Optional[BaseCategory] = None,
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
            gameId (Games, optional): Filter by game id. Defaults to `Games.minecraft`.
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

        res = await self._api.get(
            "/v1/mods/search",
            params={k: v for k, v in build.items() if v is not None},
        )

        d = res
        return self.hydrate_list(d["data"], Mod), self.hydrate(
            d["pagination"], Pagination
        )

    async def get_mod(self, modId: int) -> Mod:
        res = await self._api.get(f"/v1/mods/{modId}")
        return self.hydrate(res["data"], Mod)

    async def get_mods(self, modIdList: List[int]) -> List[Mod]:
        res = await self._api.post("/v1/mods", params={"modIds": modIdList})
        return self.hydrate_list(res["data"], Mod)

    async def get_mod_description(self, modId: int) -> str:
        res = await self._api.get(f"/v1/mods/{modId}/description")
        return res["data"]

    async def get_fingerprints(self, fingerprints: List[int]):
        """Only supports addons.
        Minecraft modpacks do not function
        I dont really know a use for this, but I can easily support it."""
        res = await self._api.post(
            "/v1/fingerprints", params={"fingerprints": fingerprints}
        )

        return self.hydrate(res["data"], FingerprintsMatchesResult)

    async def get_files(self, fileList: List[int]) -> List[File]:
        res = await self._api.post("/v1/mods/files", params={"fileIds": fileList})
        return self.hydrate_list(res["data"], File)

    async def get_mod_files(
        self,
        modId: int,
        gameVersion: Optional[str] = None,
        modLoaderType: Optional[ModLoaderType] = None,
        gameVersionTypeId: Optional[int] = None,
        index: int = 0,
        pageSize: int = 50,
    ) -> Tuple[List[File], Pagination]:
        build = {
            "gameVersion": gameVersion,
            "modLoaderType": modLoaderType,
            "gameVersionTypeId": gameVersionTypeId,
            "index": index,
            "pageSize": pageSize,
        }
        res = await self._api.get(
            f"/v1/mods/{modId}/files",
            params={k: v for k, v in build.items() if v is not None},
        )

        return self.hydrate_list(res["data"], File), self.hydrate(
            res["pagination"], Pagination
        )

    async def get_mod_file(self, modId: int, fileId: int) -> File:
        res = await self._api.get(f"/v1/mods/{modId}/files/{fileId}")
        return self.hydrate(res["data"], File)

    async def get_mod_file_changelog(self, modId: int, fileId: int) -> str:
        res = await self._api.get(f"/v1/mods/{modId}/files/{fileId}/changelog")
        return res["data"]

    async def get_mod_file_download_url(self, modId: int, fileId: int) -> str:
        res = await self._api.get(f"/v1/mods/{modId}/files/{fileId}/download-url")
        return res["data"]

    async def get_games(self) -> Enum:
        res = await self.api.get("/v1/games")
        return Enum("Games", {i["slug"]: i["id"] for i in res["data"]})

    async def close(self):
        return await self._api.close()

    @staticmethod
    def hydrate(data: Dict[Any, Any], model: Type[U]):
        """hydrates a model from a dict"""
        return model.from_dict(data)

    @staticmethod
    def hydrate_list(data: List[Dict[Any, Any]], model: Type[U]):
        """hydrates a list of models from a list of dicts"""
        return [model.from_dict(i) for i in data]

    async def download(self, url: str, chunk_size: int = 32):
        return await self._api.download(url, chunk_size)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self.close()


class SimpleCurseAPI(CurseAPI):
    def __init__(
        self,
        api_key: str,
        factory: Type["APIFactory"],
        base_url: str = "https://api.curseforge.com",
        user_agent: str = "stinky-c/curse-api",
    ) -> None:
        self._api: "APIFactory" = factory(
            api_key=api_key, base_url=base_url, user_agent=user_agent
        )
        """The main factory for handling requests
        accepts additional kwargs passing to the creation of the factory

        Args:
            api_key (str): Required. get one from here: https://docs.curseforge.com/#accessing-the-service.
            factory (APIFactory): a factory for handling API requests.
            base_url (str, optional): An overide of the url base. Defaults to "https://api.curseforge.com".
            user_agent (str, optional): user_agent used for requests. Defaults to "stinky-c/curse-api".
        """
