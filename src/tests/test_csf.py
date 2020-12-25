import os
import logging

import pytest

from PIL.PngImagePlugin import PngImageFile

from cutesnowflakes.cutesnowflakes import Color, ColorError, encode, decode

LOGGER = logging.getLogger(__name__)

uid_17 = "00000000000010001"
uid_18 = "674438327927308358"
uid_19 = "1315158838627233792"
uid_20 = "01189998819991197253"
uid_21 = "123123123123123123123"

colors = [c.name for c in Color]
custom_colors = [
    (0, 0, 0),
    (100, 100, 0),
    (156, 0, 156),
    (100, 156, 7),
    (-100, 20000, 400),
    (15, 72, 90)
]

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

def test_no_metadata(caplog):
    caplog.set_level(logging.WARNING)

    with PngImageFile("src/tests/no_meta.png") as fp:
        decode(fp)

        assert "Warning: Unable to fetch image metadata, using default value (Red).\n" \
            in caplog.text

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

@pytest.mark.parametrize("colors", custom_colors)
def test_custom_encode(colors):
    result, meta = encode(uid_18, "custom", colors[0], colors[1], colors[2])
    result.save("test.png", pnginfo=meta)

    with PngImageFile("test.png") as fp:
        assert decode(fp) == uid_18

    delete_test_png()

def test_color_error():
    with pytest.raises(ColorError):
        encode(uid_18, "ref")
