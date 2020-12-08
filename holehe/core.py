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

from localuseragent import ua
from tools.prints import *
from tools.debug import *
from tools.config import *

DEBUG = False

__version__ = "1.57"


async def maincore():
    modules = import_submodules("modules")
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

def main(DEBUG):
    debug(DEBUG)
    trio.run(maincore)

if __name__ == "__main__":
    DEBUG = True
    main(DEBUG)
