import os
from curse_api.api import APIFactory, CurseAPI


class NewFactory(APIFactory):
    # A simple overide that prints the url and http method

    def _get(self, url, params=None, **kwargs):
        print("GET", url)
        return super()._get(url, params, **kwargs)

    def _post(self, url, params=None, **kwargs):
        print("POST", url)
        return super()._post(url, params, **kwargs)


api = CurseAPI(os.environ["CF_API_KEY"], factory=NewFactory)

api.get_mod(3358)
api.search_mods(slug="jei")
