from holehe.core import *
from holehe.localuseragent import *


async def insightly(email, client, out):
    name = "insightly"
    domain = "insightly.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'authority': 'accounts.insightly.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://accounts.insightly.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://accounts.insightly.com/?plan=trial',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
    }

    data = {
      'emailaddress': email
    }

    response = await client.post('https://accounts.insightly.com/signup/isemailvalid', headers=headers, data=data)

    if "An account exists for this address. Use another address or" in response.text:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return()
    elif response.text == "true":
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
