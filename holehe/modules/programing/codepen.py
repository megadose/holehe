import requests
import random
from holehe.localuseragent import ua
from bs4 import BeautifulSoup

def codepen(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://codepen.io/accounts/signup/user/free',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://codepen.io',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    try:
        s = requests.session()
        req = s.get(
            "https://codepen.io/accounts/signup/user/free",
            headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")
        token = soup.find(attrs={"name": "csrf-token"}).get("content")
        headers["X-CSRF-Token"] = token
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    data = {
        'attribute': 'email',
        'value': email,
        'context': 'user'
    }

    response = s.post(
        'https://codepen.io/accounts/duplicate_check',
        headers=headers,
        data=data)
    if "That Email is already taken." in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
