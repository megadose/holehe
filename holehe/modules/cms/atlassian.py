from holehe.core import *
from holehe.localuseragent import *

async def atlassian(email, client, out):
    name = "atlassian"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Origin': 'https://id.atlassian.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    r = await client.get("https://id.atlassian.com/login", headers=headers)
    try:
        token = r.text.split('{&quot;csrfToken&quot;:&quot;')[1].split('&quot')[0]
        data = {'csrfToken': token,
                'username': email
                }
    except IndexError:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return

    r = await client.post('https://id.atlassian.com/rest/check-username',
                headers=headers, data=data)
    try:
        if r.json()["action"] == "signup":
            out.append({"name": name,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except AttributeError:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
