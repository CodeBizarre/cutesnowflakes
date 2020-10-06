import sys

import numpy

from PIL import Image

VERSION = "0.1.0"

def encode(snowflake: str) -> Image:
    """Takes a discord snowflake in string form and returns a Pillow image."""
    if len(snowflake) != 18:
        raise ValueError("Must provide a valid snowflake.")

    numbers = [
        int(
            snowflake[i:i + 2]
        ) for i in range(0, len(snowflake), 2)
    ]

    data = numpy.zeros((3, 3, 3), dtype=numpy.uint8)

    for i, v in enumerate(numpy.ndindex(data.shape[:2])):
        data[v] = (numbers[i] * 2, numbers[i] / 2, numbers[i] + 25)

    return Image.fromarray(data)

def decode(image: Image) -> str:
    """Decodes a Discord snowflake ID from a cutesnowflakes Pillow image."""
    if image.width != 3 and image.height != 3:
        raise ValueError("Image must be 3x3 pixels")

    data = numpy.array(image)

    result = [
        str(int(data[v][0] / 2)).zfill(2)
        for i, v in enumerate(numpy.ndindex(data.shape[:2]))
    ]

    return "".join(result)

def _usage():
    print(f"Usage: {sys.argv[0]} <help | encode <snowflake> | decode <path.png>>")

def _parse_args(input_: list):
    action = input_[1].lower()

    if action in ["help", "?", "/?", "-h", "--help"]:
        _usage()
    elif action in ["encode", "--encode", "-e"]:
        result = encode(sys.argv[2])
        result.show()
        result.save(f"{sys.argv[2]}.PNG")
    elif action in ["decode", "--decode", "-d"]:
        with Image.open(f"{input_[2]}") as fp:
            print(decode(fp))
    else:
        _usage()

if __name__ == "__main__":
    try:
        _parse_args(sys.argv)
    except Exception:
        _usage()
