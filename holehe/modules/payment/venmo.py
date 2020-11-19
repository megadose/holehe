<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *

=======
import requests
import random
from holehe.localuseragent import ua

try:
    import cookielib
except BaseException:
    import http.cookiejar as cookielib
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb


def venmo(email):
    s = requests.Session()
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://venmo.com/',
        'Content-Type': 'application/json',
        'Origin': 'https://venmo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    s.get("https://venmo.com/signup/email",headers=headers)
    try:
        headers["device-id"]=s.cookies["v_id"]
    except :
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

    data = '{"last_name":"e","first_name":"z","email":"'+email+'","password":"","phone":"1","client_id":10}'

    response = s.post('https://venmo.com/api/v5/users', headers=headers, data=data)
    if "Not acceptable" not in response.text:
        if "That email is already registered in our system." in response.text:
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
