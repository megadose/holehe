import requests
import json
import random
from holehe.localuseragent import ua

s = requests.session()

def xvideos(email):
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://www.xvideos.com/',
    }

    params = (
        ('email', email),
    )

    response = s.get('https://www.xvideos.com/account/checkemail', headers=headers, params=params)
    try:
        if response.json()['result'] == False:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
