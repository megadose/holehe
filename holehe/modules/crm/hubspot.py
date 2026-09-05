from holehe.core import *
from holehe.localuseragent import *


async def hubspot(email, client, out):
    name = "hubspot"
    domain = "hubspot.com"
    method= "login"
    frequent_rate_limit=False


    headers = {
        'authority': 'api.hubspot.com',
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'content-type': 'application/json',
        'origin': 'https://app.hubspot.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://app.hubspot.com/',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
    }

    data = '{"email":"'+email+'","password":"","rememberLogin":false}'

    response = await client.post('https://api.hubspot.com/login-api/v1/login', headers=headers, data=data)
    if response.status_code == 400:
        if response.json()["status"]=="INVALID_PASSWORD":
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        elif response.json()["status"]=="INVALID_USER":
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        return()
    out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                "rateLimit": True,
                "exists": False,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None})
    return()
