from curse_api import CurseAPI, ModLoaderType
import os
import json

api = CurseAPI(os.environ["CF_API_KEY"])

# gets modloader verion from curseforge
versions = api.modloader_versions()


# filtering using list comprehension
v1_16_4 = [i for i in versions if i.gameVersion == "1.16.5"]        # finds all 1.16.5 versions
forge = [i for i in versions if i.type == ModLoaderType.Forge]      # finds all forge loaders

# building on previous lists
v_1_12_2_forge = [i for i in forge if i.gameVersion == "1.12.2"]    # finds all 1.12.2 forge versions
v_1_12_2_forge_latest = [i for i in v_1_12_2_forge if i.latest]     # finds recommened 1.12.2 forge version

# alternative method
v_1_19_3_fabric_recommended = [
    i
    for i in versions
    if i.type == ModLoaderType.Fabric and i.gameVersion == "1.19.3" and i.recommended
][0]

# NOTE the modloader version list is large and not cached
# dump to disk if you wish to save network resources
with open("versions.json", "w") as f:
    from pydantic.json import pydantic_encoder
    # we have a list of pydantic objects
    # `json.dump` cannot normally dump datetime objects

    json.dump(versions, f, default=pydantic_encoder)

# works the same for minecraft version
mc_versions = api.minecraft_versions()
for i in (i for i in mc_versions if i.versionString == "1.7.2"):    # creates generator
    print(i.approved)
