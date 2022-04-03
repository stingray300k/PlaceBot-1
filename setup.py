# coding: utf-8
from setuptools import setup

setup(
    name="PlaceBot-vim",
    version="0.3.0",
    packages=["place_vim"],
    entry_points={
        'console_scripts': [
            'place-vim=place_vim:main',
        ]
    },
    install_requires=[
        "requests",
        "PlaceBot @ git+https://github.com/goatgoose/PlaceBot@c4f87b5"
    ],
)
