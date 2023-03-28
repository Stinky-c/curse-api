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
    Minecraft = 432
    Demeo = 78135
    WildStar = 454
    Chronicles_of_Arcadia = 70667
    Sid_Meiers_Civilization_VI = 727
    The_Secret_World = 64
    The_Elder_Scrolls_Online = 455
    Runes_of_Magic = 335
    Secret_World_Legends = 4455
    Among_Us = 69761
    Darkest_Dungeon = 608
    Kerbal_Space_Program = 4401
    Terraria = 431
    World_of_Tanks = 423
    Minecraft_Dungeons = 69271
    Stardew_Valley = 669
    StarCraft_II = 65
    Surviving_Mars = 61489
    World_of_Warcraft = 1
    Rift = 424


class MinecraftCategories(IntEnum):
    Worlds = 17
    Bukkit_Plugins = 5
    Customization = 4546
    Modpacks = 4471
    Resource_Packs = 12
    Addons = 4559
    Mods = 6


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


class ModLoaderType(Enum):
    Any_ = None
    Any = 0
    Forge = 1
    Cauldron = 2
    LiteLoader = 3
    Fabric = 4
    Quilt = 5
