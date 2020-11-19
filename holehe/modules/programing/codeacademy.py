<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *

=======
import requests
import random
from holehe.localuseragent import ua
from bs4 import BeautifulSoup
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def codeacademy(email):
    s = requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.codecademy.com/register?redirect=%2',
        'Content-Type': 'application/json',
        'Origin': 'https://www.codecademy.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    req = s.get(
        "https://www.codecademy.com/register?redirect=%2F",
        headers=headers)
    soup = BeautifulSoup(req.content, features="lxml")
    try:
        headers["X-CSRF-Token"] = soup.find(
            attrs={"name": "csrf-token"}).get("content")
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    data = '{"user":{"email":"' + email + '"}}'

    response = s.post(
        'https://www.codecademy.com/register/validate',
        headers=headers,
        data=data)
    if 'is already taken' in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
