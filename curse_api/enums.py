from enum import Enum, IntEnum


class ModsSearchSortField(Enum):
    Featured = "Featured"
    Popularity = "Popularity"
    LastUpdated = "LastUpdated"
    Name = "Name"
    Author = "Author"
    TotalDownloads = "TotalDownloads"
    Category = "Category"
    GameVersion = "GameVersion"


class SortOrder(Enum):
    Ascending = "asc"
    Descending = "desc"


class Games(IntEnum):
    # Auto Generated Enum
    demeo = 78135
    wildstar = 454
    chronicles_of_arcadia = 70667
    final_fantasy_iii = 5026
    rom = 335
    civ6 = 727
    final_fantasy_v = 5021
    final_fantasy_i = 5230
    teso = 455
    sims4 = 78062
    tsw = 64
    among_us = 69761
    minecraft = 432
    final_fantasy_vi = 4773
    swlegends = 4455
    worldoftanks = 423
    terraria = 431
    darkestdungeon = 608
    kerbal = 4401
    stardewvalley = 669
    final_fantasy_iv = 4741
    wow = 1
    minecraft_dungeons = 69271
    sc2 = 65
    surviving_mars = 61489
    final_fantasy_ii = 5001
    rift = 424


class CoreApiStatus(IntEnum):
    Private = 1
    Public = 2


class CoreStatus(IntEnum):
    Draft = 1
    Test = 2
    PendingReview = 3
    Rejected = 4
    Approved = 5
    Live = 6


class GameVersionStatus(IntEnum):
    Approved = 1
    Deleted = 2
    New = 3


class GameVersionTypeStatus(IntEnum):
    Normal = 1
    Deleted = 2


class FileRelationType(IntEnum):
    EmbeddedLibrary = 1
    OptionalDependency = 2
    RequiredDependency = 3
    Tool = 4
    Incompatible = 5
    _Include = 6


class FileReleaseType(IntEnum):
    Release = 1
    Beta = 2
    Alpha = 3


class FileStatus(IntEnum):
    Processing = 1
    ChangesRequired = 2
    UnderReview = 3
    Approved = 4
    Rejected = 5
    MalwareDetected = 6
    Deleted = 7
    Archived = 8
    Testing = 9
    Released = 10
    ReadyForReview = 11
    Deprecated = 12
    Baking = 13
    AwaitingPublishing = 14
    FailedPublishing = 15


class HashAlgo(IntEnum):
    Sha1 = 1
    Md5 = 2


class ModStatus(IntEnum):
    New = 1
    ChangesRequired = 2
    UnderSoftReview = 3
    Approved = 4
    Rejected = 5
    ChangesMade = 6
    Inactive = 7
    Abandoned = 8
    Deleted = 9
    UnderReview = 10


class ModLoaderInstallMethod(IntEnum):
    ForgeInstaller = 1
    ForgeJarInstall = 2
    ForgeInstaller_v2 = 3


class ModLoaderType(IntEnum):
    Any = 0
    Forge = 1
    Cauldron = 2
    LiteLoader = 3
    Fabric = 4
    Quilt = 5
