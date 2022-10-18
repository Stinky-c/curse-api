import os
from curse_api import CurseAPI

api = CurseAPI(os.environ["CF_API_KEY"])

# setting httpx client timeout to 30 seconds
print(api.api._sess.timeout)
api.api.set_client_timeout(default=30)
print(api.api._sess.timeout)

# setting response and request hooks
def log(obj):
    print(obj, type(obj))


api.api.set_request_hook(log)
api.api.set_response_hook(log)

api.get_mod(285109)

# print the current hooks
print("request hooks", api.api.request_hooks)
print("request hooks", api.api.response_hooks)

# remove all request and response hooks
# returns the functions
api.api.pop_request_hooks()
api.api.pop_response_hooks()
