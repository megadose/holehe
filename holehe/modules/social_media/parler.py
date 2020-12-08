from holehe.core import *
from holehe.localuseragent import *
from holehe.tools.utils import *


async def parler(email, client, out):

    name = "parler"
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
    data = '{"identifier":' + email + \
        ',"password":"invalidpasswordfortest","deviceId":"' + get_random_string(16) + '"}'
    try:
        r = await client.post(url, data=data, headers=headers)
    except BaseException:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None
    data = r.text
    if 'password' in data:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
