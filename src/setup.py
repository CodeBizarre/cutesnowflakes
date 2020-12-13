from setuptools import setup

with open("../README.md") as fp:
    long_description = fp.read()

setup(
    name="cutesnowflakes",
    version="0.3.0",
    description="Cute 3x3 images from snowflake IDs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeBizarre/cutesnowflakes",
    author="CodeBizarre",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=["cutesnowflakes"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19<1.20",
        "pillow==8.0"
    ]
)
