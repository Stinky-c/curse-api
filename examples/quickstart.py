from curse_api import CurseAPI
import os

api = CurseAPI(os.environ["CF_API_KEY"])


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