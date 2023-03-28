from curse_api import CurseAPI
from curse_api.clients.httpx import HttpxFactory
import os
import asyncio


class MyFactory(HttpxFactory):
    # A simple subclass of the httpx wrapper that prints the url and http method

    async def get(self, url, params=None, **kwargs):
        print("GET", url)
        return await super().get(url, params, **kwargs)

    async def post(self, url, params=None, **kwargs):
        print("POST", url)
        return await super().post(url, params, **kwargs)


async def main():
    api = CurseAPI(os.environ["CF_API_KEY"], factory=MyFactory)
    # alteritve factoires exsit at 'curse_api.clients'

    mod = await api.get_mod(3358)
    search = await api.search_mods(slug="jei")

    await api.close()  # We close the API gracefully


if __name__ == "__main__":
    asyncio.run(main())
