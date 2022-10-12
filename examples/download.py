from curse_api import CurseAPI
import os

api = CurseAPI(os.environ["CF_API_KEY"])

mod_l, page_data = api.search_mods(slug="jei")
latest = mod_l[0].latestFiles[0]

with open(latest.fileName, "wb") as f:
    f.write(latest.download())
