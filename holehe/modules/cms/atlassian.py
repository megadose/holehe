from holehe.core import *
from holehe.localuseragent import *


async def atlassian(email, client, out):
    name = "atlassian"
    domain = "atlassian.com"
    method="register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://id.atlassian.com/',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://id.atlassian.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    try:
        r = await client.get("https://id.atlassian.com/login", headers=headers)
        data = {'csrfToken': r.text.split('{&quot;csrfToken&quot;:&quot;')[
            1].split('&quot')[0], 'username': email}
    except :
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    response = await client.post('https://id.atlassian.com/rest/check-username', headers=headers, data=data)
    if response.json()["action"] == "signup":
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
