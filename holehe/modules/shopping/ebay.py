<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *

=======
import requests
import random
import json
from holehe.localuseragent import ua
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def ebay(email):

    s = requests.session()
    s.headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.ebay.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    try:
        srt = s.get(
            "https://www.ebay.com/signin/").text.split('"csrfAjaxToken":"')[1].split('"')[0]
    except IndexError as e:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    data = {
        'identifier': email,
        'srt': srt
    }

    response = s.post(
        'https://signin.ebay.com/signin/srv/identifer',
        data=data).json()
    if "err" in response.keys():
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
