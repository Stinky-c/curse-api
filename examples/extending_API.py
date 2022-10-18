import os
from curse_api import CurseAPI, APIFactory


class MyFactory(APIFactory):
    # A simple factory that prints the url and http method

    def _get(self, url, params=None, **kwargs):
        print("GET", url)
        return super()._get(url, params, **kwargs)

    def _post(self, url, params=None, **kwargs):
        print("POST", url)
        return super()._post(url, params, **kwargs)


api = CurseAPI(os.environ["CF_API_KEY"], factory=MyFactory)

api.get_mod(3358)
api.search_mods(slug="jei")
