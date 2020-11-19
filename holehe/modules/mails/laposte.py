<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *
=======
import requests
import random
from bs4 import BeautifulSoup

from holehe.localuseragent import ua
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def laposte(email):
    headers = {
        'Origin': 'https://www.laposte.fr',
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://www.laposte.fr/authentification',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'email': email,
        'customerId': '',
        'tunnelSteps': ''
        }

    response = requests.post('https://www.laposte.fr/authentification', headers=headers, data=data)
    post_soup = BeautifulSoup(response.content , 'lxml')
    l = post_soup.find_all('span', id="wrongEmail")
    return({"rateLimit": False, "exists": l != [], "emailrecovery": None, "phoneNumber": None, "others": None})
