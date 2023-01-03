from curse_api import CurseAPI
import os
import asyncio


async def main():
    async with CurseAPI(os.environ["CF_API_KEY"]) as api:

        mod_l, page_data = await api.search_mods(slug="jei")
        latest = mod_l[0].latestFiles[0]

        with open(latest.fileName, "wb") as f:
            f.write(latest.download())


if __name__ == "__main__":
    asyncio.run(main())
