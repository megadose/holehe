from holehe.core import *
from holehe.localuseragent import *


async def bitmoji(email, client, out):
    name = "bitmoji"
    domain = "bitmoji.com"
    method = "login"
    frequent_rate_limit=False

    try:
        req = await client.get("https://accounts.snapchat.com")
        xsrf = req.text.split('data-xsrf="')[1].split('"')[0]
        webClientId = req.text.split('ata-web-client-id="')[1].split('"')[0]
        url = "https://accounts.snapchat.com/accounts/merlin/login"
        headers = {
            "Host": "accounts.snapchat.com",
            "User-Agent": random.choice(ua["browsers"]["firefox"]),
            "Accept": "*/*",
            "X-XSRF-TOKEN": xsrf,
            "Accept-Encoding": "gzip, late",
            "Content-Type": "application/json",
            "Connection": "close",
            "Cookie": "xsrf_token=" + xsrf + "; web_client_id=" + webClientId
        }
        data = '{"email":' + email + ',"app":"BITMOJI_APP"}'

        response = await client.post(url, data=data, headers=headers)
        if response.status_code != 204:
            data = response.json()
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": data["hasBitmoji"],
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return None
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    except:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
