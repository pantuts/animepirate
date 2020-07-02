#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="animepirate-pantuts",
    version="0.1.1",
    author="Nick Bien",
    author_email="pantuts@gmail.com",
    description="Dumb anime videos downloader.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pantuts/animepirate",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'pirateanime = animepirate.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License"
    ],
    python_requires='>=3.6',
)
