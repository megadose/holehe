from holehe.core import *
from holehe.localuseragent import *


async def google(email, client, out):
    name = "google"
    domain = "google.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'X-Same-Domain': '1',
        'Google-Accounts-XSRF': '1',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Origin': 'https://accounts.google.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Faccounts.google.com%2F&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp',
        'TE': 'Trailers',
    }

    req = await client.get(
        "https://accounts.google.com/signup/v2/webcreateaccount?continue=https%3A%2F%2Faccounts.google.com%2FManageAccount%3Fnc%3D1&gmb=exp&biz=false&flowName=GlifWebSignIn&flowEntry=SignUp",
        headers=headers)
    try:
        freq = req.text.split('quot;,null,null,null,&quot;')[
            1].split('&quot')[0]
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    params = {
        'hl': 'fr',
        'rt': 'j',
    }

    data = {
        'continue': 'https://accounts.google.com/',
        'dsh': '',
        'hl': 'fr',
        'f.req': '["' + freq + '","","","' + email + '",false]',
        'azt': '',
        'cookiesDisabled': 'false',
        'deviceinfo': '[null,null,null,[],null,"FR",null,null,[],"GlifWebSignIn",null,[null,null,[],null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,[],null,null,null,[],[]],null,null,null,null,0,null,false]',
        'gmscoreversion': 'unined',
        '': ''

    }
    response = await client.post('https://accounts.google.com/_/signup/webusernameavailability', headers=headers, params=params, data=data)
    if '"gf.wuar",2' in response.text:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif '"gf.wuar",1' in response.text or "EmailInvalid" in response.text:
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
