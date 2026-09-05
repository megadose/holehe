from holehe.core import *
from holehe.localuseragent import *
import random
import json


async def snapchat(email, client, out):
    name = "snapchat"
    domain = "snapchat.com"
    method = "login"
    frequent_rate_limit = False

    try:
        req = await client.get("https://accounts.snapchat.com")

        if req.status_code != 200 or 'data-xsrf="' not in req.text or 'ata-web-client-id="' not in req.text:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        xsrf_parts = req.text.split('data-xsrf="')
        webclient_parts = req.text.split('ata-web-client-id="')

        if len(xsrf_parts) < 2 or len(webclient_parts) < 2:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        xsrf = xsrf_parts[1].split('"')[0]
        webClientId = webclient_parts[1].split('"')[0]

        url = "https://accounts.snapchat.com/accounts/merlin/login"
        headers = {
            "Host": "accounts.snapchat.com",
            "User-Agent": random.choice(ua["browsers"]["firefox"]),
            "Accept": "*/*",
            "X-XSRF-TOKEN": xsrf,
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "Connection": "close",
            "Cookie": "xsrf_token=" + xsrf + "; web_client_id=" + webClientId
        }
        data = json.dumps({"email": email, "app": "BITMOJI_APP"})

        response = await client.post(url, data=data, headers=headers)

        if response.status_code != 204:
            try:
                data_json = response.json()
                has_snapchat = data_json.get("hasSnapchat", False)
            except Exception:
                has_snapchat = False

            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": has_snapchat, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
