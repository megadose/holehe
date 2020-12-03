from holehe.core import *
from holehe.localuseragent import *


async def ebay(email, client, out):
    name = "ebay"

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.ebay.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }
    try:
        req = await client.get(
            "https://www.ebay.com/signin/", headers=headers)
        srt = req.text.split('"csrfAjaxToken":"')[1].split('"')[0]
    except IndexError:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    data = {
        'identifier': email,
        'srt': srt
    }

    req = await client.post(
        'https://signin.ebay.com/signin/srv/identifer',
        data=data, headers=headers)
    results = json.loads(req.text)
    if "err" in results.keys():
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
