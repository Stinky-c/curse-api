from datetime import datetime
from pydantic import BaseModel
from pathlib import Path
from typing import Any, List, Optional, TypeVar, TextIO
import json
from pydantic.json import pydantic_encoder
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
class APIBanned(Exception):
    """In case a mod is banned from interacting with the API"""


class BaseCurseModel(BaseModel):
    """The base for curseforge data"""

    def to_dict(self):
        """transforms object to a dict"""
        return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        """Given data returns a hydrated object"""
        return cls.parse_obj(data)

    def to_json(self, fp: TextIO):
        """dumps object to TextIO"""
        if not fp.writable():
            raise Exception("Cannot write to buffer")
        json.dump(self, fp, default=pydantic_encoder)

    @classmethod
    def from_json(cls, fp: TextIO):
        """loads json from buffer returns cls"""
        data = json.load(fp)
        return cls.from_dict(data)


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


class SortableGameVersion(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_SortableGameVersion"""

    gameVersionName: str
    gameVersionPadded: str
    gameVersion: str
    gameVersionReleaseDate: datetime
    gameVersionTypeId: Optional[int]


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
    additionalFilesJson: Optional[str]
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


class FileDependency(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FileDependency"""

    modId: int
    relationType: FileRelationType


class FileHash(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FileHash"""

    value: str
    algo: HashAlgo


class FileIndex(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FileIndex"""

    gameVersion: str
    fileId: int
    filename: str
    releaseType: FileReleaseType
    gameVersionTypeId: Optional[int]
    modLoader: Optional[ModLoaderType]


class FileModule(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FileModule"""

    name: str
    fingerprint: int


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


class FingerprintFuzzyMatch(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FingerprintFuzzyMatch"""

    id: int
    file: File
    latestFiles: List[File]
    fingerprints: List[int]


class FingerprintMatch(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FingerprintMatch"""

    id: int
    file: File
    latestFiles: List[File]


class FingerprintsMatchesResult(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FingerprintsMatchesResult"""

    isCacheBuilt: bool
    exactMatches: List[FingerprintMatch]
    exactFingerprints: List[int]
    partialMatches: List[FingerprintMatch]
    partialMatchFingerprints: Any
    installedFingerprints: List[int]
    unmatchedFingerprints: Optional[List[int]]


class FolderFingerprint(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FolderFingerprint"""

    foldername: str
    fingerprints: List[int]


# game


class GameAssets(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_GameAssets"""

    iconUrl: str
    tileUrl: str
    coverUrl: str


class Game(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_Game"""

    id: int
    name: str
    slug: str
    dateModified: datetime
    assets: GameAssets
    status: CoreStatus
    apiStatus: CoreApiStatus


class GameVersionType(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_GameVersionsByType"""

    id: int
    gameId: int
    name: str
    slug: str


# mod


class ModAsset(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_ModAsset"""

    id: int
    modId: int
    title: str
    description: str
    thumbnailUrl: str
    url: str


class ModAuthor(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_ModAuthor"""

    id: int
    name: str
    url: str


class ModLinks(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_ModLinks"""

    websiteUrl: Optional[str]
    wikiUrl: Optional[str]
    issuesUrl: Optional[str]
    sourceUrl: Optional[str]


class Mod(BaseRequest):
    """https://docs.curseforge.com/#tocS_Mod

    allowModDistribution : bool | None : If none the mod download url is not available for download

    isAvailable : bool : True if the mod can be searched for
    """

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
        if len(self.latestFiles) == 0:
            raise Exception("No latest files")
        return self._download(self.latestFiles[0].downloadUrl, **kwargs)


# misc


class FeaturedModsResponse(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_FeaturedModsResponse"""

    featured: List[Mod]
    popular: List[Mod]
    recentlyUpdated: List[Mod]


class Pagination(BaseCurseModel):
    """https://docs.curseforge.com/#tocS_Pagination"""

    index: int
    pageSize: int
    resultCount: int
    totalCount: int
