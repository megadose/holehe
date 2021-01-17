from holehe.core import *
from holehe.localuseragent import *


async def patreon(email, client, out):
    name = "patreon"
    domain = "patreon.com"
    method = "login"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.patreon.com/signup?ru=%2Fcreate%3Fru%3D%252Feurope',
        'Content-Type': 'application/vnd.api+json',
        'Origin': 'https://www.patreon.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    params = {
        'json-api-version': '1.0',
        'include': '[]',
    }

    data = '{"data":{"attributes":{"email":"'+email+'"},"relationships":{}}}'
    try:
        response = await client.post('https://www.patreon.com/api/email/available', headers=headers, params=params, data=data)
        if response.json()["data"]["is_available"] == True :
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except :
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
