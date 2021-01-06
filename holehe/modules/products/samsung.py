from holehe.core import *
from holehe.localuseragent import *


async def samsung(email, client, out):
    name = "samsung"
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
        if "rtnCd" in data.keys() and "INAPPROPRIATE_CHARACTERS" not in response.text:
            out.append({"name": name,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    else:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
