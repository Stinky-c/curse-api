import os
from curse_api import CurseAPI, ModLoaderType

api = CurseAPI(os.environ["CF_API_KEY"])

# modloader verion
# NOTE: currently only supports modloaders
versions = api.modloader_versions()
v1_16_5 = versions.filter(gvs="1.16.5")
v1_18_2 = versions.recommended(gvs="1.18.2", ml=ModLoaderType.Fabric)
v1_12_2 = versions.latest(gvs="1.12.2", ml=ModLoaderType.Forge)
