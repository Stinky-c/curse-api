from curse_api import AsyncCurseAPI
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.asyncio
async def test_get_mod_file(api: AsyncCurseAPI):
    pid = 60089
    fid = 3871353
    res = await api.get_mod_file(pid, fid)
    assert res.id == fid, "Wrong File"
    assert res.modId == pid, "Wrong Mod"


@pytest.mark.asyncio
async def test_get_mod_files(api: AsyncCurseAPI):  # notice the s!
    pid = 60089
    res, page = await api.get_mod_files(pid)
    assert isinstance(res, list)
    assert res[0].modId == pid, "Wrong Mod"
    assert page.resultCount == 50, "Check for default page size"
