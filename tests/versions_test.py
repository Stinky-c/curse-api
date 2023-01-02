from curse_api import CurseAPI


def test_get_mod_file(api: CurseAPI):
    pid = 60089
    fid = 3871353
    res = api.get_mod_file(pid, fid)
    assert res.id == fid, "Wrong File"
    assert res.modId == pid, "Wrong Mod"
