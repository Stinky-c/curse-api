from curse_api import SimpleCurseAPI
from curse_api.clients.httpx import HttpxFactory
import os
import asyncio


async def main():
    async with SimpleCurseAPI(os.environ["CF_API_KEY"], factory=HttpxFactory) as api:

        # fetch the latest file from project with slug 'jei'
        mod_l, page_data = await api.search_mods(slug="jei")
        latest = mod_l[0].latestFiles[0]

        with open(latest.fileName, "wb") as f:
            down = await api.download(latest.downloadUrl)  # type: ignore
            async for b in down:
                f.write(b)


if __name__ == "__main__":
    asyncio.run(main())
