# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='holehe',
    version="1",
    packages=find_packages(),
    author="megadose",
    install_requires=["requests","fake_useragent","evolut","argparse","termcolor","tqdm"],
    description="holehe allows you to check if the mail is used on different sites like twitter, instagram and will retrieve information on sites with the forgotten password function.",
    include_package_data=True,
    url='http://github.com/megadose/holehe',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
