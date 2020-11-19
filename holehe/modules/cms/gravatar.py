<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *
=======
import requests
import random
from bs4 import BeautifulSoup
import hashlib

from holehe.localuseragent import ua
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def gravatar(email):
    hashed_name =  hashlib.md5(email.encode()).hexdigest()
    r =  requests.get('https://gravatar.com/{hashed_name}.json')
    if r.status_code != 200:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        try:
            data = r.json()
            name = data['entry'][0]['name'].get('formatted')
            others = {
                'FullName': name,
            }

            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": others})
        except BaseException:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
