import os
import pytest

from PIL.PngImagePlugin import PngImageFile

from cutesnowflakes.cutesnowflakes import CuteSnowflakes

uid_18 = "674438327927308358"
uid_19 = "1315158838627233792"
uid_20 = "01189998819991197253"

colors = ["grey", "red", "green", "blue", "purple", "magenta", "yellow", "orange"]

def delete_test_png():
    if os.path.exists("test.png"): os.remove("test.png")

@pytest.fixture
def encode(scope="function"):
    csf = CuteSnowflakes()

    def _action(uid: str):
        result, meta = csf.encode(uid)
        result.save("test.png", pnginfo=meta)

        with PngImageFile("test.png") as fp:
            uid_result = csf.decode(fp)

        return result, uid_result

    yield _action

    delete_test_png()

def test_decode():
    csf = CuteSnowflakes()

    with PngImageFile(f"src/tests/{uid_18}.PNG") as fp:
        result = csf.decode(fp)

    assert result == uid_18

@pytest.mark.parametrize(
    "uid,expected", [(uid_18, uid_18), (uid_19, uid_19), (uid_20, uid_20)]
)
def test_encode(encode, uid, expected):
    result, uid_result = encode(uid)

    assert result.size == (3, 3)
    assert uid_result == expected

@pytest.mark.parametrize("color", colors)
def test_set_mode(color):
    csf = CuteSnowflakes()

    csf.set_mode(color)

    result, meta = csf.encode(uid_18)
    result.save("test.png", pnginfo=meta)

    with PngImageFile("test.png") as fp:
        assert csf.decode(fp) == uid_18

    delete_test_png()

def test_custom_encode():
    csf = CuteSnowflakes()

    csf.set_custom((100, 999, 62))
    csf.set_mode("custom")

    result, meta = csf.encode(uid_18)
    result.save("test.png", pnginfo=meta)

    with PngImageFile("test.png") as fp:
        assert csf.decode(fp) == uid_18

    if os.path.exists("test.png"): os.remove("test.png")

def test_set_mode_error():
    csf = CuteSnowflakes()

    with pytest.raises(ValueError):
        csf.set_mode("incorrect color")
