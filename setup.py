# coding: utf-8
from setuptools import setup

setup(
    name="PlaceBot-vim",
    version="0.3.0",
    scripts=["scripts/place-vim"],
    install_requires=[
        "requests",
        "PlaceBot @ git+https://github.com/goatgoose/PlaceBot@c4f87b5"
    ],
)
