# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='mailscope',
    version="2.0.0",
    packages=find_packages(),
    author="megadose",
    author_email="megadose@protonmail.com",
    install_requires=["termcolor", "bs4", "httpx", "trio", "tqdm", "colorama", "socksio"],
    description="MailScope checks if an email address is associated with accounts across numerous online services with intelligent rate-limit defense and proxy rotation.",
    include_package_data=True,
    url='https://github.com/megadose/holehe',
    entry_points={'console_scripts': [
        'mailscope = mailscope.core:main',
        'holehe = mailscope.core:main',
    ]},
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
