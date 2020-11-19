import requests
import random
from holehe.localuseragent import ua
from bs4 import BeautifulSoup

def freelancer(email):
    s = requests.session()
    s.headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/json',
        'Origin': 'https://www.freelancer.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    params = (
        ('compact', 'true'),
        ('new_errors', 'true'),
    )

    data = '{"user":{"email":"' + email + '"}}'
    response = s.post(
        'https://www.freelancer.com/api/users/0.1/users/check',
        params=params,
        data=data)
    resData = response.json()
    if response.status_code == 409:
        if "EMAIL_ALREADY_IN_USE" in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})

    elif response.status_code == 200:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
