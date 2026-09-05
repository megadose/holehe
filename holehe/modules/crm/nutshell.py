from holehe.core import *
from holehe.localuseragent import *


async def nutshell(email, client, out):
    name = "nutshell"
    domain = "nutshell.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'authority': 'app.nutshell.com',
        'accept': '*/*',
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://app.nutshell.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://app.nutshell.com/auth',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
    }

    data = {
      'via': 'database',
      'timezone_offset': '1',
      'remember_me': 'true',
      'username': email,
      'invalidToken': 'false',
      'password': 'a'
    }

    response = await client.post('https://app.nutshell.com/auth', headers=headers, data=data)

    if "Sorry, your password is incorrect" in response.text:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif "find a Nutshell account for that email address." in response.text:
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
