#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages
setup(
    name = "dtcli",
    version = "0.0.1",
    keywords = ("pip", "dependencytrack", "cli"),
    description = "Dependency Track cli tool",
    long_description = "Dependency Track cli tool. ",
    license = "MIT Licence",
    url = "https://github.com/wolf-li/dtcli.git",
    author = "wolf-li",
    author_email = "hermannli2019@163.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "Linux",
    install_requires = ["requests"],
    scripts = [],
    entry_points = {
        'console_scripts': [
            'dtcli = dtcli.dtcli:main'
        ]
    }
)
