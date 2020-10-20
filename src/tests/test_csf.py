import os

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

    if os.path.exists("test.png"):
        os.remove("test.png")
