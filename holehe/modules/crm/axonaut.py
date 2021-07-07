from holehe.core import *
from holehe.localuseragent import *


async def axonaut(email, client, out):
    name = "axonaut"
    domain = "axonaut.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'authority': 'axonaut.com',
        'upgrade-insecure-requests': '1',
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://axonaut.com/en',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
    }


    response = await client.get('https://axonaut.com/onboarding/?email='+email, headers=headers,allow_redirects=False)

    if response.status_code == 302 and "/login?email" in str(response.headers['Location']):
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif response.status_code ==200:
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
