from curse_api import CurseAPI
import os

api = CurseAPI(os.environ["CF_API_KEY"], timeout=8)

file = api.get_mod_file(247217, 2868969)

# cast to dict
# TODO update me
file_dict = file.to_dict()
