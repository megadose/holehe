from holehe.core import *
from holehe.localuseragent import *


async def blip(email, client, out):
    name = "blip"
    domain = "blip.fm"
    method= "register"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept-Language': 'en,en-US;q=0.5',
        'Origin': 'https://blip.fm',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://blip.fm/',
    }

    data = {
        'referringUrl': '',
        'genpass': '1',
        'signup[urlName]': 'test',
        'signup[emailAddress]': email,
        'g-recaptcha-response': '',
        'tos': '0'
    }
    try:
        response = await client.post('https://blip.fm/signup/save', headers=headers, data=data)
        if 'That email address is already in use.' in response.text:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        elif 'cloudfront.net/images/blip/spinner.gif" alt="loading..."' in response.text:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
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
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
