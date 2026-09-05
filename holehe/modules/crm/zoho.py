from holehe.core import *
from holehe.localuseragent import *


async def zoho(email, client, out):
    name = "zoho"
    domain = "zoho.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://accounts.zoho.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'en-US;q=0.8,en;q=0.7',
    }

    response = await client.get("https://accounts.zoho.com/register", headers=headers)
    headers['X-ZCSRF-TOKEN']='iamcsrcoo='+response.cookies["iamcsr"]

    data = {
      'mode': 'primary',
      'servicename': 'ZohoCRM',
      'serviceurl': 'https://crm.zoho.com/crm/ShowHomePage.do',
      'service_language': 'fr'
    }

    response = await client.post('https://accounts.zoho.com/signin/v2/lookup/'+email, headers=headers, data=data)
    if response.status_code==200 and "message" in response.json().keys() and response.json()["message"]=="User exists" and response.json()["status_code"]==201:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif response.status_code==200 and "message" in response.json().keys() and response.json()["status_code"]==400:
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
