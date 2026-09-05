from holehe.core import *
from holehe.localuseragent import *
import random
import re


async def samsung(email, client, out):
    name = "samsung"
    domain = "samsung.com"
    method = "password recovery"
    frequent_rate_limit = False

    try:
        req = await client.get(
            "https://account.samsung.com/accounts/v1/Samsung_com_FR/signUp")

        if req.status_code != 200 or "sJSESSIONID" not in req.text or "{'token' : '" not in req.text:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None

        token_parts = req.text.split("sJSESSIONID")
        if len(token_parts) < 2 or len(token_parts[1].split('"')) < 2:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None
        token = token_parts[1].split('"')[1]

        csrf_parts = req.text.split("{'token' : '")
        if len(csrf_parts) < 2 or len(csrf_parts[1].split("'")) < 1:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
            return None
        crsf = csrf_parts[1].split("'")[0]

        cookies = {
            'EUAWSIAMSESSIONID': token,
        }

        headers = {
            'User-Agent': random.choice(ua["browsers"]["firefox"]),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en,en-US;q=0.5',
            'Referer': 'https://account.samsung.com/accounts/v1/Samsung_com_FR/signUp',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRF-TOKEN': crsf,
            'Origin': 'https://account.samsung.com',
            'DNT': '1',
            'Connection': 'keep-alive',
        }

        params = {
            'v': random.randrange(1000, 9999),
        }

        data = '{"emailID":"' + email + '"}'

        response = await client.post(
            'https://account.samsung.com/accounts/v1/Samsung_com_FR/signUpCheckEmailIDProc',
            headers=headers,
            params=params,
            cookies=cookies,
            data=data)

        if response.status_code == 200:
            try:
                resp_json = response.json()
            except Exception:
                resp_json = {}

            if "rtnCd" in resp_json and "INAPPROPRIATE_CHARACTERS" not in response.text and "accounts aren't supported." not in response.text:
                phone_number = await get_phone_number(email, client, cookies, headers)
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": phone_number, "others": None})
            else:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except Exception:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})


async def get_phone_number(email, client, cookies, headers):
    try:
        phone_number_pattern = re.compile(r'(\d{4}[*]{2}\d{2}[*]{2}\d{2})')

        headers['Referer'] = 'https://account.samsung.com/accounts/v1/DCGLIT/resetPassword'
        params = {'v': random.randrange(int(1.5E12), int(2E12))}
        data = {"signUpID": email, "signUpIDType": "003"}

        response = await client.post(
            'https://account.samsung.com/accounts/v1/DCGLIT/resetPasswordProc',
            headers=headers,
            params=params,
            cookies=cookies,
            json=data)
        data = response.json()

        phone_number = None
        if data.get('rtnCd') == 'NEXT' and "nextURL" in data:
            req = await client.get('https://account.samsung.com' + data["nextURL"], headers=headers, cookies=cookies)
            found = re.search(phone_number_pattern, req.text)
            if found:
                phone_number = found.group()
            elif 'btnResetPasswordWithRecovery' in req.text:
                response = await client.post("https://account.samsung.com/accounts/v1/DCGLIT/resetPasswordWithRecoveryProc",
                                             headers=headers, params=params, cookies=cookies)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('rtnCd') == 'NEXT' and "nextURL" in data:
                        req = await client.get('https://account.samsung.com' + data["nextURL"], headers=headers, cookies=cookies)
                        found = re.search(phone_number_pattern, req.text)
                        if found:
                            phone_number = found.group()

        return phone_number
    except Exception:
        return None
