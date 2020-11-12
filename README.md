![Tests](https://github.com/CodeBizarre/cutesnowflakes/workflows/Tests/badge.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/cutesnowflakes.svg)](https://badge.fury.io/py/cutesnowflakess)

(Note) Currently MacOS tests are failing under Python 3.9
# Cute Snowflakes

Have you ever wanted cute 3x3 images from snowflake IDs? Great, because here they are!

Examples:

![](https://i.imgur.com/fa4rkle.png)
![](https://i.imgur.com/GYQWhtN.png)
![](https://i.imgur.com/ddrpniN.png)
![](https://i.imgur.com/Pi3iPHE.png)

## Installation
Requires Python 3.6+

`pip install cutesnowflakes`

## Usage:
As a command line application:

`cutesnowflakes.py --encode 118999881999119725 red`

`cutesnowflakes.py --decode folder/my_file.png`

Available colors for encoding are:
```
grey
red
green
blue
purple
magenta
yellow
orange
```

As a library:
```py
## CREATING A SNOWFLAKE
from cutesnowflakes import CuteSnowflakes

flake = CuteSnowflakes()

# Create the snowflake
image, meta = flake.encode("118999881999119725")
# Open it in the system photo viewer
image.show()
# Save the image with its metadata
image.save("my_image.png", pnginfo=meta)

## LOADING A SNOWFLAKE
from PIL.PngImagePlugin import PngImageFile

with PngImageFile("my_image.png") as fp:
    print(flake.decode(fp))

## CHANGING SNOWFLAKE COLOR
flake.set_mode("magenta")
```
