<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *
=======
import requests
import random

from holehe import *

>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb

def discord(email):
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return(result_str)

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"fingerprint":"","email":"' + email + '","username":"' + get_random_string(20) + '","password":"' + get_random_string(
        20) + '","invite":null,"consent":true,"date_of_birth":"","gift_code_sku_id":null,"captcha_key":null}'

    response = requests.post(
        'https://discord.com/api/v8/auth/register',
        headers=headers,
        data=data)
    responseData = response.json()
    try:
        if "code" in responseData.keys():
            try:
                if responseData["errors"]["email"]["_errors"][0]['code'] == "EMAIL_ALREADY_REGISTERED":
                    return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
                else:
                    return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            except BaseException:
                return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif responseData["captcha_key"][0] == "captcha-required":
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
