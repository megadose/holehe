from holehe.core import *
from holehe.localuseragent import *
import random
import re


async def evernote(email, client, out):
    name = "evernote"
    domain = "evernote.com"
    method = "login"
    frequent_rate_limit = False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.evernote.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.evernote.com/Login.action',
        'TE': 'Trailers',
    }

    try:
        data = await client.get("https://www.evernote.com/Login.action", headers=headers)
        if data.status_code != 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        # Defensively extract tokens
        hpts_match = re.search(r'document\.getElementById\("hpts"\)\.value\s*=\s*"([^"]+)"', data.text)
        hptsh_match = re.search(r'document\.getElementById\("hptsh"\)\.value\s*=\s*"([^"]+)"', data.text)
        source_match = re.search(r'<input\s+type="hidden"\s+name="_sourcePage"\s+value="([^"]+)"', data.text)
        fp_match = re.search(r'<input\s+type="hidden"\s+name="__fp"\s+value="([^"]+)"', data.text)

        if not (hpts_match and hptsh_match and source_match and fp_match):
            # Page layout updated / redirected to accounts.evernote.com SPA
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        data2 = {
            'username': email,
            'evaluateUsername': '',
            'hpts': hpts_match.group(1),
            'hptsh': hptsh_match.group(1),
            'analyticsLoginOrigin': 'login_action',
            'clipperFlow': 'false',
            'showSwitchService': 'true',
            'usernameImmutable': 'false',
            '_sourcePage': source_match.group(1),
            '__fp': fp_match.group(1)
        }
        response = await client.post('https://www.evernote.com/Login.action', data=data2, headers=headers)
        if "usePasswordAuth" in response.text:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif "displayMessage" in response.text:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
