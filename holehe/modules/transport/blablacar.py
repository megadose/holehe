import requests
import json
import random

from holehe import *



def blablacar(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'fr_FR',
        'Referer': 'https://www.blablacar.fr/',
        'Content-Type': 'application/json',
        'x-locale': 'fr_FR',
        'x-currency': 'EUR',
        'x-client': 'SPA|1.0.0',
        'x-forwarded-proto': 'https',
        'Origin': 'https://www.blablacar.fr',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    try:
        appToken = requests.get(
            "https://www.blablacar.fr/register",
            headers=headers).text.split(',"appToken":"')[1].split('"')[0]
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    cookies = {
        'datadome': '',
    }

    headers["Authorization"] = 'Bearer ' + appToken

    response = requests.get(
        'https://edge.blablacar.fr/auth/validation/email/' +
        email,
        headers=headers,
        cookies=cookies)
    data = response.json()
    if "url" in data.keys():
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif "exists" in data.keys():
        return({"rateLimit": False, "exists": data["exists"], "emailrecovery": None, "phoneNumber": None, "others": None})
