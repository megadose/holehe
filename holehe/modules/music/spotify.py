from holehe.core import *
from holehe.localuseragent import *


async def spotify(email, client, out):
    name = "spotify"
    domain = "spotify.com"
    method= "register"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    params = {
        'validate': '1',
        'email': email,
    }
    try:
        req = await client.get(
            'https://spclient.wg.spotify.com/signup/public/v1/account',
            headers=headers,
            params=params)
        if req.json()["status"] == 1:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        elif req.json()["status"] == 20:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": None,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except :
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": None,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
