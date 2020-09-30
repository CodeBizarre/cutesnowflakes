from PIL import Image

from cutesnowflakes import encode, decode

uid = "674438327927308358"

def test_decode():
    with Image.open(f"..\\tests\\{uid}.PNG") as fp:
        result = decode(fp)

    assert result == uid

def test_encode():
    image = encode(uid)

    assert (image.width, image.height) == (3, 3)
    assert decode(image) == uid
