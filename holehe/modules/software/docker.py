from holehe.core import *
from holehe.localuseragent import *

async def docker(email, client, out):
    name="docker"
    domain = "docker.com"
    method = "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://hub.docker.com/signup',
        'Content-Type': 'application/json',
        'X-CSRFToken': '',
        'Origin': 'https://hub.docker.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    data = '{"email":"'+email+'","password":"","recaptcha_response":"","redirect_value":"","subscribe":true,"username":""}'

    response = await client.post('https://hub.docker.com/v2/users/signup/', headers=headers, data=data)
    if "This email is already in use." in response.text:
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
