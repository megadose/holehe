<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *

=======
import requests
import random
from holehe.localuseragent import ua

try:
    import cookielib
except BaseException:
    import http.cookiejar as cookielib
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb


def eventbrite(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.eventbrite.com/',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.eventbrite.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    req = requests.get(
        "https://www.eventbrite.com/signin/?referrer=%2F",
        headers=headers)
    try:
        csrf_token = req.cookies["csrftoken"]

    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    cookies = {
        'csrftoken': csrf_token,
    }

    headers["X-CSRFToken"] = csrf_token
    data = '{"email":"' + email + '"}'

    response = requests.post(
        'https://www.eventbrite.com/api/v3/users/lookup/',
        headers=headers,
        cookies=cookies,
        data=data)
    if response.status_code == 200:
        try:
            reqd = response.json()
            if reqd["exists"] == True:
                return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
            else:
                return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        except BaseException:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
