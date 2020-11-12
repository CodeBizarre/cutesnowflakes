import os
import pytest

from PIL.PngImagePlugin import PngImageFile

from cutesnowflakes.cutesnowflakes import CuteSnowflakes

uid = "674438327927308358"

def test_decode():
    csf = CuteSnowflakes()

    with PngImageFile(f"src/tests/{uid}.PNG") as fp:
        result = csf.decode(fp)

    assert result == uid

def test_encode():
    csf = CuteSnowflakes()
    result, meta = csf.encode(uid)

    assert result.size == (3, 3)

    result.save("test.png", pnginfo=meta)

    with PngImageFile("test.png") as fp:
        assert csf.decode(fp) == uid

    if os.path.exists("test.png"): os.remove("test.png")

def test_set_mode():
    colors = [ "grey", "red", "green", "blue", "purple", "magenta", "yellow", "orange"]
    csf = CuteSnowflakes()

    for color in colors:
        csf.set_mode(color)

        result, meta = csf.encode(uid)
        result.save("test.png", pnginfo=meta)

        with PngImageFile("test.png") as fp:
            assert csf.decode(fp) == uid

        if os.path.exists("test.png"): os.remove("test.png")

    with pytest.raises(ValueError):
        csf.set_mode("incorrect color")
