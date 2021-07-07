from holehe.core import *
from holehe.localuseragent import *


async def teamleader(email, client, out):
    name = "teamleader"
    domain = "teamleader.eu"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'authority': 'focus.teamleader.eu',
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://signup.focus.teamleader.fr',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://signup.focus.teamleader.fr/',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
    }

    data = '{"email":"'+email+'"}'

    response = await client.post('https://focus.teamleader.eu/app/emails/availability', headers=headers, data=data)
    if response.text=='{"available":false}':
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif response.text=='{"available":true}':
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})

    return()
