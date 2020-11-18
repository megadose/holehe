import requests
import random
from holehe.localuseragent import ua

def nike(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'https://www.nike.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.nike.com/',
        'TE': 'Trailers',
    }

    params = (
        ('appVersion', '831'),
        ('experienceVersion', '831'),
        ('uxid', 'com.nike.commerce.nikedotcom.web'),
        ('locale', 'fr_FR'),
        ('backendEnvironment', 'identity'),
        ('browser', ''),
        ('mobile', 'false'),
        ('native', 'false'),
        ('visit', '1'),
    )

    data = '{"emailAddress":"' + email + '"}'

    response = requests.post(
        'https://unite.nike.com/account/email/v1',
        headers=headers,
        params=params,
        data=data)
    if response.status_code == 409:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif response.status_code == 204:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
