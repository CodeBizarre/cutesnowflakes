from setuptools import setup

from cutesnowflakes import __version__

with open("../README.md") as fp:
    long_description = fp.read()

setup(
    name="cutesnowflakes",
    version=__version__,
    description="Cute 3x3 images from snowflake IDs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeBizarre/cutesnowflakes",
    author="CodeBizarre",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=["cutesnowflakes"],
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "numpy==1.19.3",
        "pillow==8.0",
        "click>=7.1<7.2",
        "aenum>=2.2<2.3"
    ]
)
