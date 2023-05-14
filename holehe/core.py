from bs4 import BeautifulSoup
from termcolor import colored
import httpx
import trio

from subprocess import Popen, PIPE
import os
from argparse import ArgumentParser
import csv
from datetime import datetime
import time
import importlib
import pkgutil
import hashlib
import re
import sys
import string
import random
import json

from holehe.localuseragent import ua
from holehe.instruments import TrioProgress


try:
    import cookielib
except Exception:
    import http.cookiejar as cookielib


DEBUG        = False
EMAIL_FORMAT = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

__version__ = "1.61"


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


def get_functions(modules,args=None):
    """Transform the modules objects to functions"""
    websites = []

    for module in modules:
        if len(module.split(".")) > 3 :
            modu = modules[module]
            site = module.split(".")[-1]
            if args is not None and args.nopasswordrecovery==True:
                if  "adobe" not in str(modu.__dict__[site]) and "mail_ru" not in str(modu.__dict__[site]) and "odnoklassniki" not in str(modu.__dict__[site]) and "samsung" not in str(modu.__dict__[site]):
                    websites.append(modu.__dict__[site])
            else:
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

def is_email(email: str) -> bool:
    """Check if the input is a valid email address

    Keyword Arguments:
    email       -- String to be tested

    Return Value:
    Boolean     -- True if string is an email, False otherwise
    """

    return bool(re.fullmatch(EMAIL_FORMAT, email))

def print_result(data,args,email,start_time,websites):
    def print_color(text,color,args):
        if args.nocolor == False:
            return(colored(text,color))
        else:
            return(text)

    description = print_color("[+] Email used","green",args) + "," + print_color(" [-] Email not used", "magenta",args) + "," + print_color(" [x] Rate limit","yellow",args) + "," + print_color(" [!] Error","red",args)
    if args.noclear==False:
        print("\033[H\033[J")
    else:
        print("\n")
    print("*" * (len(email) + 6))
    print("   " + email)
    print("*" * (len(email) + 6))

    for results in data:
        if results["rateLimit"] and args.onlyused == False:
            websiteprint = print_color("[x] " + results["domain"], "yellow",args)
            print(websiteprint)
        elif "error" in results.keys() and results["error"] and args.onlyused == False:
            toprint = ""
            if results["others"] is not None and "Message" in str(results["others"].keys()):
                toprint = " Error message: " + results["others"]["errorMessage"]
            websiteprint = print_color("[!] " + results["domain"] + toprint, "red",args)
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

async def launch_module(module,email, client, out):
    data={'aboutme': 'about.me', 'adobe': 'adobe.com', 'amazon': 'amazon.com', 'anydo': 'any.do', 'archive': 'archive.org', 'armurerieauxerre': 'armurerie-auxerre.com', 'atlassian': 'atlassian.com', 'babeshows': 'babeshows.co.uk', 'badeggsonline': 'badeggsonline.com', 'biosmods': 'bios-mods.com', 'biotechnologyforums': 'biotechnologyforums.com', 'bitmoji': 'bitmoji.com', 'blablacar': 'blablacar.com', 'blackworldforum': 'blackworldforum.com', 'blip': 'blip.fm', 'blitzortung': 'forum.blitzortung.org', 'bluegrassrivals': 'bluegrassrivals.com', 'bodybuilding': 'bodybuilding.com', 'buymeacoffee': 'buymeacoffee.com', 'cambridgemt': 'discussion.cambridge-mt.com', 'caringbridge': 'caringbridge.org', 'chinaphonearena': 'chinaphonearena.com', 'clashfarmer': 'clashfarmer.com', 'codecademy': 'codecademy.com', 'codeigniter': 'forum.codeigniter.com', 'codepen': 'codepen.io', 'coroflot': 'coroflot.com', 'cpaelites': 'cpaelites.com', 'cpahero': 'cpahero.com', 'cracked_to': 'cracked.to', 'crevado': 'crevado.com', 'deliveroo': 'deliveroo.com', 'demonforums': 'demonforums.net', 'devrant': 'devrant.com', 'diigo': 'diigo.com', 'discord': 'discord.com', 'docker': 'docker.com', 'dominosfr': 'dominos.fr', 'ebay': 'ebay.com', 'ello': 'ello.co', 'envato': 'envato.com', 'eventbrite': 'eventbrite.com', 'evernote': 'evernote.com', 'fanpop': 'fanpop.com', 'firefox': 'firefox.com', 'flickr': 'flickr.com', 'freelancer': 'freelancer.com', 'freiberg': 'drachenhort.user.stunet.tu-freiberg.de', 'garmin': 'garmin.com', 'github': 'github.com', 'google': 'google.com', 'gravatar': 'gravatar.com', 'imgur': 'imgur.com', 'instagram': 'instagram.com', 'issuu': 'issuu.com', 'koditv': 'forum.kodi.tv', 'komoot': 'komoot.com', 'laposte': 'laposte.fr', 'lastfm': 'last.fm', 'lastpass': 'lastpass.com', 'mail_ru': 'mail.ru', 'mybb': 'community.mybb.com', 'myspace': 'myspace.com', 'nattyornot': 'nattyornotforum.nattyornot.com', 'naturabuy': 'naturabuy.fr', 'ndemiccreations': 'forum.ndemiccreations.com', 'nextpvr': 'forums.nextpvr.com', 'nike': 'nike.com', 'odnoklassniki': 'ok.ru', 'office365': 'office365.com', 'onlinesequencer': 'onlinesequencer.net', 'parler': 'parler.com', 'patreon': 'patreon.com', 'pinterest': 'pinterest.com', 'plurk': 'plurk.com', 'pornhub': 'pornhub.com', 'protonmail': 'protonmail.ch', 'quora': 'quora.com', 'rambler': 'rambler.ru', 'redtube': 'redtube.com', 'replit': 'replit.com', 'rocketreach': 'rocketreach.co', 'samsung': 'samsung.com', 'seoclerks': 'seoclerks.com', 'sevencups': '7cups.com', 'smule': 'smule.com', 'snapchat': 'snapchat.com', 'soundcloud': 'soundcloud.com', 'sporcle': 'sporcle.com', 'spotify': 'spotify.com', 'strava': 'strava.com', 'taringa': 'taringa.net', 'teamtreehouse': 'teamtreehouse.com', 'tellonym': 'tellonym.me', 'thecardboard': 'thecardboard.org', 'therianguide': 'forums.therian-guide.com', 'thevapingforum': 'thevapingforum.com', 'tumblr': 'tumblr.com', 'tunefind': 'tunefind.com', 'twitter': 'twitter.com', 'venmo': 'venmo.com', 'vivino': 'vivino.com', 'voxmedia': 'voxmedia.com', 'vrbo': 'vrbo.com', 'vsco': 'vsco.co', 'wattpad': 'wattpad.com', 'wordpress': 'wordpress.com', 'xing': 'xing.com', 'xnxx': 'xnxx.com', 'xvideos': 'xvideos.com', 'yahoo': 'yahoo.com','hubspot': 'hubspot.com', 'pipedrive': 'pipedrive.com', 'insightly': 'insightly.com', 'nutshell': 'nutshell.com', 'zoho': 'zoho.com', 'axonaut': 'axonaut.com', 'amocrm': 'amocrm.com', 'nimble': 'nimble.com', 'nocrm': 'nocrm.io', 'teamleader': 'teamleader.eu'}
    try:
        await module(email, client, out)
    except Exception:
        name=str(module).split('<function ')[1].split(' ')[0]
        out.append({"name": name,"domain":data[name],
                    "rateLimit": False,
                    "error": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
async def maincore():
    parser= ArgumentParser(description=f"holehe v{__version__}")
    parser.add_argument("email",
                    nargs='+', metavar='EMAIL',
                    help="Target Email")
    parser.add_argument("--only-used", default=False, required=False,action="store_true",dest="onlyused",
                    help="Displays only the sites used by the target email address.")
    parser.add_argument("--no-color", default=False, required=False,action="store_true",dest="nocolor",
                    help="Don't color terminal output")
    parser.add_argument("--no-clear", default=False, required=False,action="store_true",dest="noclear",
                    help="Do not clear the terminal to display the results")
    parser.add_argument("-NP","--no-password-recovery", default=False, required=False,action="store_true",dest="nopasswordrecovery",
                    help="Do not try password recovery on the websites")
    parser.add_argument("-C","--csv", default=False, required=False,action="store_true",dest="csvoutput",
                    help="Create a CSV with the results")
    parser.add_argument("-T","--timeout", type=int , default=10, required=False,dest="timeout",
                    help="Set max timeout value (default 10)")

    check_update()
    args = parser.parse_args()
    credit()
    email=args.email[0]

    if not is_email(email):
        exit("[-] Please enter a target email ! \nExample : holehe email@example.com")

    # Import Modules
    modules = import_submodules("holehe.modules")
    websites = get_functions(modules,args)
    # Get timeout
    timeout=args.timeout
    # Start time
    start_time = time.time()
    # Def the async client
    client = httpx.AsyncClient(timeout=timeout)
    # Launching the modules
    out = []
    instrument = TrioProgress(len(websites))
    trio.lowlevel.add_instrument(instrument)
    async with trio.open_nursery() as nursery:
        for website in websites:
            nursery.start_soon(launch_module, website, email, client, out)
    trio.lowlevel.remove_instrument(instrument)
    # Sort by modules names
    out = sorted(out, key=lambda i: i['name'])
    # Close the client
    await client.aclose()
    # Print the result
    print_result(out,args,email,start_time,websites)
    credit()
    # Export results
    export_csv(out,args,email)

def main():
    trio.run(maincore)
