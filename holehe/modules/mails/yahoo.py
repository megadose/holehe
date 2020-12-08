from holehe.core import *
from holehe.localuseragent import *


async def yahoo(email, client, out):
    name = "yahoo"
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

        r = await client.post(
            'https://login.yahoo.com/',
            headers=headers,
            params=params,
            data=data)
        r = r.json()
        if "error" in r.keys():
            if not r["error"]:
                out.append({"name": name,
                            "rateLimit": False,
                            "exists": True,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
            else:
                out.append({"name": name,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        elif "render" in r.keys():
            if r["render"]["error"] == "messages.ERROR_INVALID_USERNAME":
                out.append({"name": name,
                            "rateLimit": False,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
            else:
                out.append({"name": name,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        else:
            out.append({"name": name,
                        "rateLimit": True,
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
