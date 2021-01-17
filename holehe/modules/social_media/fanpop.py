from holehe.core import *
from holehe.localuseragent import *


async def fanpop(email, client, out):
    name = "fanpop"
    domain = "fanpop.com"
    method = "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'text/html, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.fanpop.com',
        'Connection': 'keep-alive',
        'Referer': 'https://www.fanpop.com/register',
    }

    data = {
        'type': 'register',
        'user[name]': '',
        'user[password]': '',
        'user[email]': email,
        'agreement': '',
        'PersistentCookie': 'PersistentCookie',
        'redirect_url': 'https://www.fanpop.com/',
        'submissiontype': 'register'
    }

    response = await client.post('https://www.fanpop.com/login/superlogin', headers=headers, data=data)

    if "already registered" in response.text:
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
