from holehe.core import *
from holehe.localuseragent import *


async def myspace(email, client, out):
    name = "myspace"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Origin': 'https://myspace.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://myspace.com/signup/email',
    }

    r = await client.get("https://myspace.com/signup/email", headers=headers, timeout=3)

    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    try:
        headers['Hash'] = r.text.split('<input name="csrf" type="hidden" value="')[
            1].split('"')[0]
    except BaseException:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    headers['X-Requested-With'] = 'XMLHttpRequest'

    data = {
        'email': email
    }

    response = await client.post('https://myspace.com/ajax/account/validateemail', headers=headers, data=data, timeout=3)
    try:
        if "This email address was already used to create an account." in response.text:
            out.append({"name": name,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except BaseException:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
