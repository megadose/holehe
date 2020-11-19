<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *
=======
import requests
import random
import json

from bs4 import BeautifulSoup

from holehe.localuseragent import ua


>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def buymeacoffee(email):
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return(result_str)
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.buymeacoffee.com',
        'DNT': '1',
        'TE': 'Trailers',
    }
    r = requests.get("https://www.buymeacoffee.com/", headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(req.content, features="lxml")
        csrf_token = soup.find(attrs={'name': 'bmc_csrf_token'}).get("value")
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    cookies = {
        'bmccsrftoken': csrf_token,
    }
    data = {
        'email': email,
        'password': get_random_string(20),
        'bmc_csrf_token': csrf_token
    }

    r = requests.post(
        'https://www.buymeacoffee.com/auth/validate_email_and_password',
        headers=headers,
        cookies=cookies,
        data=data)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "SUCCESS":
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif data["status"] == "FAIL" and "email" in str(data):
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
