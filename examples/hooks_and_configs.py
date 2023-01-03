from curse_api import CurseAPI
import os
import asyncio


async def main():
    async with CurseAPI(os.environ["CF_API_KEY"]) as api:

        # setting httpx client timeout to 30 seconds
        api.api.set_client_timeout(default=30)

        # setting response and request hooks
        def log(obj):
            print(obj)
            pass

        api.api.set_request_hook(log)
        api.api.set_response_hook(log)

        await api.get_mod(285109)

        # print the current hooks

        # remove all request and response hooks
        # returns the functions
        api.api.pop_request_hooks()
        api.api.pop_response_hooks()


if __name__ == "__main__":

    asyncio.run(main())
