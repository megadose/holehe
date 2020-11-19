<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *
=======
import requests
import random


from holehe import *
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def firefox(email):
    req = requests.post(
        "https://api.accounts.firefox.com/v1/account/status",
        data={
            "email": email})
    if "false" in req.text:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    elif "true" in req.text:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
