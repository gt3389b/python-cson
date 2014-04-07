#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "python-cson",
    version = "1.0.1",
    url = 'https://github.com/lifthrasiir/cson',
    download_url = 'https://github.com/gt3389b/python-cson/',
    license = 'MIT',
    description = "Python library for CSON (schema-compressed JSON)",
    author = 'Russell Leake',
    author_email = 'gt3389b@gmail.com',
    py_modules = ["cson"],
    include_package_data = True,
    zip_safe = False,
)
