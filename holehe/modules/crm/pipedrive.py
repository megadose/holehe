from holehe.core import *
from holehe.localuseragent import *


async def pipedrive(email, client, out):
    name = "pipedrive"
    domain = "pipedrive.com"
    method= "register"
    frequent_rate_limit=False


    headers = {
        'authority': 'app.pipedrive.com',
        'accept': 'application/json',
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'content-type': 'application/json',
        'origin': 'https://www.pipedrive.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.pipedrive.com/',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
    }
    data = '{"email":"'+email+'","language":"fr","country_code":"fr","selectedTier":null,"packages":[]}'

    response = await client.post('https://app.pipedrive.com/signup-service/start', headers=headers, data=data)
    if response.status_code==200:
        if "errors" in response.json().keys() and "user_email" in response.json()["errors"].keys() and  "Email is not available" in response.json()["errors"]["user_email"]:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return()
        elif "data" in response.json().keys() and "redirectUrl" in response.json()["data"].keys() and response.json()["data"]["redirectUrl"] == "https://app.pipedrive.com/signup-service":
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
