import sys
import os
import pytest

from PIL.PngImagePlugin import PngImageFile

from cutesnowflakes.cutesnowflakes import CuteSnowflakes, print_usage

uid_17 = "00000000000010001"
uid_18 = "674438327927308358"
uid_19 = "1315158838627233792"
uid_20 = "01189998819991197253"
uid_21 = "123123123123123123123"

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

def test_usage(capsys):
    print_usage()

    assert capsys.readouterr().out == \
        f"Usage: {sys.argv[0]} <help | encode | decode>\n" \
        "encode <snowflake> [color] [r] [g] [b]\n" \
        "decode <path/to/file.png>>\n"

def test_decode():
    csf = CuteSnowflakes()

    with PngImageFile(f"src/tests/{uid_18}.png") as fp:
        result = csf.decode(fp)

    assert result == uid_18

def test_too_large():
    csf = CuteSnowflakes()

    with pytest.raises(ValueError):
        with PngImageFile("src/tests/enlarged.png") as fp:
            csf.decode(fp)

def test_no_metadata(capsys):
    csf = CuteSnowflakes()

    with PngImageFile("src/tests/no_meta.png") as fp:
        csf.decode(fp)

        assert capsys.readouterr().out == \
            "Warning: Unable to fetch image metadata, using default value (Red).\n"

@pytest.mark.parametrize(
    "uid,expected", [(uid_18, uid_18), (uid_19, uid_19), (uid_20, uid_20)]
)
def test_encode_good(encode, uid, expected):
    result, uid_result = encode(uid)

    assert result.size == (3, 3)
    assert uid_result == expected

@pytest.mark.parametrize("uid", [uid_17, uid_21])
def test_encode_bad(encode, uid):
    with pytest.raises(ValueError):
        result, uid_result = encode(uid)

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

    with pytest.raises(ValueError):
        csf.set_custom((100, 150))

    if os.path.exists("test.png"): os.remove("test.png")

def test_set_mode_error():
    csf = CuteSnowflakes()

    with pytest.raises(ValueError):
        csf.set_mode("incorrect color")

def test_init_error():
    with pytest.raises(ValueError):
        CuteSnowflakes(mode="blurple")
