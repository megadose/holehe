from holehe.core import *
from holehe.localuseragent import *


async def sporcle(email, client, out):
    name = "sporcle"
    domain = "sporcle.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.sporcle.com',
        'Connection': 'keep-alive',
    }

    data = {
        'email': str(email),
        'password1': '',
        'password2': '',
        'handle': '',
        'humancheck': '',
        'reg_path': 'main_header_join',
        'ref_page': '',
        'querystring': ''
    }

    response = await client.post('https://www.sporcle.com/auth/ajax/verify.php', headers=headers, data=data)
    if "account already exists with this email" in response.text:
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
