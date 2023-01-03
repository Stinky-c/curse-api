from curse_api import CurseAPI
import os
import asyncio


async def main():
    async with CurseAPI(os.environ["CF_API_KEY"]) as api:

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
