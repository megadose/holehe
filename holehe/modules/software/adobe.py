from holehe.core import *
from holehe.localuseragent import *


async def adobe(email, client, out):
    name = "adobe"
    domain = "adobe.com"
    method = "password recovery"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-IMS-CLIENTID': 'adobedotcom2',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://auth.services.adobe.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    data = '{"username":"' + email + '","accountType":"individual"}'
    try:
        r = await client.post(
            'https://auth.services.adobe.com/signin/v1/authenticationstate',
            headers=headers,
            data=data)
        r = r.json()
        if "errorCode" in str(r.keys()):
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return None
        headers['X-IMS-Authentication-State'] = r['id']
        params = {
            'purpose': 'passwordRecovery',
        }
        response = await client.get(
            'https://auth.services.adobe.com/signin/v2/challenges',
            headers=headers,
            params=params)
        response=response.json()
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": response['secondaryEmail'],
                    "phoneNumber": response['securityPhoneNumber'],
                    "others": None})
    except:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
