from holehe.core import *
from holehe.localuseragent import *


async def deliveroo(email, client, out):
    name = "deliveroo"

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, application/vnd.api+json',
        'Accept-Language': 'en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Roo-Client': 'orderweb-client',
        'X-Roo-Country': 'fr',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://deliveroo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = {"email_address": email}

    req = await client.post('https://consumer-ow-api.deliveroo.com/orderapp/v1/check-email', headers=headers, json=data)
    if req.status_code == 200:
        data = json.loads(req.text)
        if data["registered"]:
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
    else:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
