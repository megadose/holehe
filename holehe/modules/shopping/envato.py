<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *

=======
import requests
import random
from holehe.localuseragent import ua
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def envato(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://themeforest.net/',
        'Content-type': 'application/x-www-form-urlencoded',
        'Origin': 'https://themeforest.net',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = {
        'email': email
    }
    response = requests.post(
        'https://account.envato.com/api/validate_email',
        headers=headers,
        data=data)
    if 'Email is already in use' in response.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif "Page designed by Kotulsky" in response.text:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
