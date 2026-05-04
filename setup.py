# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='holehe',
    version="1.61",
    packages=find_packages(),
    author="megadose",
    author_email="hello@domain.local",
    install_requires=["requests", "termcolor","bs4","httpx==0.24.1","trio","tqdm","colorama"],
    description="holehe allows you to check if the mail is used on different sites like twitter, instagram , snapchat and will retrieve information on sites with the forgotten password function.",
    include_package_data=True,
    url='http://github.com/i-vt/holehe',
    entry_points = {'console_scripts': ['holehe = holehe.core:main']},
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
