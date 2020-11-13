import sys

import numpy

from typing import Generator, Tuple, Union

from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo

def clamp_rgb(values: Union[Tuple[int, ...], Generator]) -> Tuple[int, ...]:
    return tuple(min(156, i) for i in values)

class CuteSnowflakes:
    def __init__(self, mode: str = "red", fmt: Tuple[int, ...] = (100, 0, 0)) -> None:
        self.mode = mode.lower()

        # Ensure that no value in `fmt` exceeds 156 to prevent integer overflow
        fmt = clamp_rgb(fmt)

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
            raise ValueError(f"Error setting format to mode: {mode}, custom: {fmt}")

    def set_mode(self, mode: str) -> None:
        if mode not in self.__switch:
            raise ValueError(
                f"Invalid mode passed. Valid modes are: {list(self.__switch.keys())}"
            )

        self.mode = mode
        self.format = self.__switch.get(self.mode)

    def set_custom(self, fmt: Tuple[int, ...]) -> None:
        if len(fmt) != 3:
            raise ValueError("Tuple fmt must be of length 3.")

        self.__switch["custom"] = clamp_rgb(fmt)

    def encode(self, snowflake: str) -> Tuple[Image.Image, PngInfo]:
        """Takes a snowflake in string form and returns a Pillow image."""
        length = len(snowflake)

        if length < 18 or length > 20:
            raise ValueError("Must provide a valid snowflake.")

        numbers = [
            int(
                snowflake[i:i + 2]
            ) for i in range(0, len(snowflake), 2)
        ]

        data = numpy.zeros([3, 3, 4], dtype=numpy.uint8)

        for i, v in enumerate(numpy.ndindex(data.shape[:2])):
            data[v] = (
                numbers[i] + self.format[0],
                numbers[i] + self.format[1],
                numbers[i] + self.format[2],
                255
            )

        if length > 18:
            data[1][1][3] = 255 - numbers[9:][0]

        meta = PngInfo()
        meta.add_text("format", str(self.format[2]))
        return (Image.fromarray(data), meta)

    def decode(self, image: PngImageFile) -> str:
        """Decodes a snowflake ID from a cutesnowflakes Pillow image."""
        if image.width != 3 and image.height != 3:
            raise ValueError("Image must be 3x3 pixels")

        data = numpy.array(image)

        try:
            meta = image.text["format"]
        except AttributeError:
            print("Warning: Unable to fetch image metadata, using default value (Red).")
            meta = 100
        finally:
            meta = int(meta)

        result = [
            str(data[v][2] - meta).zfill(2) for v in numpy.ndindex(data.shape[:2])
        ]

        final_alpha = data[1][1][3]
        if final_alpha != 255:
            result.append(str(255 - final_alpha))

        return "".join(result)

def print_usage() -> None:
    print(
        f"Usage: {sys.argv[0]} <help | encode | decode\n"
        "encode <snowflake> [color] [r] [g] [b]\n"
        "decode <path/to/file.png>>"
    )

def main() -> None:
    action = sys.argv[1].lower()

    instance = CuteSnowflakes()

    try:
        mode = sys.argv[3].lower()

        if mode == "custom":
            instance.set_custom(
                clamp_rgb(int(rgb) for rgb in sys.argv[4:7])
            )

        instance.set_mode(mode)
    except IndexError:
        instance.set_mode("red")
    except ValueError:
        print("Error: values for r, g, b must be valid integers")
        return

    if action in ("help", "?", "/?", "-h", "--help"):
        print_usage()
    elif action in ("encode", "--encode", "-e"):
        result, meta = instance.encode(sys.argv[2])
        result.show()
        result.save(f"{sys.argv[2]}.PNG", pnginfo=meta)
    elif action in ("decode", "--decode", "-d"):
        with PngImageFile(f"{sys.argv[2]}") as fp:
            print(instance.decode(fp))
    else:
        print_usage()

if __name__ == "__main__":
    main()
