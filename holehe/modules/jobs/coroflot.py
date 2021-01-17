from holehe.core import *
from holehe.localuseragent import *


async def coroflot(email, client, out):
    name = "coroflot"
    domain = "coroflot.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.coroflot.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.coroflot.com/signup',
        'TE': 'Trailers',
    }

    data = {
        'email': email
    }
    try:
        response = await client.post('https://www.coroflot.com/home/signup_email_check',headers=headers,data=data)
        if response.json()["data"] == -2:
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
    except:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
