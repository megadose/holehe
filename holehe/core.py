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
