from __future__ import annotations

import sys

import numpy

from enum import Enum

from numpy import uint8
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo

def clamp_rgb(values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(min(156, i) for i in values)

# TODO: Custom
class Color(Enum):
    grey    = (100, 100, 100)
    red     = (100, 0, 0)
    green   = (0, 100, 0)
    blue    = (0, 0, 100)
    purple  = (50, 0, 100)
    magenta = (100, 0, 100)
    yellow  = (150, 150, 0)
    orange  = (150, 75, 0)

def encode(snowflake: str, mode: Color = Color.red) -> tuple[Image.Image, PngInfo]:
    """Takes a snowflake in string form and returns a Pillow image."""
    length = len(snowflake)

    if length < 18 or length > 20:
        raise ValueError("Must provide a valid snowflake.")

    numbers = [
        int(
            snowflake[i:i + 2]
        ) for i in range(0, len(snowflake), 2)
    ]

    data = numpy.zeros([3, 3, 4], dtype=uint8)

    for i, v in enumerate(numpy.ndindex(data.shape[:2])):
        data[v] = (
            numbers[i] + mode.value[0],
            numbers[i] + mode.value[1],
            numbers[i] + mode.value[2],
            255
        )

    if length > 18:
        data[1][1][3] = 255 - numbers[9:][0]

    meta = PngInfo()
    meta.add_text("format", str(mode.value[2]))
    return (Image.fromarray(data), meta)

def decode(image: PngImageFile) -> str:
    """Decodes a snowflake ID from a cutesnowflakes Pillow image."""
    if image.width != 3 and image.height != 3:
        raise ValueError("Image must be 3x3 pixels")

    data = numpy.array(image)

    meta = 100

    try:
        meta = int(image.text["format"])
    except (AttributeError, KeyError):
        print("Warning: Unable to fetch image metadata, using default value (Red).")

    result = [
        str(data[v][2] - meta).zfill(2) for v in numpy.ndindex(data.shape[:2])
    ]

    final_alpha = data[1][1][3]
    if final_alpha != 255:
        result.append(str(255 - final_alpha))

    return "".join(result)

def print_usage() -> None:
    print(
        f"Usage: {sys.argv[0]} <help | encode | decode>\n"
        "encode <snowflake> [color]\n"
        "decode <path/to/file.png>>"
    )

def main() -> None:
    action = sys.argv[1].lower()

    try:
        mode = Color[sys.argv[3].lower()]
    except IndexError:
        mode = Color.red
    except ValueError:
        print("Error: values for r, g, b must be valid integers")
        return

    if action in ("help", "?", "/?", "-h", "--help"):
        print_usage()
    elif action in ("encode", "--encode", "-e"):
        result, meta = encode(sys.argv[2], mode)
        result.show()
        result.save(f"{sys.argv[2]}.png", pnginfo=meta)
    elif action in ("decode", "--decode", "-d"):
        with PngImageFile(f"{sys.argv[2]}") as fp:
            print(decode(fp))
    else:
        print_usage()

if __name__ == "__main__":
    main()
