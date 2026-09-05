# -*- coding: utf-8 -*-
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

from mailscope.localuseragent import ua
from mailscope.instruments import TrioProgress
from mailscope.defense import RateLimitedException, RequestPacer
from mailscope.proxy import ClientManager, ProxyRotator, SiteClient


try:
    import cookielib
except Exception:
    import http.cookiejar as cookielib


DEBUG = False
EMAIL_FORMAT = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
__version__ = "2.0.0"

MODULE_DOMAINS = {
    'aboutme': 'about.me', 'adobe': 'adobe.com', 'amazon': 'amazon.com', 'anydo': 'any.do',
    'archive': 'archive.org', 'armurerieauxerre': 'armurerie-auxerre.com', 'atlassian': 'atlassian.com',
    'babeshows': 'babeshows.co.uk', 'badeggsonline': 'badeggsonline.com', 'biosmods': 'bios-mods.com',
    'biotechnologyforums': 'biotechnologyforums.com', 'bitmoji': 'bitmoji.com', 'blablacar': 'blablacar.com',
    'blackworldforum': 'blackworldforum.com', 'blip': 'blip.fm', 'blitzortung': 'forum.blitzortung.org',
    'bluegrassrivals': 'bluegrassrivals.com', 'bodybuilding': 'bodybuilding.com', 'buymeacoffee': 'buymeacoffee.com',
    'cambridgemt': 'discussion.cambridge-mt.com', 'caringbridge': 'caringbridge.org', 'chinaphonearena': 'chinaphonearena.com',
    'clashfarmer': 'clashfarmer.com', 'codecademy': 'codecademy.com', 'codeigniter': 'forum.codeigniter.com',
    'codepen': 'codepen.io', 'coroflot': 'coroflot.com', 'cpaelites': 'cpaelites.com', 'cpahero': 'cpahero.com',
    'cracked_to': 'cracked.to', 'crevado': 'crevado.com', 'deliveroo': 'deliveroo.com', 'demonforums': 'demonforums.net',
    'devrant': 'devrant.com', 'diigo': 'diigo.com', 'discord': 'discord.com', 'docker': 'docker.com',
    'dominosfr': 'dominos.fr', 'duolingo': 'duolingo.com', 'ebay': 'ebay.com', 'ello': 'ello.co',
    'envato': 'envato.com', 'eventbrite': 'eventbrite.com', 'evernote': 'evernote.com', 'facebook': 'facebook.com',
    'fanpop': 'fanpop.com', 'firefox': 'firefox.com', 'flickr': 'flickr.com', 'freelancer': 'freelancer.com',
    'freiberg': 'drachenhort.user.stunet.tu-freiberg.de', 'garmin': 'garmin.com', 'github': 'github.com',
    'google': 'google.com', 'gravatar': 'gravatar.com', 'imgur': 'imgur.com', 'instagram': 'instagram.com',
    'issuu': 'issuu.com', 'koditv': 'forum.kodi.tv', 'komoot': 'komoot.com', 'laposte': 'laposte.fr',
    'lastfm': 'last.fm', 'lastpass': 'lastpass.com', 'mail_ru': 'mail.ru', 'mybb': 'community.mybb.com',
    'myspace': 'myspace.com', 'nattyornot': 'nattyornotforum.nattyornot.com', 'naturabuy': 'naturabuy.fr',
    'ndemiccreations': 'forum.ndemiccreations.com', 'nextpvr': 'forums.nextpvr.com', 'nike': 'nike.com',
    'odnoklassniki': 'ok.ru', 'office365': 'office365.com', 'onlinesequencer': 'onlinesequencer.net',
    'parler': 'parler.com', 'patreon': 'patreon.com', 'pinterest': 'pinterest.com', 'plurk': 'plurk.com',
    'pornhub': 'pornhub.com', 'protonmail': 'protonmail.ch', 'quora': 'quora.com', 'rambler': 'rambler.ru',
    'redtube': 'redtube.com', 'replit': 'replit.com', 'rocketreach': 'rocketreach.co', 'samsung': 'samsung.com',
    'seoclerks': 'seoclerks.com', 'sevencups': '7cups.com', 'smule': 'smule.com', 'snapchat': 'snapchat.com',
    'soundcloud': 'soundcloud.com', 'sporcle': 'sporcle.com', 'spotify': 'spotify.com', 'strava': 'strava.com',
    'taringa': 'taringa.net', 'teamtreehouse': 'teamtreehouse.com', 'tellonym': 'tellonym.me',
    'thecardboard': 'thecardboard.org', 'therianguide': 'forums.therian-guide.com', 'thevapingforum': 'thevapingforum.com',
    'tumblr': 'tumblr.com', 'tunefind': 'tunefind.com', 'twitter': 'twitter.com', 'venmo': 'venmo.com',
    'vivino': 'vivino.com', 'voxmedia': 'voxmedia.com', 'vrbo': 'vrbo.com', 'vsco': 'vsco.co',
    'wattpad': 'wattpad.com', 'wordpress': 'wordpress.com', 'xing': 'xing.com', 'xnxx': 'xnxx.com',
    'xvideos': 'xvideos.com', 'yahoo': 'yahoo.com', 'hubspot': 'hubspot.com', 'pipedrive': 'pipedrive.com',
    'insightly': 'insightly.com', 'nutshell': 'nutshell.com', 'zoho': 'zoho.com', 'axonaut': 'axonaut.com',
    'amocrm': 'amocrm.com', 'nimble': 'nimble.com', 'nocrm': 'nocrm.io', 'teamleader': 'teamleader.eu'
}


def import_submodules(package, recursive=True):
    """Get all MailScope submodules."""
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def list_available_sites(modules):
    """Print all available modules and exit."""
    websites = []
    for module_path, mod_obj in sorted(modules.items()):
        parts = module_path.split(".")
        if len(parts) > 3:
            category = parts[2]
            site_name = parts[-1]
            func = mod_obj.__dict__.get(site_name)
            if func:
                domain = MODULE_DOMAINS.get(site_name, f"{site_name}.com")
                websites.append((site_name, domain, category))

    print("\n" + "=" * 65)
    print(f" MailScope v{__version__} - Available Modules ({len(websites)} total)")
    print("=" * 65)
    print(f" {'MODULE':<24} {'DOMAIN':<26} {'CATEGORY'}")
    print("-" * 65)
    for name, domain, category in websites:
        print(f" {name:<24} {domain:<26} {category}")
    print("=" * 65 + "\n")
    sys.exit(0)


def get_functions(modules, args=None):
    """Transform the modules objects to functions and apply module filters."""
    websites = []

    only_filter = None
    if args and getattr(args, "only_modules", None):
        only_filter = set()
        for item in args.only_modules:
            for sub in item.split(","):
                sub = sub.strip().lower()
                if sub:
                    only_filter.add(sub)

    exclude_filter = set()
    if args and getattr(args, "exclude_modules", None):
        for item in args.exclude_modules:
            for sub in item.split(","):
                sub = sub.strip().lower()
                if sub:
                    exclude_filter.add(sub)

    for module in modules:
        if len(module.split(".")) > 3:
            modu = modules[module]
            site = module.split(".")[-1]
            func = modu.__dict__.get(site)
            if not func:
                continue

            site_lower = site.lower()
            domain_lower = MODULE_DOMAINS.get(site, f"{site}.com").lower()

            # Check --only filter
            if only_filter is not None:
                if site_lower not in only_filter and domain_lower not in only_filter:
                    continue

            # Check --exclude filter
            if site_lower in exclude_filter or domain_lower in exclude_filter:
                continue

            # Legacy --no-password-recovery
            if args is not None and getattr(args, "nopasswordrecovery", False):
                if site in ("adobe", "mail_ru", "odnoklassniki", "samsung"):
                    continue

            websites.append(func)

    return websites


def check_update():
    """Check for MailScope updates safely without crashing if unreachable."""
    try:
        check_version = httpx.get("https://pypi.org/pypi/mailscope/json", timeout=3.0)
        if check_version.status_code == 200:
            latest_v = check_version.json()["info"]["version"]
            if latest_v != __version__:
                pip_cmd = ["pip3" if os.name != 'nt' else "pip", "install", "--upgrade", "mailscope"]
                p = Popen(pip_cmd, stdout=PIPE, stderr=PIPE)
                p.communicate()
                print("MailScope has been updated to the latest version. Please restart.")
                exit(0)
    except Exception:
        pass


def credit():
    """Print Credit & Header"""
    print(f"MailScope v{__version__} | OSINT Email Checker with 429 Defense & Proxy Rotation")
    print("Twitter : @palenath | Github : https://github.com/megadose/holehe")


def is_email(email: str) -> bool:
    """Check if the input is a valid email address."""
    return bool(re.fullmatch(EMAIL_FORMAT, email))


def print_result(data, args, email, start_time, websites):
    def print_color(text, color, args):
        if args.nocolor:
            return text
        return colored(text, color)

    description = (
        print_color("[+] Email used", "green", args) + ", " +
        print_color("[-] Email not used", "magenta", args) + ", " +
        print_color("[x] Rate limit", "yellow", args) + ", " +
        print_color("[!] Error", "red", args)
    )

    if not args.noclear:
        print("\033[H\033[J")
    else:
        print("\n")

    print("*" * (len(email) + 6))
    print("   " + email)
    print("*" * (len(email) + 6))

    for results in data:
        is_rate_limited = results.get("rate_limited", False) or results.get("rateLimit", False)
        if is_rate_limited and not args.onlyused:
            websiteprint = print_color("[x] " + results["domain"], "yellow", args)
            print(websiteprint)
        elif results.get("error", False) and not args.onlyused:
            toprint = ""
            if results.get("others") and "errorMessage" in results["others"]:
                toprint = " Error message: " + results["others"]["errorMessage"]
            websiteprint = print_color("[!] " + results["domain"] + toprint, "red", args)
            print(websiteprint)
        elif not results.get("exists", False) and not args.onlyused:
            websiteprint = print_color("[-] " + results["domain"], "magenta", args)
            print(websiteprint)
        elif results.get("exists", False):
            toprint = ""
            if results.get("emailrecovery"):
                toprint += " " + results["emailrecovery"]
            if results.get("phoneNumber"):
                toprint += " / " + results["phoneNumber"]
            if results.get("others") and "FullName" in results["others"]:
                toprint += " / FullName " + results["others"]["FullName"]
            if results.get("others") and "Date, time of the creation" in results["others"]:
                toprint += " / Date, time of the creation " + results["others"]["Date, time of the creation"]

            websiteprint = print_color("[+] " + results["domain"] + toprint, "green", args)
            print(websiteprint)

    print("\n" + description)
    print(f"{len(websites)} websites checked in {round(time.time() - start_time, 2)} seconds\n")


def export_csv(data, args, email):
    """Export result to CSV file."""
    if getattr(args, "csvoutput", False):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        name_file = f"mailscope_{round(timestamp)}_{email}_results.csv"
        all_keys = [
            "name", "domain", "method", "frequent_rate_limit",
            "rateLimit", "rate_limited", "error", "exists",
            "emailrecovery", "phoneNumber", "others"
        ]
        with open(name_file, 'w', encoding='utf8', newline='') as output_file:
            fc = csv.DictWriter(output_file, fieldnames=all_keys, extrasaction='ignore')
            fc.writeheader()
            for row in data:
                row_copy = dict(row)
                row_copy.setdefault("rate_limited", row_copy.get("rateLimit", False))
                fc.writerow(row_copy)
        print(f"[+] All results have been exported to {name_file}")


async def launch_module(module, email, client_manager, out, limiter):
    """
    Executes a module check with concurrency limiting, per-site client isolation,
    human-like pacing, proxy rotation, and clean rate limit defense.
    """
    async with limiter:
        name = getattr(module, "__name__", str(module))
        domain = MODULE_DOMAINS.get(name, f"{name}.com")
        site_client = await client_manager.create_client()

        try:
            await module(email, site_client, out)
        except RateLimitedException:
            # Cleanly flag the result as rate_limited instead of failing unhandled
            out[:] = [r for r in out if r.get("name") != name]
            out.append({
                "name": name,
                "domain": domain,
                "method": "rate_limit",
                "frequent_rate_limit": True,
                "rateLimit": True,
                "rate_limited": True,
                "error": False,
                "exists": False,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None
            })
        except Exception as e:
            # Check if module already recorded an entry
            already_appended = any(r.get("name") == name for r in out)
            if not already_appended:
                out.append({
                    "name": name,
                    "domain": domain,
                    "method": "error",
                    "frequent_rate_limit": False,
                    "rateLimit": False,
                    "rate_limited": False,
                    "error": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": {"errorMessage": str(e)}
                })
        finally:
            await site_client.aclose()


async def maincore():
    parser = ArgumentParser(description=f"MailScope v{__version__} - OSINT Email Checker with Rate Limit Defense & Proxy Rotation")
    parser.add_argument("email", nargs='*', metavar='EMAIL', help="Target Email")
    parser.add_argument("--only-used", default=False, required=False, action="store_true", dest="onlyused",
                        help="Displays only the sites used by the target email address.")
    parser.add_argument("--no-color", default=False, required=False, action="store_true", dest="nocolor",
                        help="Don't color terminal output")
    parser.add_argument("--no-clear", default=False, required=False, action="store_true", dest="noclear",
                        help="Do not clear the terminal to display the results")
    parser.add_argument("-NP", "--no-password-recovery", default=False, required=False, action="store_true", dest="nopasswordrecovery",
                        help="Do not try password recovery on the websites")
    parser.add_argument("-C", "--csv", default=False, required=False, action="store_true", dest="csvoutput",
                        help="Create a CSV with the results")
    parser.add_argument("-T", "--timeout", type=int, default=10, required=False, dest="timeout",
                        help="Set max timeout value (default: 10s)")

    # Goal 2: Concurrency & Pacing
    parser.add_argument("--sequential", default=False, required=False, action="store_true", dest="sequential",
                        help="Run checks sequentially (worker concurrency = 1).")
    parser.add_argument("-c", "--concurrency", type=int, default=2, required=False, dest="concurrency",
                        help="Maximum concurrent worker ceiling (default: 2).")

    # Goal 3: Proxy & IP Rotation
    parser.add_argument("--proxy", type=str, default=None, required=False, dest="proxy",
                        help="Route all requests through a single HTTP/SOCKS5 proxy (e.g. http://127.0.0.1:8080 or socks5://127.0.0.1:1080).")
    parser.add_argument("--proxy-file", type=str, default=None, required=False, dest="proxy_file",
                        help="Path to a file containing a list of proxies (one per line) for round-robin and 429 rotation.")

    # Goal 4: Module Filtering & Inspection
    parser.add_argument("--only", nargs="+", default=None, required=False, dest="only_modules",
                        help="Run checks only on selected sites/modules (names or domains).")
    parser.add_argument("--exclude", nargs="+", default=None, required=False, dest="exclude_modules",
                        help="Skip specified sites/modules from checks (names or domains).")
    parser.add_argument("--list-sites", default=False, required=False, action="store_true", dest="list_sites",
                        help="Print all available modules and exit.")

    check_update()
    args = parser.parse_args()

    # Import modules
    modules = import_submodules("mailscope.modules")

    # Handle --list-sites
    if args.list_sites:
        list_available_sites(modules)

    # Check for target email
    if not args.email:
        sys.exit("[-] Please enter a target email!\nExample : mailscope email@example.com\nFor all options : mailscope --help")

    credit()
    email = args.email[0]

    if not is_email(email):
        sys.exit("[-] Please enter a valid target email address!\nExample : mailscope email@example.com")

    if args.proxy_file and not os.path.isfile(args.proxy_file):
        sys.exit(f"[-] Proxy file not found: {args.proxy_file}")

    websites = get_functions(modules, args)
    if not websites:
        sys.exit("[-] No modules to run after applying filters. Check --only / --exclude options.")

    # Concurrency control ceiling
    concurrency = 1 if args.sequential else max(1, args.concurrency)
    limiter = trio.CapacityLimiter(concurrency)

    # Client Manager with pacing and proxy rotation
    client_manager = ClientManager(
        proxy=args.proxy,
        proxy_file=args.proxy_file,
        timeout=args.timeout,
        min_delay=0.5,
        max_delay=1.8
    )

    start_time = time.time()
    out = []
    instrument = TrioProgress(len(websites))
    trio.lowlevel.add_instrument(instrument)

    async with trio.open_nursery() as nursery:
        for website in websites:
            nursery.start_soon(launch_module, website, email, client_manager, out, limiter)

    trio.lowlevel.remove_instrument(instrument)

    out = sorted(out, key=lambda i: i['name'])
    print_result(out, args, email, start_time, websites)
    credit()
    export_csv(out, args, email)


def main():
    trio.run(maincore)


if __name__ == "__main__":
    main()
