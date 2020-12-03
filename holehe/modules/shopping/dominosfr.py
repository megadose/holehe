from holehe.core import *
from holehe.localuseragent import *


async def dominosfr(email, client, out):
    name = "dominosfr"

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://commande.dominos.fr/eStore/fr/Signup',
    }

    await client.get("https://commande.dominos.fr/eStore/fr/Signup", headers=headers)
    headers['X-Requested-With'] = 'XMLHttpRequest'

    data = {"email": email}

    req = await client.get('https://commande.dominos.fr/eStore/fr/Signup/IsEmailAvailable', headers=headers, params=data)
    if req.status_code == 200:
        if req.text == "false":
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
