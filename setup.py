# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='holehe',
    version="1.58.8.2",
    packages=find_packages(),
    author="megadose",
    author_email="megadose@protonmail.com",
    install_requires=["termcolor","bs4","httpx","trio","argparse"],
    description="holehe allows you to check if the mail is used on different sites like twitter, instagram , snapchat and will retrieve information on sites with the forgotten password function.",
    include_package_data=True,
    url='http://github.com/megadose/holehe',
    entry_points = {'console_scripts': ['holehe = holehe.core:main']},
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
