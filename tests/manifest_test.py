from curse_api.ext import ManifestParser
import pytest
from typing import Dict, Any


MANIFEST: Dict[Any, Any] = {
    "minecraft": {
        "version": "1.16.5",
        "modLoaders": [{"id": "forge-36.1.31", "primary": True}],
    },
    "manifestType": "minecraftModpack",
    "overrides": "overrides",
    "manifestVersion": 1,
    "version": "v3.4",
    "author": "Buckybubba",
    "name": "NYNSP",
    "files": [{"projectID": 238222, "fileID": 3312207, "required": True}],
}


@pytest.mark.asyncio
async def test_metadata(manifest_parser: ManifestParser):
    metadata = await manifest_parser.load_meatdata(MANIFEST)
    assert metadata.name == MANIFEST["name"], "Manifest data is incorrect"


@pytest.mark.asyncio
async def test_files(manifest_parser: ManifestParser):
    files = await manifest_parser.load_files(MANIFEST)
    expected = MANIFEST["files"][0]
    assert files[0].id == expected["fileID"], " got unexpected file id"
    assert files[0].modId == expected["projectID"], " got unexpected project id"


@pytest.mark.asyncio
async def test_mods(manifest_parser: ManifestParser):
    mods = await manifest_parser.load_mods(MANIFEST)
    expected = MANIFEST["files"][0]
    assert mods[0].id == expected["projectID"], "Got wrong project"


@pytest.mark.asyncio
async def test_modloader(manifest_parser: ManifestParser):
    modloader = await manifest_parser.load_modloader(MANIFEST)
    excepted = MANIFEST["minecraft"]
    assert (
        modloader.minecraftVersion == excepted["version"]  # type:ignore
    ), "Incorrect modloader"
    assert (
        modloader.name == excepted["modLoaders"][0]["id"]  # type:ignore
    ), "invalid modloader name & version"
