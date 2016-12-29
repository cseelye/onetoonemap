#!/usr/bin/env python2.7

from setuptools import setup
import os

setup(
    name = "twowaymap",
    version = "1.0.0",
    author = "Carl Seelye",
    author_email = "cseelye@gmail.com",
    description = "Two-way mapping collection type",
    license = "MIT",
    keywords = "two-way map dict",
    packages = ["twowaymap"],
    url = "https://github.com/cseelye/twowaymap",
    long_description = open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    install_requires = [
    ]
)

