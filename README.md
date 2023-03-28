# curse-api

----

## A simple async python Curseforge api wrapper using pydantic

Built to serve CF endpoints while providing methods and functions to assist in finding the right mod.

- Quick Install: `pip install curse-api[quick]`
- [Features](#features)
- [Quick Start](#quick-start)
- [Examples](#examples)

----

## Some backstory

A while back when I was starting to learn python further then the basics I created a small tool to download Minecraft mods from a pack manifest.
Soon after I wrote it the new API changes came and broke it. Now once more I want to return to that project idea and expand further. After first rewriting the project using [chili](https://pypi.org/project/chili/) it felt off, so returned to rewrite once more using [pydantic](https://pypi.org/project/pydantic/) for data validation and ease of access. This is mostly a pet project to learn further python.

----

## Features

Main Dependency:

- [Pydantic](https://pypi.org/project/pydantic/)

Native async library support:

- [Aiohttp](https://pypi.org/project/aiohttp/) - `pip install curse-api[aiohttp]`
- [Httpx](https://pypi.org/project/httpx/) - `pip install curse-api[httpx]`

Currently implemented:

- Important endpoint support
- Full CurseForge model
- Mediocre error handling
- Pluggable API factories
- Serialization and deserialization of models
- Python 3.7, 3.8 & 3.9 support
- Async

To Do:

- Fix to be usable with pydantic based ORM's
- Address all TODO's
- Test other games too
- Add more
- Write docs
- Update and fix error handling
- Shortcuts to import clients

CI/CD:

- Type checking
- Version testing
- Tests

----

## Examples

### Quick start

Requires an api from CF to use the API. You can get one [here](https://docs.curseforge.com/#authentication).
This example runs through most of the basics

```python
from curse_api import CurseAPI
from curse_api.clients.httpx import HttpxFactory
import os
import asyncio


async def main():
    async with CurseAPI(os.environ["CF_API_KEY"], factory=HttpxFactory) as api:

        "Mods"
        a = await api.search_mods(searchFilter="JEI", slug="jei")
        # applies the search filters to the standard of CF docs

        mod = await api.get_mod(250398)  # returns a singular Mod
        mod_list = await api.get_mods([285109, 238222])  # returns a list of Mods

        "files"
        "See examples/download.py"
        # TODO finish file support
        files = await api.get_files([3940240])  # returns a list of Files matching their id
        mod_files = await api.get_mod_files(238222)  # returns all the Files of on a give Mod

        "Version details - large data"
        "See examples/modloader.py"
        mc = await api.minecraft_versions()  # returns all of minecraft version data
        ml = await api.modloader_versions()  # returns **ALL** modloader versions on curseforge

        mc_112 = await api.get_specific_minecraft_version("1.12.2")  # returns minecraft version related information
        forge = await api.get_specific_minecraft_modloader("forge-36.2.39")  # returns forge related version information


if __name__ == "__main__":
    asyncio.run(main())
```

### Downloading to a file

This example opens a properly named file in the current working directory and writes to it.

```python
from curse_api import CurseAPI
from curse_api.clients.httpx import HttpxFactory
import os
import asyncio


async def main():
    async with CurseAPI(os.environ["CF_API_KEY"], factory=HttpxFactory) as api:

        # fetch the latest file from project with slug 'jei'
        mod_l, page_data = await api.search_mods(slug="jei")
        latest = mod_l[0].latestFiles[0]

        with open(latest.fileName, "wb") as f:
            down = await api.download(latest.downloadUrl)  # type: ignore
            async for b in down:
                f.write(b)


if __name__ == "__main__":
    asyncio.run(main())

```

----

### Sub project / extension ideas

- Modloader download and installation
- Minecraft Version type / parser
- MC pack installation
- DB cache extension
- Manifest parsing
