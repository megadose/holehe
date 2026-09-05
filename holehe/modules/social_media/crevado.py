from holehe.core import *
from holehe.localuseragent import *
from bs4 import BeautifulSoup
import random


async def crevado(email, client, out):
    name = "crevado"
    domain = "crevado.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://crevado.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    try:
        req = await client.get("https://crevado.com", headers=headers)
        if req.status_code != 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        soup = BeautifulSoup(req.text, 'html.parser')
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        token = csrf_meta.get('content') if csrf_meta else None

        if not token:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        data = {
            'utf8': '\u2713',
            'authenticity_token': token,
            'plan': 'basic',
            'account[full_name]': '',
            'account[email]': email,
            'account[password]': '',
            'account[domain]': '',
            'account[confirm_madness]': '',
            'account[terms_accepted]': '0',
            'account[terms_accepted]': '1',
        }

        response = await client.post('https://crevado.com/', headers=headers, data=data)

        if "has already been taken" in response.text:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        elif "showFormErrors" in response.text or response.status_code == 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
