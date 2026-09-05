from holehe.core import *
from holehe.localuseragent import *
from bs4 import BeautifulSoup
import string
import random


async def buymeacoffee(email, client, out):
    name = "buymeacoffee"
    domain = "buymeacoffee.com"
    method = "register"
    frequent_rate_limit = True

    def get_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.buymeacoffee.com',
        'DNT': '1',
        'TE': 'Trailers',
    }

    try:
        r = await client.get("https://www.buymeacoffee.com/", headers=headers)
        if r.status_code != 200:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        soup = BeautifulSoup(r.content, features="html.parser")
        csrf_elem = soup.find(attrs={'name': 'bmc_csrf_token'}) or soup.find('input', {'name': '_token'})
        csrf_token = csrf_elem.get("value") if csrf_elem else None

        if not csrf_token:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        cookies = {
            'bmccsrftoken': csrf_token,
        }
        data = {
            'email': email,
            'password': get_random_string(20),
            'bmc_csrf_token': csrf_token
        }

        r = await client.post(
            'https://www.buymeacoffee.com/auth/validate_email_and_password',
            headers=headers,
            cookies=cookies,
            data=data)

        if r.status_code == 200:
            try:
                data_json = r.json()
            except Exception:
                data_json = {}

            if data_json.get("status") == "SUCCESS":
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            elif data_json.get("status") == "FAIL" and "email" in str(data_json):
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
            else:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
