#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def read_readme(fname):
   try:
      import pypandoc
      return pypandoc.convert('README.md','rst')
   except (IOError, ImportError):
      return ''

setup(
    name = "python-cson",
    version = "1.0.7",
    url = 'https://github.com/lifthrasiir/cson',
    download_url = 'https://github.com/gt3389b/python-cson/',
    license = 'MIT',
    description = "Python library for CSON (schema-compressed JSON)",
    author = 'Russell Leake',
    author_email = 'gt3389b@gmail.com',
    py_modules = ["cson"],
    long_description = read_readme('README.md'),
    include_package_data = True,
    zip_safe = False,
    keywords = 'json cson cursive'
)
