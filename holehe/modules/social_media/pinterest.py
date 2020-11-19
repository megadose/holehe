<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *

=======
import requests
import random
import json

from holehe.localuseragent import ua
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def pinterest(email):
    req = requests.get(
        "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",
        params={
            "source_url": "/",
            "data": '{"options": {"email": "' + email + '"}, "context": {}}'})
    if req.json()["resource_response"]["data"]:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
