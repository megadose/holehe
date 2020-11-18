import requests
import random
from bs4 import BeautifulSoup

from holehe.localuseragent import ua



def dominosfr(email):
    s = requests.session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://commande.dominos.fr/eStore/fr/Signup',
    }

    s.get("https://commande.dominos.fr/eStore/fr/Signup",headers=headers)
    headers['X-Requested-With'] = 'XMLHttpRequest'

    params = (
        ('email', email),
    )

    response = requests.get('https://commande.dominos.fr/eStore/fr/Signup/IsEmailAvailable', headers=headers, params=params)
    if response.status_code==200:
        if response.text=="false":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
