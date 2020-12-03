from holehe.core import *
from holehe.localuseragent import *


async def envato(email, client, out):
    name = "envato"

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
    req = await client.post(
        'https://account.envato.com/api/validate_email',
        headers=headers,
        data=data)
    if 'Email is already in use' in req.text:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif "Page designed by Kotulsky" in req.text:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
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
