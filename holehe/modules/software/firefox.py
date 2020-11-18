import requests
import random


from holehe import *

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
