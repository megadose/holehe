from holehe.core import *
from holehe.localuseragent import *


def samsung(email):
    req = requests.get(
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

    params = (
        ('v', '1337'),
    )

    data = '{"emailID":"' + email + '"}'

    response = requests.post(
        'https://account.samsung.com/accounts/v1/Samsung_com_FR/signUpCheckEmailIDProc',
        headers=headers,
        params=params,
        cookies=cookies,
        data=data)
    data = response.json()
    if response.status_code == 200:
        if "rtnCd" in data.keys():
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
