<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *
=======
import requests
import random
from bs4 import BeautifulSoup


from holehe.localuseragent import ua

>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb


def pornhub(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    s = requests.session()
    req = s.get("https://www.pornhub.com/signup", headers=headers)
    soup = BeautifulSoup(req.content, features="lxml")
    try:
        toe = soup.find(attrs={"name": "token"}).get("value")
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    params = (
        ('token', toe),
    )

    data = {
        'check_what': 'email',
        'email': email
    }

    response = s.post(
        'https://www.pornhub.com/user/create_account_check',
        headers=headers,
        params=params,
        data=data)
    try:
        if response.json()["error_message"] == "Email has been taken.":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
