from setuptools import setup, find_packages

setup(name="cutesnowflakes", packages=find_packages())

from cutesnowflakes.cutesnowflakes import VERSION

setup(
    name="cutesnowflakes",
    version=VERSION,
    description="Cute 3x3 images from snowflake IDs",
    url="https://github.com/CodeBizarre/cutesnowflakes",
    author="CodeBizarre",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=1.19<1.20",
        "pillow==8.0"
    ],
    entry_points={
        "console_scripts": [
            "cutesnowflakes=cutesnowflakes:main"
        ]
    }
)
