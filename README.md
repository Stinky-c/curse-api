# curse-api

----

## A simple python Curseforge api wrapper using pydantic

Built to serve CF endpoints while providing methods and functions to assist in finding the right mod.

- [Features](#features)
- [Quick Start](#quick-start)
- [Examples](#examples)

----

## Some backstory

A while back when I was starting to learn python further then the basics I created a small tool to download Minecraft mods from a pack manifest.
Soon after I wrote it the new API changes came and broke it. Now once more I want to return to that project idea and expand further. After first rewriting the project using [chili](https://pypi.org/project/chili/) it felt off, so returned to rewrite once more using [pydantic](https://pypi.org/project/pydantic/) for data validation and ease of access

----

## Features

Main Dependencies:

- [Pydantic](https://pypi.org/project/pydantic/)
- [HTTPX](https://pypi.org/project/httpx/)

Currently implemented:

- Important endpoint support
- Full CurseForge model
- Mediocre error handling
- Shortcuts to download mods
- Pluggable API factory
- Serialization and deserialization of models

To Do:

- Fix to be usable with pydantic based ORM's
- Async Rewrite
- Port to python 3.8 and 3.9
- Address all TODO's
- Fully expose needed httpx args
- Write more download handling code
- Test other games too
- Write docs
- Update and fix error handling

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

api = CurseAPI(API_KEY)


"Mods"
a = api.search_mods(searchFilter="JEI", slug="jei")
# applies the search filters to the standard of CF docs

mod = api.get_mod(250398)                   # returns a singular Mod
mod_list = api.get_mods([285109, 238222])   # returns a list of Mods


"files"
"See examples/download.py"
# TODO finish file support
files = api.get_files([3940240])        # returns a list of Files matching their id
mod_files = api.get_mod_files(238222)   # returns all the Files of on a give Mod


"Version details - large data"
"See examples/modloader.py"
mc = api.minecraft_versions()  # returns all of minecraft version data
ml = api.modloader_versions()  # returns **ALL** modloader versions on curseforge

mc_112 = api.get_specific_minecraft_version("1.12.2")           # returns minecraft version related information
forge = api.get_specific_minecraft_modloader("forge-36.2.39")   # returns forge related version information
```

### Downloading to a file

This example opens a properly named file in the current working directory and writes to it.

```python
from curse_api import CurseAPI

api = CurseAPI(API_KEY)

mod_l, page_data = api.search_mods(slug="jei")
latest = mod_l[0].latestFiles[0] # gets the first mod matching the slug "jei" and latest file from the mod

with open(latest.fileName, "wb") as f:
    f.write(latest.download()) # download returns bytes while kwargs is passed to the get method

```

----
Sub project / extension ideas:

- Modloader download and installation
- Minecraft Version type / parser
- MC pack installation
- DB cache extension
