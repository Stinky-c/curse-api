from curse_api import CurseAPI
from curse_api.clients.httpx import HttpxFactory
import os
import asyncio


async def main():
    async with CurseAPI(os.environ["CF_API_KEY"], factory=HttpxFactory) as api:

        file = await api.get_mod_file(247217, 2868969)

        # cast to dict
        # TODO update me
        file_dict = file.to_dict()


if __name__ == "__main__":
    asyncio.run(main())
