from curse_api import CurseAPI, ModLoaderType
from curse_api.clients.httpx import HttpxFactory
import os
import asyncio
import json

"""
This example is thoroughly powered using list comprehension. Some tutorials are provided

https://realpython.com/list-comprehension-python/
https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
https://gist.github.com/bkbncn/85b845b955cc6b4eb1d12442fb56df25

"""


async def main():
    async with CurseAPI(os.environ["CF_API_KEY"], factory=HttpxFactory) as api:

        # gets modloader verion from curseforge
        versions = await api.modloader_versions()

        # filtering using list comprehension
        v1_16_4 = [
            i for i in versions if i.gameVersion == "1.16.5"
        ]  # finds all 1.16.5 versions
        forge = [
            i for i in versions if i.type == ModLoaderType.Forge
        ]  # finds all forge loaders

        # building on previous lists
        v_1_12_2_forge = [
            i for i in forge if i.gameVersion == "1.12.2"
        ]  # finds all 1.12.2 forge versions
        v_1_12_2_forge_latest = [
            i for i in v_1_12_2_forge if i.latest
        ]  # finds recommened 1.12.2 forge version

        # alternative method
        v_1_19_3_fabric_recommended = [
            i
            for i in versions
            if i.type == ModLoaderType.Fabric
            and i.gameVersion == "1.19.3"
            and i.recommended
        ][0]

        # NOTE the modloader version list is large and not cached
        # dump to disk or otherways if you wish to save network resources
        with open("versions.json", "w") as f:
            from pydantic.json import pydantic_encoder

            # we have a list of pydantic objects
            # `json.dump` cannot normally dump datetime objects

            json.dump(versions, f, default=pydantic_encoder)

        # works the same for minecraft version
        mc_versions = await api.minecraft_versions()
        for i in (i for i in mc_versions if i.versionString == "1.7.2"):
            print(i.approved)


if __name__ == "__main__":
    asyncio.run(main())
