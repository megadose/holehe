import requests
import random

from holehe import *


def myspace(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Origin': 'https://myspace.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://myspace.com/signup/email',
    }

    s=requests.session()

    r=s.get("https://myspace.com/signup/email",headers=headers,timeout=3)

    headers['Content-Type']= 'application/x-www-form-urlencoded; charset=UTF-8'
    try:
        headers['Hash']= r.text.split('<input name="csrf" type="hidden" value="')[1].split('"')[0]
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    headers['X-Requested-With']= 'XMLHttpRequest'

    data = {
      'email': email
    }

    response = requests.post('https://myspace.com/ajax/account/validateemail', headers=headers, data=data,timeout=3)
    try:
        if "This email address was already used to create an account." in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
