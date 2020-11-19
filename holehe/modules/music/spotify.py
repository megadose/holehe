import requests
import random
import json

from holehe import *


def spotify(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    params = (
        ('validate', '1'),
        ('email', email),
    )

    req = requests.get(
        'https://spclient.wg.spotify.com/signup/public/v1/account',
        headers=headers,
        params=params)
    if req.json()["status"] == 1:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif req.json()["status"] == 20:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
