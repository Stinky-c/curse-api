from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Generic, List, Optional, TypeVar
from typing_extensions import Self
import chili  # type: ignore
import httpx  # type: ignore

from .enums import (
    CoreApiStatus,
    CoreStatus,
    FileRelationType,
    FileReleaseType,
    FileStatus,
    GameVersionStatus,
    GameVersionTypeStatus,
    HashAlgo,
    ModLoaderInstallMethod,
    ModLoaderType,
    ModStatus,
)

"""
schemas can be found at https://docs.curseforge.com/#schemas
If exceptions to the format or naming conventions there will be a comment detailing the change
"""
T = TypeVar("T")
# TODO: rewrite download handling code
# File
# Modloader
# minecraft Game Version
class APIBanned(Exception):
    """In case a mod is banned from interacting with the API"""


class BaseCurseModel:
    """The base for curseforge data"""

    def to_dict(self) -> dict[str, Any]:
        d = chili.asdict(self)
        d["cls"] = type(self)
        return d

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return chili.init_dataclass(data, data["cls"])


class BaseRequest(BaseCurseModel):
    def _download(self, url, **kwargs) -> bytes:
        """Kwargs is passed to httpx.get"""
        if url is None:
            raise APIBanned("Mod is unavailable")
        res = httpx.get(
            url, follow_redirects=True, **kwargs, timeout=httpx.Timeout(5, read=15)
        )
        res.raise_for_status()
        return res.content


# misc
@dataclass(slots=True)
class SortableGameVersion(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_SortableGameVersion"""

    gameVersionName: str
    gameVersionPadded: str
    gameVersion: str
    gameVersionReleaseDate: datetime
    gameVersionTypeId: Optional[int]


@dataclass(slots=True)
class Category(BaseCurseModel):
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

    def download_jar(self, **kwargs) -> bytes:
        return self._download(self.jarDownloadUrl, **kwargs)

    def download_json(self, **kwargs) -> bytes:
        return self._download(self.jsonDownloadUrl, **kwargs)


@dataclass(slots=True)
class MinecraftModLoaderIndex(BaseCurseModel):
    "https://docs.curseforge.com/#tocS_MinecraftModLoaderIndex"
    name: str
    gameVersion: str
    latest: bool
    recommended: bool
    dateModified: datetime
    type: ModLoaderType

    def get(self, headers: dict, url: str = "https://api.curseforge.com"):
        raise NotImplementedError  # TODO
        res = httpx.get(url + f"/v1/minecraft/modloader/{self.name}")
        res.raise_for_status()
        return res


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
        res = httpx.get(self.downloadUrl, **kwargs)
        res.raise_for_status()
        return res.content

    def install(self, path: Path) -> Path:  # TODO download to path
        raise NotImplementedError


# file
@dataclass(slots=True)
class FileDependency(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FileDependency"""

    modId: int
    relationType: FileRelationType


@dataclass(slots=True)
class FileHash(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FileHash"""

    value: str
    algo: HashAlgo


@dataclass(slots=True)
class FileIndex(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FileIndex"""

    gameVersion: str
    fileId: int
    filename: str
    releaseType: FileReleaseType
    gameVersionTypeId: Optional[int]
    modLoader: Optional[ModLoaderType]


@dataclass(slots=True)
class FileModule(BaseCurseModel):
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
    downloadUrl: str | None
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
        return self._download(self.downloadUrl, **kwargs)


@dataclass(slots=True)
class FingerprintFuzzyMatch(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FingerprintFuzzyMatch"""

    id: int
    file: File
    latestFiles: List[File]
    fingerprints: List[int]


@dataclass(slots=True)
class FingerprintMatch(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FingerprintMatch"""

    id: int
    file: File
    latestFiles: List[File]


@dataclass(slots=True)
class FingerprintsMatchesResult(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FingerprintsMatchesResult"""

    isCacheBuilt: bool
    exactMatches: List[FingerprintMatch]
    exactFingerprints: List[int]
    partialMatches: List[FingerprintMatch]
    partialMatchFingerprints: Any
    installedFingerprints: List[int]
    unmatchedFingerprints: Optional[List[int]]


@dataclass(slots=True)
class FolderFingerprint(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FolderFingerprint"""

    foldername: str
    fingerprints: List[int]


# game
@dataclass(slots=True)
class GameAssets(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_GameAssets"""

    iconUrl: str
    tileUrl: str
    coverUrl: str


@dataclass(slots=True)
class Game(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_Game"""

    id: int
    name: str
    slug: str
    dateModified: datetime
    assets: GameAssets
    status: CoreStatus
    apiStatus: CoreApiStatus


@dataclass(slots=True)
class GameVersionType(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_GameVersionsByType"""

    id: int
    gameId: int
    name: str
    slug: str


# mod
@dataclass(slots=True)
class ModAsset(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_ModAsset"""

    id: int
    modId: int
    title: str
    description: str
    thumbnailUrl: str
    url: str


@dataclass(slots=True)
class ModAuthor(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_ModAuthor"""

    id: int
    name: str
    url: str


@dataclass(slots=True)
class ModLinks(BaseCurseModel):
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
    allowModDistribution: bool | None  # API status
    gamePopularityRank: int
    isAvailable: bool  # search status
    thumbsUpCount: int

    def download_latest(self, **kwargs) -> bytes:
        if len(self.latestFiles) == 0:
            raise Exception("")
        return self._download(self.latestFiles[0].downloadUrl, **kwargs)


# misc
@dataclass(slots=True)
class FeaturedModsResponse(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FeaturedModsResponse"""

    featured: List[Mod]
    popular: List[Mod]
    recentlyUpdated: List[Mod]


@dataclass(slots=True)
class Pagination(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_Pagination"""

    index: int
    pageSize: int
    resultCount: int
    totalCount: int


class FilterableVersionList(list, Generic[T]):
    """a custom list for accessibility"""

    # TODO
    def filter(self, gvs: Optional[str] = None, ml: Optional[ModLoaderType] = None):
        """Sorts the list and returns a new list matching a string filter"""
        if len(self) <= 0:
            raise Exception("Not long enough to filter")
        temp = self
        if gvs and isinstance(self[0], MinecraftModLoaderIndex):
            temp = [t for t in temp if t.gameVersion == gvs]
        if ml and isinstance(self[0], MinecraftModLoaderIndex):
            temp = [t for t in temp if t.type == ml]
        return temp

    def latest(self, gvs: Optional[str] = None, ml: Optional[ModLoaderType] = None):
        """returns the latest for a given versions"""
        self = self.filter(gvs=gvs, ml=ml)
        return [i for i in self if i.latest == True][0]

    def recommended(
        self, gvs: Optional[str] = None, ml: Optional[ModLoaderType] = None
    ):
        """returns the recommended for a given version"""
        self = self.filter(gvs=gvs, ml=ml)
        return [i for i in self if i.recommended == True]
