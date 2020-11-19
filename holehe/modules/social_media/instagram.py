<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *

=======
import requests
import random
import json

import string

from holehe.localuseragent import ua
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb


def instagram(email):
    s = requests.session()
    s.headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.instagram.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    freq = s.get("https://www.instagram.com/accounts/emailsignup/")
    token = freq.text.split('{"config":{"csrf_token":"')[1].split('"')[0]
    data = {
        'email': email,
        'username': '',
        'first_name': '',
        'opt_into_one_tap': 'false'
    }

    check = s.post(
        "https://www.instagram.com/accounts/web_create_ajax/attempt/",
        data=data,
        headers={
            "x-csrftoken": token}).json()
    if 'email' in check["errors"].keys():
        if check["errors"]["email"][0]["code"] == "email_is_taken":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif "email_sharing_limit" in str(check["errors"]):
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
