from holehe.core import *
from holehe.localuseragent import *


async def crevado(email, client, out):
    name = "crevado"
    domain = "crevado.com"
    method = "register"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://crevado.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }
    try:
        req = await client.get("https://crevado.com")
    except :
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return()
    token = req.text.split(
        '<meta name="csrf-token" content="')[1].split('"')[0]

    data = {
        'utf8': '\u2713',
        'authenticity_token': token,
        'plan': 'basic',
        'account[full_name]': '',
        'account[email]': email,
        'account[password]': '',
        'account[domain]': '',
        'account[confirm_madness]': '',
        'account[terms_accepted]': '0',
        'account[terms_accepted]': '1',
    }

    response = await client.post('https://crevado.com/', headers=headers, data=data)
    try:
        msg_error = response.text.split('showFormErrors({"')[1].split('"')[0]
        if msg_error == "account_email":
            errorEMail = response.text.split(
                'showFormErrors({"account_email":{"error_message":"')[1].split('"')[0]
            if errorEMail == "has already been taken":
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
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
