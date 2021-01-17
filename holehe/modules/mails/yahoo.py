from holehe.core import *
from holehe.localuseragent import *


async def yahoo(email, client, out):
    name = "yahoo"
    domain = "yahoo.com"
    method= "login"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://login.yahoo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    req = await client.get("https://login.yahoo.com", headers=headers)

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'bucket': 'mbr-fe-merge-manage-account',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://login.yahoo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    params = {
        '.src': 'fpctx',
        '.intl': 'ca',
        '.lang': 'en-CA',
        '.done': 'https://ca.yahoo.com',
    }
    try:
        data = {
            'acrumb': req.text.split('<input type="hidden" name="acrumb" value="')[1].split('"')[0],
            'sessionIndex': req.text.split('<input type="hidden" name="sessionIndex" value="')[1].split('"')[0],
            'username': email,
            'passwd': '',
            'signin': 'Next',
            'persistent': 'y'}

        response = await client.post(
            'https://login.yahoo.com/',
            headers=headers,
            params=params,
            data=data)
        response = response.json()
        if "error" in response.keys():
            if not response["error"]:
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": False,
                            "exists": True,
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
        elif "render" in response.keys():
            if response["render"]["error"] == "messages.ERROR_INVALID_USERNAME":
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
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
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
