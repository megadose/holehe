from holehe.core import *
from holehe.localuseragent import *


async def nocrm(email, client, out):
    name = "nocrm"
    domain = "nocrm.io"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'authority': 'register.nocrm.io',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'x-requested-with': 'XMLHttpRequest',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://register.nocrm.io/?lang=en&cc=FR&edition=dreamteam&site_version=v3-video-sun-fr&first_seen_from=https%3A%2F%2Fyoudontneedacrm.com%2Ffr&first_seen_on=%2Ffr&fp_tracking=',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
    }


    response = await client.get('https://register.nocrm.io/register/check_trial_duplicate?email='+email, headers=headers)
    if '{"account":1,"url":"' in response.text:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif response.text == '{"account":0}':
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
