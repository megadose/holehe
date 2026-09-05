from holehe.core import *
from holehe.localuseragent import *


async def bodybuilding(email, client, out):
    name = "bodybuilding"
    domain = "bodybuilding.com"
    method = "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Origin': 'https://www.bodybuilding.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.bodybuilding.com/',
    }

    response = await client.head('https://api.bodybuilding.com/profile/email/' + email, headers=headers)
    if response.status_code == 200:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
