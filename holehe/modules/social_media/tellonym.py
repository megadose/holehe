from holehe.core import *
from holehe.localuseragent import *


async def tellonym(email, client, out):
    name = "tellonym"
    domain = "tellonym.me"
    method = "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'tellonym-client': 'web:0.51.1',
        'content-type': 'application/json;charset=utf-8',
        'Origin': 'https://tellonym.me',
        'Connection': 'keep-alive',
        'Referer': 'https://tellonym.me/register/email',
        'TE': 'Trailers',
    }

    params = {
        'email': str(email),
        'errorMessage': '',
        'limit': '25',
    }

    try:
        response = await client.get('https://api.tellonym.me/accounts/check', headers=headers, params=params)
        if "EMAIL_ALREADY_IN_USE" in response.text:
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
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
