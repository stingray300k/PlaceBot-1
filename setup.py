# coding: utf-8
from setuptools import setup

setup(
    name="PlaceBot-vim",
    version="0.3.2",
    packages=["place_vim"],
    entry_points={
        'console_scripts': [
            'place-vim=place_vim:main',
        ]
    },
    install_requires=[
        "requests",
        "PlaceBot @ git+https://github.com/goatgoose/PlaceBot@e62c6e1"
    ],
)
