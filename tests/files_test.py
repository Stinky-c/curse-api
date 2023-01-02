from curse_api import CurseAPI
from dotenv import load_dotenv

load_dotenv()


def test_get_mod_file(api: CurseAPI):
    pid = 60089
    fid = 3871353
    res = api.get_mod_file(pid, fid)
    assert res.id == fid, "Wrong File"
    assert res.modId == pid, "Wrong Mod"


def test_get_mod_files(api: CurseAPI):  # notice the s!
    pid = 60089
    res, page = api.get_mod_files(pid)
    assert isinstance(res, list)
    assert res[0].modId == pid, "Wrong Mod"
    assert page.resultCount == 50, "Check for default page size"
