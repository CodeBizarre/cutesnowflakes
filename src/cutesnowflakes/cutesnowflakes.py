from __future__ import annotations

import logging

import click
import numpy

from enum import Enum

from numpy import uint8
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo

logging.basicConfig(level=logging.WARNING, format="%(message)s")

def clamp_rgb(values: tuple[int, ...]) -> tuple[int, ...]:
    """Clamp values in a given tuple to a maximum value of 156.

    Arguments:
        values: A tuple of RGB(A) values to be clamped.

    Returns:
        The clamped result of `values`.
    """
    return tuple(min(156, i) for i in values)

# TODO: Custom
class Color(Enum):
    """name:(R,G,B) values for preset colors"""
    grey    = (100, 100, 100)
    red     = (100, 0, 0)
    green   = (0, 100, 0)
    blue    = (0, 0, 100)
    purple  = (50, 0, 100)
    magenta = (100, 0, 100)
    yellow  = (150, 150, 0)
    orange  = (150, 75, 0)

    def __str__(self) -> str:
        return " ".join(f"{c.name}" for c in Color)

class ColorError(KeyError):
    """Color mismatch, display valid colors."""
    def __init__(self, *args, **kwargs):
        logging.error(
            f"[CuteSnowflakes Error]: Color must be one of {[c.name for c in Color]}"
        )
        super().__init__()

def encode(snowflake: str, color: Color = Color.red) -> tuple[Image.Image, PngInfo]:
    """Takes a snowflake in string form and returns a Pillow image.

    Args:
        snowflake: A snowflake ID between 18-20 digits (inclusive) passed as str.
        color: The Color to create the image in.

    Returns:
        A tuple of (Pillow Image, Pillow PngInfo). The PngInfo is to be used in the
        image.save() function. For example:

        image, meta = encode("01189998819991197253")
        image.save("my_file.png", pnginfo=meta)

    Raises:
        ValueError: Invalid snowflake passed.
    """
    length = len(snowflake)

    if length < 18 or length > 20:
        raise ValueError("Must provide a valid snowflake.")

    # Create a list of 2-digit numbers from the given input string
    numbers = [
        int(
            snowflake[i:i + 2]
        ) for i in range(0, len(snowflake), 2)
    ]

    # Create a 3 wide by 3 tall array of 4 values to represent an RGBA image
    data = numpy.zeros([3, 3, 4], dtype=uint8)

    # Adjust the value of each pixel based on the given snowflake numbers and color choice
    for i, v in enumerate(numpy.ndindex(data.shape[:2])):
        data[v] = (
            numbers[i] + color.value[0],
            numbers[i] + color.value[1],
            numbers[i] + color.value[2],
            255
        )

    # If the snowflake was longer than 18 characters, store the remaining data in the
    # alpha channel of the center pixel
    if length > 18:
        data[1][1][3] = 255 - numbers[9:][0]

    # Store the color's format key in the metadata of the image
    meta = PngInfo()
    meta.add_text("format", str(color.value[2]))

    return (Image.fromarray(data), meta)

def decode(image: PngImageFile, color: Color = None) -> str:
    """Decodes a snowflake ID from a cutesnowflakes Pillow image.

    Args:
        image: A Pillow PngImageFile representation of a Cute Snowflake.
        color: The color to use as fallback if format metadata is not found in the image.

    Returns:
        A string representing the snowflake ID decoded from the image.

    Raises:
        ValueError: An image larger/smaller than 3x3 pixels was passed.
    """
    if image.width != 3 and image.height != 3:
        raise ValueError("Image must be 3x3 pixels")

    data = numpy.array(image)

    meta = 100

    # FIXME: color parameter is not used
    try:
        meta = int(image.text["format"])
    except (AttributeError, KeyError):
        logging.warning(
            "Warning: Unable to fetch image metadata, using default value (Red)."
        )

    # Calculate the number pairs from the converted image
    result = [
        str(data[v][2] - meta).zfill(2) for v in numpy.ndindex(data.shape[:2])
    ]

    # Grab any extra numbers stored in the center pixel's alpha channel
    final_alpha = data[1][1][3]
    if final_alpha != 255:
        result.append(str(255 - final_alpha))

    return "".join(result)

## Command line interface
@click.group()
def cli(): pass

@cli.command(name="encode")
@click.argument("snowflake", required=True, type=str)
@click.option(
    "color", "--color", "-c",
    required=False,
    type=str,
    default="red",
    help=Color.__str__(Color)
)
@click.option(
    "path", "--path", "-p",
    required=False,
    default=".",
    help="Path to the folder to save the file in."
)
@click.option(
    "show", "--show", "-s",
    required=False,
    type=bool,
    help="Open the image in the default image viewer after creation."
)
def cli_encode(snowflake: str, color: str = "red", path: str = ".", show: bool = False):
    """Encode SNOWFLAKE into a Cute Snowflake. Must be an 18-20 digit number."""
    try:
        image, meta = encode(snowflake, Color[color])
    except KeyError:
        raise ColorError

    if show:
        image.show()

    image.save(f"{path}/{snowflake}.png", pnginfo=meta)

@cli.command(name="decode")
@click.argument("path", required=True, type=str)
@click.option(
    "color", "--color", "-c",
    required=False,
    type=str,
    default="red",
    help=Color.__str__(Color)
)
def cli_decode(path: str, color: str = "red"):
    """Decode a snowflake image at the given file PATH"""
    try:
        set_color = Color[color]
    except KeyError:
        raise ColorError

    try:
        with PngImageFile(path) as fp:
            print(decode(fp, set_color))
    except Exception as e:
        logging.error(f"Error: {e}")

def main():
    cli()

if __name__ == "__main__":
    main()
