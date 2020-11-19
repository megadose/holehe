import requests
import random

from holehe import *


def strava(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.strava.com/register/free?cta=sign-up&element=button&source=website_show',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    s=requests.session()
    r=s.get("https://www.strava.com/register/free?cta=sign-up&element=button&source=website_show",headers=headers)
    try:
        headers['X-CSRF-Token']= r.text.split('<meta name="csrf-token" content="')[1].split('"')[0]
    except:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    headers['X-Requested-With']= 'XMLHttpRequest'

    params = (
        ('email', email),
    )

    response = s.get('https://www.strava.com/athletes/email_unique', headers=headers, params=params)

    if response.text=="false":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.text=="true":
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
