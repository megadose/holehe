from holehe.core import *
from holehe.localuseragent import *
import re
import random


async def github(email, client, out):
    name = "github"
    domain = "github.com"
    method = "register"
    frequent_rate_limit = False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    try:
        freq = await client.get("https://github.com/signup", headers=headers)
        if freq.status_code != 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        token_regex = re.compile(
            r'<auto-check src="/signup_check/username[\s\S]*?value="([\S]+)"[\s\S]*<auto-check src="/signup_check/email[\s\S]*?value="([\S]+)"')
        token = re.findall(token_regex, freq.text)

        auth_token = None
        if token and len(token[0]) > 1:
            auth_token = token[0][1]
        else:
            # Fallback to general authenticity_token
            fallback_match = re.search(r'authenticity_token[^>]*value="([^"]+)"', freq.text)
            if fallback_match:
                auth_token = fallback_match.group(1)

        if not auth_token:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        data = {"value": email, "authenticity_token": auth_token}
        req = await client.post("https://github.com/signup_check/email", data=data, headers=headers)

        if "Your browser did something unexpected." in req.text:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif req.status_code == 422:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif req.status_code == 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
