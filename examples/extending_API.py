from curse_api import SimpleCurseAPI, CurseAPI
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
    api = SimpleCurseAPI(os.environ["CF_API_KEY"], factory=MyFactory)
    # alteritve factoires exist at 'curse_api.clients'

    mod = await api.get_mod(3358)
    search = await api.search_mods(slug="jei")

    await api.close()  # We close the API gracefully


async def build_factory():
    return MyFactory(os.environ["CF_API_KEY"])


async def main2():
    # CurseAPI replaced the old version taking instances of session instead the factory itself
    # They are functionally the same CurseAPI allows precreated session of your http client to be used
    # See 'complex_API.py'
    api = CurseAPI(await build_factory())

    mod = await api.get_mod(3358)
    search = await api.search_mods(slug="jei")

    await api.close()


if __name__ == "__main__":
    asyncio.run(main())
