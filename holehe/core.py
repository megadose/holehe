import hashlib
import httpx
import importlib
import json
import pkgutil
import os
import random
import re
import string
import sys
import time
import trio

from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
from tqdm import tqdm

try:
    import cookielib
except BaseException:
    import http.cookiejar as cookielib

from holehe.localuseragent import ua
from prints import *


DEBUG = True

__version__ = "1.57"

if not DEBUG:
    checkVersion = httpx.get("https://pypi.org/pypi/holehe/json")
if not DEBUG and checkVersion.json()["info"]["version"] != __version__:
    if os.name != 'nt':
        p = Popen(["pip3",
                   "install",
                   "--upgrade",
                   "git+git://github.com/megadose/holehe@master"],
                  stdout=PIPE,
                  stderr=PIPE)
    else:
        p = Popen(["pip",
                   "install",
                   "--upgrade",
                   "git+git://github.com/megadose/holehe@master"],
                  stdout=PIPE,
                  stderr=PIPE)
    (output, err) = p.communicate()
    p_status = p.wait()
    print("Holehe has just been updated, you can restart it. ")
    exit()


def import_submodules(package, recursive=True):
    """Get all the holehe submodules"""
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def get_functions(modules):
    """Transform the modules objects to functions"""
    websites = []
    for module in modules:
        if len(module.split(".")) > 3:
            modu = modules[module]
            site = module.split(".")[-1]
            websites.append(modu.__dict__[site])
    return websites


def ask_email():
    if len(sys.argv) < 2 or len(sys.argv[1]) < 5:
        exit("[-] Please enter a target email ! \nExample : holehe email@example.com")
    return sys.argv[1]

async def maincore():
    modules = import_submodules("holehe.modules")
    websites = get_functions(modules)

    credits()
    email = ask_email()
    start_time = time.time()
    client = httpx.AsyncClient(timeout=6)
    out = []
    async with trio.open_nursery() as nursery:
        for website in tqdm(websites):
            nursery.start_soon(website, email, client, out)

    out.sort(key=lambda i: i['name'])# We sort by modules names

    await client.aclose()
    shows(email, out, time, len(websites), start_time)

def main():
    trio.run(maincore)

main()
