![Tests](https://github.com/CodeBizarre/cutesnowflakes/workflows/Tests/badge.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/cutesnowflakes.svg)](https://badge.fury.io/py/cutesnowflakess)

# Cute Snowflakes

Have you ever wanted cute 3x3 images from snowflake IDs? Great, because here they are!

Examples:

![](https://i.imgur.com/fa4rkle.png)
![](https://i.imgur.com/GYQWhtN.png)
![](https://i.imgur.com/ddrpniN.png)
![](https://i.imgur.com/Pi3iPHE.png)

## Installation
Requires Python 3.7+

`pip install cutesnowflakes`

## Usage:
As a command line application:

`cutesnowflakes.py encode 118999881999119725`

`cutesnowflakes.py decode folder/my_file.png`

for more information and options use:
`cutesnowflakes.py encode --help` or `cutesnowflakes.py decode --help`

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
from cutesnowflakes import encode, decode

# Create the snowflake
image, meta = encode("118999881999119725")
# Open it in the system photo viewer
image.show()
# Save the image with its metadata
image.save("my_image.png", pnginfo=meta)

## LOADING A SNOWFLAKE
from PIL.PngImagePlugin import PngImageFile

with PngImageFile("my_image.png") as fp:
    print(decode(fp))

## USING A DIFFERENT COLOR
from cutesnowflakes import Color

image, meta = encode("118999881999119725", Color.magenta)

# To decode with a specific color:
result = decode(fp, color = Color.magenta)
```

## Changelog:
### Legend:
```diff
+   : Added
-   : Removed
*** : Fixed
\   : Changed
```
### 0.4.0 (In development):
```diff
\\\ Major rewrite
+ __version__ import to __init__.py
+ New improved command line interface with Click
+ New docstrings
+ Logging
- CuteSnowflakes class
- Support for custom formatting (Temporarily)
\ Now requires Python 3.7 or higher
\ Improved old docstrings
```

### 0.3.0 (Current release)
```diff
+ __version__ to __init__.py
+ Error handling for set_mode()
+ Support for 19 and 20 digit snowflakes
+ Support for custom colors through command line --encode argument
\ Various minor code cleanups and improvements
\ Rename __usage() to print_usage()
\ Improved test suite
\ Improved type annotations
*** Possibility for integer overflows
```

### 0.2.1:
```diff
*** \ Various minor documentation and structure changes/fixes
```

### 0.2.0:
```diff
\ Move to a class instead of bare functions
\ Improved command line arguments
\ Moved version to setup.py
+ Multiple colors with set_mode() and format hint PngInfo
```

### 0.1.0:
```diff
+ Initial version
```
