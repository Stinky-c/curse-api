import json
from curse_api import CurseAPI
import os
import pickle

API_KEY = "$2a$10$bL4bIL5pUWqfcO7KQtnMReakwtfHbNKh6v1uTpKlzhwoueEJQnPnm"
api = CurseAPI(os.environ["CF_API_KEY"], timeout=8)

file = api.get_mod_file(247217, 2868969)

# cast to dict and back
file_dict = file.to_dict()
file2 = file_dict["cls"].from_dict(file_dict)

# cast to pickle and back
file_pickle = pickle.dumps(file)
file4 = pickle.loads(file_pickle)
pass
