import sys

import numpy

from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo

VERSION = "0.2.0"

class CuteSnowflakes:
    def __init__(self, mode: str = "red", fmt: tuple = None) -> None:
        self.mode = mode.lower()

        self.__switch = {
            "grey": (100, 100, 100),
            "red": (100, 0, 0),
            "green": (0, 100, 0),
            "blue": (0, 0, 100),
            "purple": (50, 0, 100),
            "magenta": (100, 0, 100),
            "yellow": (150, 150, 0),
            "orange": (150, 75, 0),
            "custom": fmt
        }

        self.format = self.__switch.get(self.mode, None)

        if self.format is None:
            raise ValueError(f"Error setting format: {mode}:{fmt}")

    def set_mode(self, mode: str):
        self.mode = mode
        self.format = self.__switch.get(self.mode)

    def encode(self, snowflake: str) -> tuple[Image, PngInfo]:
        """Takes a snowflake in string form and returns a Pillow image."""
        if len(snowflake) != 18:
            raise ValueError("Must provide a valid snowflake.")

        numbers = [
            int(
                snowflake[i:i + 2]
            ) for i in range(0, len(snowflake), 2)
        ]

        data = numpy.zeros((3, 3, 3), dtype=numpy.uint8)

        for i, v in enumerate(numpy.ndindex(data.shape[:2])):
            data[v] = (
                numbers[i] + self.format[0],
                numbers[i] + self.format[1],
                numbers[i] + self.format[2]
            )

        meta = PngInfo()
        meta.add_text("format", str(self.format[2]))
        return (Image.fromarray(data), meta)

    def decode(_, image: PngImageFile) -> str:
        """Decodes a snowflake ID from a cutesnowflakes Pillow image."""
        if image.width != 3 and image.height != 3:
            raise ValueError("Image must be 3x3 pixels")

        data = numpy.array(image)

        try:
            meta = image.text["format"]
        except Exception:
            print("Warning: Unable to fetch image metadata, using default value.")
            meta = 100
        finally:
            meta = int(meta)

        result = [
            str(int(data[v][2] - meta)).zfill(2)
            for _, v in enumerate(numpy.ndindex(data.shape[:2]))
        ]

        return "".join(result)

def __usage():
    print(
        f"Usage: {sys.argv[0]} <help | encode | decode\n"
        "encode <snowflake> [mode=red]\n"
        "decode <path/to/file.png>>"
    )

if __name__ == "__main__":
    action = sys.argv[1].lower()

    instance = CuteSnowflakes()

    try:
        instance.set_mode(sys.argv[3].lower())
    except IndexError:
        instance.set_mode("red")

    # TODO: Add custom option for the command line
    if action in ("help", "?", "/?", "-h", "--help"):
        __usage()
    elif action in ("encode", "--encode", "-e"):
        result, meta = instance.encode(sys.argv[2])
        result.show()
        result.save(f"{sys.argv[2]}.PNG", pnginfo=meta)
    elif action in ("decode", "--decode", "-d"):
        with PngImageFile(f"{sys.argv[2]}") as fp:
            print(instance.decode(fp))
    else:
        __usage()
