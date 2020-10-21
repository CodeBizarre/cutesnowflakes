![Tests](https://github.com/CodeBizarre/cutesnowflakes/workflows/Tests/badge.svg?branch=master)

(Note) Currently MacOS tests are failing under Python 3.9
# Cute Snowflakes

Have you ever wanted cute 3x3 images from snowflake IDs? Great, because here they are!

## Installation
Requires Python 3.6+

`pip install cutesnowflakes`

## Usage:
As a command line application:

`cutesnowflakes.py --encode 118999881999119725 red`

`cutesnowflakes.py --decode folder/my_file.png`

As a library:
```py
## CREATING A SNOWFLAKE
from cutesnowflakes import CuteSnowflakes

flake, meta = CuteSnowflakes()

# Create the snowflake
image = flake.encode("118999881999119725")
# Open it in the system photo viewer
image.show()
# Save the image with its metadata
image.save("my_image.png", pnginfo=meta)

## LOADING A SNOWFLAKE
from PIL.PngImagePlugin import PngImageFile

with PngImageFile("my_image.png") as fp:
    print(flake.decode(fp))
```
