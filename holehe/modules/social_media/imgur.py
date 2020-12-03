from holehe.core import *
from holehe.localuseragent import *


async def imgur(email, client, out):
    name = "imgur"

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://imgur.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    r = await client.get("https://imgur.com/register?redirect=%2Fuser", headers=headers)

    headers["X-Requested-With"] = "XMLHttpRequest"

    data = {
        'email': email
    }

    response = await client.post('https://imgur.com/signin/ajax_email_available', headers=headers, data=data)
    if response.status_code == 200:
        if response.json()["data"]["available"]:
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
    else:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
