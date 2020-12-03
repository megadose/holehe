from holehe.core import *
from holehe.localuseragent import *


def parler(email):
    url = "https://api.parler.com/v2/login/new"
    headers = {
        'authority': 'api.parler.com',
        'accept': 'application/json, text/plain, */*',
        'dnt': '1',
        'user-agent': random.choice(ua["browsers"]["chrome"]),
        'content-type': 'application/json',
        'origin': 'https://parler.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://parler.com/',
        'accept-language': 'es,en-US;q=0.9,en;q=0.8',
        'sec-gpc': '1',
    }
    email = '"' + email + '"'
    data = '{"identifier":' + email + ',"password":"invalidpasswordfortest","deviceId":"uCs4pEF696JLGwzm"}'
    response = requests.post(url, data=data, headers=headers)
    data = response.text
    if 'password' in data:
        return ({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return ({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
