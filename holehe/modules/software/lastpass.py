from holehe.core import *
from holehe.localuseragent import *


async def lastpass(email, client, out):
    name = "lastpass"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://lastpass.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    params = {
        'check': 'avail',
        'skipcontent': '1',
        'mistype': '1',
        'username': email,
    }

    r = await client.get(
        'https://lastpass.com/create_account.php',
        params=params,
        headers=headers)
    if r.text == "no":
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None
    if r.text == "ok" or r.text == "emailinvalid":
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
