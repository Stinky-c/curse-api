from curse_api import CurseAPI, File, Mod


def test_dict_conversion(api: CurseAPI):  # notice the s!

    # cast to dict and parse using pydantic
    file = api.get_mod_file(247217, 2868969)
    data = file.to_dict()
    file2 = File.parse_obj(data)
    assert file2 == file, "Pydantic conversion failed"


def test_conversion(api: CurseAPI):
    # cast to dict and parse using class method
    model1 = api.get_mod(250398)
    data = model1.to_dict()

    model2 = api.hydrate(data, Mod)
    assert model1 == model2, "hydration method failed"
