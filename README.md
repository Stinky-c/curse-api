# curse-api

----

## A simple python Curseforge api wrapper with built in dataclasses

Built to serve CF endpoints while providing methods and functions to assist in finding the right mod.

- [Features](#features)
- [Quick Start](#quickstart)
- [Examples](#examples)

----

## Some backstory

A while back when I was starting to learn python further then the basics I created a small tool to download Minecraft mods from a pack manifest.
Soon after I wrote it the new API changes came and broke it. Now once more I want to return to that project idea and expand further. Thus chance to rewrite an old api wrapper of mine with a new library [Chili](https://pypi.org/project/chili/), a dataclass support library also providing data hydration. I have learned a lot since I first wrote that tool. I hope to learn more to build a better revision of it.
I decided that this simple-ish api wrapper would be the first step to a Modpack manager.

----

## Features

Main Dependencies:

- [Chili](https://pypi.org/project/chili/)
- [Requests](https://pypi.org/project/requests/)

Currently implemented:

- most important end point support
- full if not most dataclass support
- mediocre error handling
- shortcuts to download mods

TODO:

- fully expose needed httpx args
- write more dataclass download handling code
- switch to a custom API factory
- write tests

Missing:

- multi-game support - mostly only works for Minecraft
- no downloading of api banned mods
- lack of docs

----

## Examples

### Quickstart

Requires an api from CF to use the API. You can get one [here](https://docs.curseforge.com/#authentication).
This example runs through most of the basics

```python
from curse_api import CurseAPI

api = CurseAPI(API_KEY)

"Mods"
a = api.search_mods(searchFilter="JEI", slug="jei")
# applies the search filters to the standard of CF docs

mod = api.get_mod(3358) # returns a singular Mod
mod_list = api.get_mods([285109, 238222]) # returns a list of Mods


"files"  # TODO finish file support
files = api.get_files([3940240]) # returns a list of Files matching their id
mod_files = api.get_mod_files(238222) # returns all the Files of on a give Mod


"Version details - large data"
# uses functools and caches the return values to conserve API calls
mc = api.minecraft_versions() # returns all of minecraft version data
ml = api.modloader_versions() # returns **ALL** modloader versions on curseforge

# does not use functools
mc_112 = api.get_specific_minecraft_version("1.12.2") # returns minecraft version related information
forge = api.get_specific_minecraft_modloader("forge-36.2.39") # returns forge related version information

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

### Custom hooks and http client settings

Here we configure some settings on our http client and setup some event hooks.

Method calls that result in an api call will always raise for status

```python
from curse_api import CurseAPI

api = CurseAPI(API_KEY)

# setting httpx client timeout to 30 seconds
api._sess.timeout = 30
print(api._sess.timeout)

# setting response and request hooks
def log(obj):
    print(obj, type(obj))


api.set_request_hook(log)
api.set_response_hook(log)

api.get_mod(285109)

# remove all request and response hooks
# returns the functions
api.pop_request_hooks()
api.pop_response_hooks()

```

----
sub project ideas:

- write modloader downloading everything
- enum for mc versions?
- download from manifest
- download pack and unzip
- DB cache of mods and files
