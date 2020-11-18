import time
import argparse
import queue
import requests

import importlib
import pkgutil

from tqdm import tqdm
from termcolor import colored
from threading import Thread
from mechanize import Browser

try:
    import cookielib
except BaseException:
    import http.cookiejar as cookielib

from holehe.localuseragent import *


def import_submodules(package, recursive=True):
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results

modules = import_submodules("modules")

websites = list()

for module in modules:
    if len(module.split(".")) > 2:
        modu = modules[module]
        site = module.split(".")[-1]
        websites.append(modu.__dict__[site])

def main():
    print('Github : https://github.com/megadose/holehe')
    start_time = time.time()
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    parser.add_argument(
        "-e",
        "--email",
        help="Email of the target",
        required=True)
    args = parser.parse_args()

    def websiteName(WebsiteFunction, Websitename, email):
        return({Websitename: WebsiteFunction(email)})

    que = queue.Queue()
    infos = {}
    threads_list = []

    for website in websites:
        t = Thread(
            target=lambda q, arg1: q.put(
                websiteName(
                    website, website.__name__, args.email)), args=(
                que, website))
        t.start()
        threads_list.append(t)

    for t in tqdm(threads_list):
        t.join()

    while not que.empty():
        result = que.get()
        key, value = next(iter(result.items()))
        infos[key] = value

    description = colored("Email used",
                          "green") + "," + colored(" Email not used",
                                                   "magenta") + "," + colored(" Rate limit",
                                                                              "red")
    print("\033[H\033[J")
    print("*" * 25)
    print(args.email)
    print("*" * 25)
    for i in sorted(infos):
        key, value = i, infos[i]
        i = value
        if i["rateLimit"] == True:
            websiteprint = colored(key, "red")
        elif i["exists"] == False:
            websiteprint = colored(key, "magenta")
        else:
            toprint = ""
            if i["emailrecovery"] is not None:
                toprint += " " + i["emailrecovery"]
            if i["phoneNumber"] is not None:
                toprint += " / " + i["phoneNumber"]
            if i["others"] is not None:
                toprint += " / FullName " + i["others"]["FullName"]

            websiteprint = colored(str(key) + toprint, "green")
        print(websiteprint)

    print("\n" + description)
    print(str(len(websites)) + " websites checked in " +
          str(round(time.time() - start_time, 2)) + " seconds")

main()
