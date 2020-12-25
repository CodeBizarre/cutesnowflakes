import sys
import os
import pytest

from PIL.PngImagePlugin import PngImageFile

from cutesnowflakes.cutesnowflakes import Color, encode, decode

uid_17 = "00000000000010001"
uid_18 = "674438327927308358"
uid_19 = "1315158838627233792"
uid_20 = "01189998819991197253"
uid_21 = "123123123123123123123"

colors = ["grey", "red", "green", "blue", "purple", "magenta", "yellow", "orange"]

def delete_test_png():
    if os.path.exists("test.png"): os.remove("test.png")

@pytest.fixture
def fixture_encode(scope="function"):
    def _action(uid: str, color: Color = Color.red):
        result, meta = encode(uid)
        result.save("test.png", pnginfo=meta)

        with PngImageFile("test.png") as fp:
            uid_result = decode(fp)

        return result, uid_result

    yield _action

    delete_test_png()

def test_decode():
    with PngImageFile(f"src/tests/{uid_18}.png") as fp:
        result = decode(fp)

    assert result == uid_18

def test_too_large():
    with pytest.raises(ValueError):
        with PngImageFile("src/tests/enlarged.png") as fp:
            decode(fp)

def test_no_metadata(capsys):
    with PngImageFile("src/tests/no_meta.png") as fp:
        decode(fp)

        assert capsys.readouterr().out == \
            "Warning: Unable to fetch image metadata, using default value (Red).\n"

@pytest.mark.parametrize(
    "uid,expected", [(uid_18, uid_18), (uid_19, uid_19), (uid_20, uid_20)]
)
def test_encode_good(fixture_encode, uid, expected):
    result, uid_result = fixture_encode(uid)

    assert result.size == (3, 3)
    assert uid_result == expected

@pytest.mark.parametrize("uid", [uid_17, uid_21])
def test_encode_bad(fixture_encode, uid):
    with pytest.raises(ValueError):
        result, uid_result = encode(uid)

@pytest.mark.parametrize("color", colors)
def test_encode_colors(fixture_encode, color):
    result, uid_result = fixture_encode(uid_18, Color[color])

    assert uid_result == uid_18

# def test_custom_encode():
#     csf.set_custom((100, 999, 62))
#     csf.set_mode("custom")

#     result, meta = csf.encode(uid_18)
#     result.save("test.png", pnginfo=meta)

#     with PngImageFile("test.png") as fp:
#         assert csf.decode(fp) == uid_18

#     with pytest.raises(ValueError):
#         csf.set_custom((100, 150))

#     if os.path.exists("test.png"): os.remove("test.png")
