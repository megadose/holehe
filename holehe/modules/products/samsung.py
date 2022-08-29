from holehe.core import *
from holehe.localuseragent import *


async def samsung(email, client, out):
    name = "samsung"
    domain = "samsung.com"
    method = "password recovery"
    frequent_rate_limit=False

    req = await client.get(
        "https://account.samsung.com/accounts/v1/Samsung_com_FR/signUp")
    token = req.text.split("sJSESSIONID")[1].split('"')[1].split('"')[0]

    crsf = req.text.split("{'token' : '")[1].split("'")[0]

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
        'v': random.randrange(1000,9999),
    }

    data = '{"emailID":"' + email + '"}'

    response = await client.post(
        'https://account.samsung.com/accounts/v1/Samsung_com_FR/signUpCheckEmailIDProc',
        headers=headers,
        params=params,
        cookies=cookies,
        data=data)
    data = response.json()
    #print(data)
    if response.status_code == 200:
        if "rtnCd" in data.keys() and "INAPPROPRIATE_CHARACTERS" not in response.text and "accounts aren't supported." not in response.text:
            phone_number = await get_phone_number(email, client, cookies, headers)
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": phone_number,
                        "others": None})
        else:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})


async def get_phone_number(email, client, cookies, headers):
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
    if data['rtnCd'] == 'NEXT':
        req = await client.get('https://account.samsung.com' + data["nextURL"], headers=headers, cookies=cookies)
        found = re.search(phone_number_pattern, req.text)
        if found:
            phone_number = found.group()
        elif 'btnResetPasswordWithRecovery' in req.text:
            response = await client.post("https://account.samsung.com/accounts/v1/DCGLIT/resetPasswordWithRecoveryProc",
                                         headers=headers, params=params, cookies=cookies)
            if response.status_code == 200:
                data = response.json()
                if data['rtnCd'] == 'NEXT':
                    req = await client.get('https://account.samsung.com' + data["nextURL"], headers=headers, cookies=cookies)
                    found = re.search(phone_number_pattern, req.text)
                    if found:
                        phone_number = found.group()

    return phone_number
