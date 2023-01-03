from curse_api import CurseAPI, APIFactory
import os
import asyncio


class MyFactory(APIFactory):
    # A simple factory that prints the url and http method

    async def _get(self, url, params=None, **kwargs):
        print("GET", url)
        return await super()._get(url, params, **kwargs)

    async def _post(self, url, params=None, **kwargs):
        print("POST", url)
        return await super()._post(url, params, **kwargs)


async def main():
    api = CurseAPI(os.environ["CF_API_KEY"], factory=MyFactory)

    mod = await api.get_mod(3358)
    search = await api.search_mods(slug="jei")

    await api.close() # We close the API gracefully


asyncio.run(main())
