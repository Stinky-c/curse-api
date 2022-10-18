import os
from curse_api import CurseAPI

api = CurseAPI(os.environ["CF_API_KEY"])

versions = api.modloader_versions()

v1_12_2 = versions.filter(gvs="1.12.2")
v1_16_5 = versions.filter(gvs="1.16.5")
# TODO: add mod loader type filter
pass