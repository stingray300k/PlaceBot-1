# coding: utf-8
from setuptools import setup

setup(
    name="PlaceBot-vim",
    version="0.1.0",
    modules=["place_bot"],
    scripts=["examples/place_vim.py"],
    install_requires=[
        "requests",
        "websocket-client",
        "beautifulsoup4",
        "numpy",
        "Pillow",
    ],
)
