from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional
import requests as req

from .enums import *
from .exceptions import *

"""
schemas can be found at https://docs.curseforge.com/#schemas
If exceptions to the format or naming conventions there will be a comment detailing the change
"""


class BaseRequest:
    @staticmethod
    def _raise(status_code: int):
        match status_code:
            case 200:
                return True
            case 400:
                raise BadRequest(
                    "The server cannot or will not process the request due to something that is perceived to be a client error."
                )
            case 403:
                raise Forbidden("The client does not have access rights to the content")
            case 404:
                raise NotFound("The server can not find the requested resource.")
            case 500:
                raise InternalServerError(
                    "The server has encountered a situation it does not know how to handle."
                )
            case 418:
                raise ImATeapot(
                    "The server refuses to brew coffee because it is, permanently, a teapot."
                )
            case _:
                raise Exception(f"I don't know what went wrong")


# misc
@dataclass(slots=True)
class SortableGameVersion:
    """https://docs.curseforge.com/#tocS_SortableGameVersion"""

    gameVersionName: str
    gameVersionPadded: str
    gameVersion: str
    gameVersionReleaseDate: datetime
    gameVersionTypeId: Optional[int]


@dataclass(slots=True)
class Category:
    """https://docs.curseforge.com/#tocS_Category"""

    id: int
    gameId: int
    name: str
    slug: str
    url: str
    iconUrl: str
    dateModified: datetime
    isClass: bool
    classId: int
    parentCategoryId: int


# game version
@dataclass(slots=True)
class MinecraftGameVersion(BaseRequest):
    """https://docs.curseforge.com/#tocS_MinecraftGameVersion"""

    id: int
    gameVersionId: int
    versionString: str
    jarDownloadUrl: str
    jsonDownloadUrl: str
    approved: bool
    dateModified: datetime
    gameVersionTypeId: int
    gameVersionStatus: GameVersionStatus
    gameVersionTypeStatus: GameVersionTypeStatus

    def _download(self, url, **kwargs):
        res = req.get(url, **kwargs)
        if self._raise(res.status_code):
            return res.content

    def download_jar(self, **kwargs) -> bytes:
        self._download(self.jarDownloadUrl, **kwargs)

    def download_json(self, **kwargs) -> bytes:
        self._download(self.jsonDownloadUrl, **kwargs)


@dataclass(slots=True)
class MinecraftModLoaderIndex:
    "https://docs.curseforge.com/#tocS_MinecraftModLoaderIndex"
    name: str
    gameVersion: str
    latest: bool
    recommended: bool
    dateModified: datetime
    type: Optional[ModLoaderType]

    def get(self, headers: dict, url: str = "https://api.curseforge.com"):
        res = req.get(url + f"/v1/minecraft/modloader/{self.name}")


@dataclass(slots=True)
class MinecraftModLoaderVersion(BaseRequest):
    "https://docs.curseforge.com/#tocS_MinecraftModLoaderVersion"
    id: int
    gameVersionId: int
    minecraftGameVersionId: int
    forgeVersion: str
    name: str
    type: ModLoaderType
    downloadUrl: str
    filename: str
    installMethod: ModLoaderInstallMethod
    latest: bool
    recommended: bool
    approved: bool
    dateModified: datetime
    mavenVersionString: str
    versionJson: str
    librariesInstallLocation: str
    minecraftVersion: str
    additionalFilesJson: str
    modLoaderGameVersionId: int
    modLoaderGameVersionTypeId: int
    modLoaderGameVersionStatus: GameVersionStatus
    modLoaderGameVersionTypeStatus: GameVersionTypeStatus
    mcGameVersionId: int
    mcGameVersionTypeId: int
    mcGameVersionStatus: GameVersionStatus
    mcGameVersionTypeStatus: GameVersionTypeStatus
    installProfileJson: str

    def download(self, **kwargs) -> bytes:  # download
        res = req.get(self.downloadUrl, **kwargs)
        if self._raise(res.status_code):
            return res.content

    def install(self, path: Path) -> Path:  # TODO download to path
        return
        install_loc = self.librariesInstallLocation
        self.download()
        pass


# file
@dataclass(slots=True)
class FileDependency:
    """https://docs.curseforge.com/#tocS_FileDependency"""

    modId: int
    relationType: FileRelationType


@dataclass(slots=True)
class FileHash:
    """https://docs.curseforge.com/#tocS_FileHash"""

    value: str
    algo: HashAlgo


@dataclass(slots=True)
class FileIndex:
    """https://docs.curseforge.com/#tocS_FileIndex"""

    gameVersion: str
    fileId: int
    filename: str
    releaseType: FileReleaseType
    gameVersionTypeId: Optional[int]
    modLoader: Optional[ModLoaderType]


@dataclass(slots=True)
class FileModule:
    """https://docs.curseforge.com/#tocS_FileModule"""

    name: str
    fingerprint: int


@dataclass(slots=True)
class File(BaseRequest):
    """https://docs.curseforge.com/#tocS_File"""

    id: int
    gameId: int
    modId: int
    isAvailable: bool
    displayName: str
    fileName: str
    releaseType: FileReleaseType
    fileStatus: FileStatus
    hashes: List[FileHash]
    fileDate: datetime
    fileLength: int
    downloadCount: int
    downloadUrl: str
    gameVersions: List[str]
    sortableGameVersions: List[SortableGameVersion]
    dependencies: List[FileDependency]
    exposeAsAlternative: Optional[bool]
    parentProjectFileId: Optional[int]
    alternateFileId: int
    isServerPack: bool
    serverPackFileId: Optional[int]
    fileFingerprint: int
    modules: List[FileModule]

    def download(self, **kwargs) -> bytes:
        """Kwargs is passed to requests.get"""
        res = req.get(self.downloadUrl, **kwargs)
        if self._raise(res.status_code):
            return res.content


@dataclass(slots=True)
class FingerprintFuzzyMatch:
    """https://docs.curseforge.com/#tocS_FingerprintFuzzyMatch"""

    id: int
    file: File
    latestFiles: List[File]
    fingerprints: List[int]


# @dataclass(slots=True)
# class FingerprintFuzzyMatchResult:
#     """https://docs.curseforge.com/#tocS_FingerprintFuzzyMatchResult"""
#     fuzzyMatches: List[FingerprintFuzzyMatch]


@dataclass(slots=True)
class FingerprintMatch:
    """https://docs.curseforge.com/#tocS_FingerprintMatch"""

    id: int
    file: File
    latestFiles: List[File]


@dataclass(slots=True)
class FingerprintsMatchesResult:
    """https://docs.curseforge.com/#tocS_FingerprintsMatchesResult"""

    isCacheBuilt: bool
    exactMatches: List[FingerprintMatch]
    exactFingerprints: List[int]
    partialMatches: List[FingerprintMatch]
    partialMatchFingerprints: Any
    installedFingerprints: List[int]
    unmatchedFingerprints: Optional[List[int]]


@dataclass(slots=True)
class FolderFingerprint:
    """https://docs.curseforge.com/#tocS_FolderFingerprint"""

    foldername: str
    fingerprints: List[int]


# game
@dataclass(slots=True)
class GameAssets:
    """https://docs.curseforge.com/#tocS_GameAssets"""

    iconUrl: str
    tileUrl: str
    coverUrl: str


@dataclass(slots=True)
class Game:
    """https://docs.curseforge.com/#tocS_Game"""

    id: int
    name: str
    slug: str
    dateModified: datetime
    assets: GameAssets
    status: CoreStatus
    apiStatus: CoreApiStatus


# @dataclass(slots=True)
# class GameVersionsByType:
#     """https://docs.curseforge.com/#tocS_GameVersionsByType"""
#     type: int
#     versions: List[str]


@dataclass(slots=True)
class GameVersionType:
    """https://docs.curseforge.com/#tocS_GameVersionsByType"""

    id: int
    gameId: int
    name: str
    slug: str


# mod
@dataclass(slots=True)
class ModAsset:
    """https://docs.curseforge.com/#tocS_ModAsset"""

    id: int
    modId: int
    title: str
    description: str
    thumbnailUrl: str
    url: str


@dataclass(slots=True)
class ModAuthor:
    """https://docs.curseforge.com/#tocS_ModAuthor"""

    id: int
    name: str
    url: str


@dataclass(slots=True)
class ModLinks:
    """https://docs.curseforge.com/#tocS_ModLinks"""

    websiteUrl: Optional[str]
    wikiUrl: Optional[str]
    issuesUrl: Optional[str]
    sourceUrl: Optional[str]


@dataclass(slots=True)
class Mod(BaseRequest):
    """https://docs.curseforge.com/#tocS_Mod"""

    id: int
    gameId: int
    name: str
    slug: str
    links: ModLinks
    summary: str
    status: ModStatus
    downloadCount: int
    isFeatured: bool
    primaryCategoryId: int
    categories: List[Category]
    classId: int
    authors: List[ModAuthor]
    logo: ModAsset
    screenshots: List[ModAsset]
    mainFileId: int
    latestFiles: List[File]
    latestFilesIndexes: List[FileIndex]
    dateCreated: datetime
    dateModified: datetime
    dateReleased: datetime
    allowModDistribution: bool | None
    gamePopularityRank: int
    isAvailable: bool
    thumbsUpCount: int

    def download_latest(self, **kwargs) -> bytes:
        res = req.get(self.latestFiles[0].downloadUrl, **kwargs)
        if self._raise(res.status_code):
            return res.content


# misc
@dataclass(slots=True)
class FeaturedModsResponse:
    """https://docs.curseforge.com/#tocS_FeaturedModsResponse"""

    featured: List[Mod]
    popular: List[Mod]
    recentlyUpdated: List[Mod]


@dataclass(slots=True)
class Pagination:
    """https://docs.curseforge.com/#tocS_Pagination"""

    index: int
    pageSize: int
    resultCount: int
    totalCount: int
