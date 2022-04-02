# coding: utf-8
from setuptools import setup

setup(
    name="PlaceBot-vim",
    version="0.1.2",
    packages=["place_bot_vim"],
    scripts=["scripts/place-vim"],
    install_requires=[
        "requests",
        "websocket-client",
        "beautifulsoup4",
        "numpy",
        "Pillow",
    ],
)
