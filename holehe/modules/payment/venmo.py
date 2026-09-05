from holehe.core import *
from holehe.localuseragent import *
import random
import httpx


async def venmo(email, client, out):
    name = "venmo"
    domain = "venmo.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://venmo.com/',
        'Content-Type': 'application/json',
        'Origin': 'https://venmo.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    try:
        req = await client.get("https://venmo.com/signup/email", headers=headers)
        if req.status_code != 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        device_id = client.cookies.get("v_id", "")
        if device_id:
            headers["device-id"] = device_id

        data = '{"last_name":"e","first_name":"z","email":"' + \
            email + '","password":"","phone":"1","client_id":10}'

        response = await client.post('https://venmo.com/api/v5/users', headers=headers, data=data)
        if "Not acceptable" not in response.text:
            if "That email is already registered in our system." in response.text:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
            else:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except (httpx.RequestError, Exception):
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
