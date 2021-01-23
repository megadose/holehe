import time
import importlib
import pkgutil
from termcolor import colored
import httpx
import trio
from subprocess import Popen, PIPE
import os
from argparse import ArgumentParser
import csv
from datetime import datetime

from bs4 import BeautifulSoup
import hashlib
import re
import sys
import string
import random
import json
from holehe.localuseragent import ua

try:
    import cookielib
except BaseException:
    import http.cookiejar as cookielib


DEBUG = False

__version__ = "1.58.6.7"


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

def check_update():
    """Check and update holehe if not the last version"""
    check_version = httpx.get("https://pypi.org/pypi/holehe/json")
    if check_version.json()["info"]["version"] != __version__:
        if os.name != 'nt':
            p = Popen(["pip3",
                       "install",
                       "--upgrade",
                       "holehe"],
                      stdout=PIPE,
                      stderr=PIPE)
        else:
            p = Popen(["pip",
                       "install",
                       "--upgrade",
                       "holehe"],
                      stdout=PIPE,
                      stderr=PIPE)
        (output, err) = p.communicate()
        p_status = p.wait()
        print("Holehe has just been updated, you can restart it.")
        exit()

def credit():
    """Print Credit"""
    print('Twitter : @palenath')
    print('Github : https://github.com/megadose/holehe')
    print('For BTC Donations : 1FHDM49QfZX6pJmhjLE5tB2K6CaTLMZpXZ')

def check_if_email(email):
    """Check if len < 5"""
    if len(email) < 5:
        exit("[-] Please enter a target email ! \nExample : holehe email@example.com")

def print_result(data,args,email,start_time,websites):
    def print_color(text,color,args):
        if args.nocolor == False:
            return(colored(text,color))
        else:
            return(text)

    description = print_color("[+] Email used","green",args) + "," + print_color(" [-] Email not used", "magenta",args) + "," + print_color(" [x] Rate limit","red",args)
    print("\033[H\033[J")
    print("*" * (len(email) + 6))
    print("   " + email)
    print("*" * (len(email) + 6))

    for results in data:
        if results["rateLimit"] and args.onlyused == False:
            websiteprint = print_color("[x] " + results["domain"], "red",args)
            print(websiteprint)
        elif results["exists"] == False and args.onlyused == False:
            websiteprint = print_color("[-] " + results["domain"], "magenta",args)
            print(websiteprint)
        elif results["exists"] == True:
            toprint = ""
            if results["emailrecovery"] is not None:
                toprint += " " + results["emailrecovery"]
            if results["phoneNumber"] is not None:
                toprint += " / " + results["phoneNumber"]
            if results["others"] is not None and "FullName" in str(results["others"].keys()):
                toprint += " / FullName " + results["others"]["FullName"]
            if results["others"] is not None and "Date, time of the creation" in str(results["others"].keys()):
                toprint += " / Date, time of the creation " + results["others"]["Date, time of the creation"]

            websiteprint = print_color("[+] " + results["domain"] + toprint, "green",args)
            print(websiteprint)

    print("\n" + description)
    print(str(len(websites)) + " websites checked in " +
          str(round(time.time() - start_time, 2)) + " seconds")


def get_timeout():
    """Get Timeout from Gravatar.com"""
    check_timeout = httpx.get("https://gravatar.com")
    timeout_value=int(check_timeout.elapsed.total_seconds()*6)+5
    return(timeout_value)

def export_csv(data,args,email):
    """Export result to csv"""
    if args.csvoutput == True:
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        name_file="holehe_"+str(round(timestamp))+"_"+email+"_results.csv"
        with open(name_file, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file,fieldnames=data[0].keys())
            fc.writeheader()
            fc.writerows(data)
        exit("All results have been exported to "+name_file)

async def launch_module(module,email, client, out, args):
    await module(email, client, out)

async def maincore():
    parser= ArgumentParser(description=f"holehe v{__version__}")
    parser.add_argument("email",
                    nargs='+', metavar='EMAIL',
                    help="Target Email")
    parser.add_argument("--only-used", default=False, required=False,action="store_true",dest="onlyused",
                    help="Displays only the sites used by the target email address.")
    parser.add_argument("--no-color", default=False, required=False,action="store_true",dest="nocolor",
                    help="Don't color terminal output")
    parser.add_argument("-C","--csv", default=False, required=False,action="store_true",dest="csvoutput",
                    help="Create a CSV with the results")

    check_update()
    args = parser.parse_args()
    credit()
    email=args.email[0]
    check_if_email(email)


    # Import Modules
    modules = import_submodules("holehe.modules")
    websites = get_functions(modules)
    # Get timeout
    timeout=get_timeout()
    # Start time
    start_time = time.time()
    # Def the async client
    client = httpx.AsyncClient(timeout=timeout)
    # Launching the modules
    out = []
    async with trio.open_nursery() as nursery:
        for website in websites:
            nursery.start_soon(launch_module, website, email, client, out ,args)

    # Sort by modules names
    out = sorted(out, key=lambda i: i['name'])
    # Close the client
    await client.aclose()
    # Print the result
    print_result(out,args,email,start_time,websites)
    # Export results
    export_csv(out,args,email)

def main():
    trio.run(maincore)
