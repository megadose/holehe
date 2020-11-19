<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *

=======
import requests
import random
import json
from holehe import *
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb


def anydo(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://desktop.any.do/',
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Platform': '3',
        'Origin': 'https://desktop.any.do',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"email":"'+email+'"}'

    response = requests.post('https://sm-prod2.any.do/check_email', headers=headers, data=data)
    if response.status_code==200:
        if response.json()["user_exists"]==True:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
