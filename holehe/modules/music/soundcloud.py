from holehe.core import *
from holehe.localuseragent import *
from bs4 import BeautifulSoup
import random
import re
import json


async def soundcloud(email, client, out):
    name = "soundcloud"
    domain = "soundcloud.com"
    method = "register"
    frequent_rate_limit = False

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': random.choice(ua["browsers"]["chrome"])
    }

    try:
        getAuth = await client.get('https://soundcloud.com/octobersveryown', headers=headers)
        if getAuth.status_code != 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        soup = BeautifulSoup(getAuth.text, 'html.parser')
        clientId = None

        # Search inline scripts
        for script in soup.find_all('script'):
            txt = script.text or (script.contents[0] if script.contents else "")
            if "runtimeConfig" in txt:
                try:
                    data = json.loads(txt)
                    clientId = data.get("runtimeConfig", {}).get("clientId")
                    if clientId:
                        break
                except Exception:
                    pass
            m = re.search(r'client_id[:=]\s*["\']([a-zA-Z0-9]{32})["\']', str(txt))
            if m:
                clientId = m.group(1)
                break

        # Search external scripts if still not found
        if not clientId:
            external_scripts = [s.get('src') for s in soup.find_all('script') if s.get('src') and 'sndcdn.com' in s.get('src')]
            for src in external_scripts[:3]:
                try:
                    js_resp = await client.get(src, headers=headers)
                    m = re.search(r'client_id[:=]\s*["\']([a-zA-Z0-9]{32})["\']', js_resp.text)
                    if m:
                        clientId = m.group(1)
                        break
                except Exception:
                    continue

        if not clientId:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        linkMail = email.replace('@', '%40')
        API = await client.get(f'https://api-auth.soundcloud.com/web-auth/identifier?q={linkMail}&client_id={clientId}', headers=headers)

        if API.status_code == 200:
            try:
                Json = API.json()
            except Exception:
                Json = {}

            status = Json.get('status')
            if status in ('available', 'in_use'):
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False,
                            "exists": (status == 'in_use'),
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
            else:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
