<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *

=======
import requests
import random
import json

from holehe import *
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def rambler(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://id.rambler.ru/champ/registration',
        'Content-Type': 'application/json',
        'Origin': 'https://id.rambler.ru',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    data = '{"method":"Rambler::Id::get_email_account_info","params":[{"email":"' + email + '"}],"rpc":"2.0"}'

    response = requests.post(
        'https://id.rambler.ru/jsonrpc',
        headers=headers,
        data=data)
    try:
        if response.json()["result"]["exists"] == 0:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
