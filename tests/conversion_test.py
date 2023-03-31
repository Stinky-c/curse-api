from curse_api import SimpleCurseAPI, File, Mod
import pytest

@pytest.mark.asyncio
async def test_dict_conversion(api: SimpleCurseAPI):  # notice the s!

    # cast to dict and parse using pydantic
    file = await api.get_mod_file(247217, 2868969)
    data = file.to_dict()
    file2 = File.parse_obj(data)
    assert file2 == file, "Pydantic conversion failed"

@pytest.mark.asyncio
async def test_conversion(api: SimpleCurseAPI):
    # cast to dict and parse using class method
    model1 = await api.get_mod(250398)
    data = model1.to_dict()

    model2 = api.hydrate(data, Mod)
    assert model1 == model2, "hydration method failed"
