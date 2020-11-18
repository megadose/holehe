import requests
import random
from bs4 import BeautifulSoup

from holehe.localuseragent import ua

def imgur(email):
    s=requests.session()

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://imgur.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }


    r=requests.get("https://imgur.com/register?redirect=%2Fuser",headers=headers)


    headers["X-Requested-With"]="XMLHttpRequest"

    data = {
      'email': email
    }

    response = s.post('https://imgur.com/signin/ajax_email_available', headers=headers, data=data)
    if response.status_code==200:
        if response.json()["data"]["available"]==True:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
