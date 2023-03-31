from curse_api import SimpleCurseAPI
import pytest


@pytest.mark.asyncio
async def test_get_mod_file(api: SimpleCurseAPI):
    pid = 60089
    fid = 3871353
    res = await api.get_mod_file(pid, fid)
    assert res.id == fid, "Wrong File"
    assert res.modId == pid, "Wrong Mod"
