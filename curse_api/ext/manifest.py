from __future__ import annotations
from typing import Dict, Any, TYPE_CHECKING, List
from ..models import File, ManifestMetadata

if TYPE_CHECKING:
    from ..api import CurseAPI

AnyDict = Dict[Any, Any]

# TODO: custom manifest creator
class ManifestParser:
    def __init__(self, api: "CurseAPI") -> None:
        self.api = api

    async def load_files(self, data: AnyDict) -> List[File]:
        files = data.get("files", None)
        if not isinstance(files, list):
            raise TypeError("Files is not list")

        fids = [i["fileID"] for i in files]
        return await self.api.get_files(fids)

    async def load_modloader(self, data: AnyDict):  # TODO: type better
        minecraft = data.get("minecraft")
        if not isinstance(minecraft, dict):
            raise TypeError("Manifest is invalid")
        modls: List[Dict] = minecraft.get("modLoaders")  # type: ignore

        modls = [i["id"] for i in modls if i["primary"]]
        if len(modls) != 1:
            raise Exception("Modloaders primary not found")

        return await self.api.get_specific_minecraft_modloader(modls[0])  # type: ignore

    async def load_meatdata(self, data: AnyDict):
        return ManifestMetadata.from_dict(data)
