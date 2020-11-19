import requests
import random
from bs4 import BeautifulSoup
from holehe import *


def teamtreehouse(email):
    s = requests.Session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://teamtreehouse.com/subscribe/new?trial=yes',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://teamtreehouse.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    req = s.get(
        "https://teamtreehouse.com/subscribe/new?trial=yes",
        headers=headers)
    soup = BeautifulSoup(req.content, features="lxml")
    token = soup.find(attrs={"name": "csrf-token"}).get("content")
    headers['X-CSRF-Token'] = token

    data = {
        'email': email
    }

    response = s.post(
        'https://teamtreehouse.com/account/email_address',
        headers=headers,
        data=data)
    if 'that email address is taken.' in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.text == '{"success":true}':
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
