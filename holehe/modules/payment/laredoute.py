from holehe.core import *
from holehe.localuseragent import *


async def laredoute(email, client, out):
    name = "laredoute"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.laredoute.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-GPC': '1',
        'TE': 'Trailers',
    }

    data = {
        'email': email
    }
    try:
        req = await client.post(
            'https://www.laredoute.com/CustomerServices/VerifyEmailRegistration',
            headers=headers,
            data=data)
    except :
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return(None)

    if 'This email address already has an account.' in req.text:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif "Please enable JS and disable any ad blocker" in req.text:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
