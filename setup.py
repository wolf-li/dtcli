#!/usr/bin/env python
#-*- coding:utf-8 -*-

with open("README.md", "r") as fh:
    long_description = fh.read()

from setuptools import setup, find_packages
setup(
    name = "dptcli",
    version = "0.0.2",
    keywords = ("pip", "dependencytrack", "cli"),
    description = "Dependency Track cli tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = "MIT Licence",
    url = "https://github.com/wolf-li/dtcli",
    author = "wolf-li",
    author_email = "hermannli2019@163.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "Linux",
    install_requires = ["requests"],
    scripts = [],
    entry_points = {
        'console_scripts': [
            'dptcli = dptcli.dptcli:main'
        ]
    }
)
