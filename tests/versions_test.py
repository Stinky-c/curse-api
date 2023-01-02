from curse_api import AsyncCurseAPI
import pytest


@pytest.mark.asyncio
async def test_get_mod_file(api: AsyncCurseAPI):
    pid = 60089
    fid = 3871353
    res = await api.get_mod_file(pid, fid)
    assert res.id == fid, "Wrong File"
    assert res.modId == pid, "Wrong Mod"
