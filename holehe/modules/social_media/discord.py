from holehe.core import *
from holehe.localuseragent import *
from holehe.tools.utils import *

async def discord(email, client, out):

    name = "discord"

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"fingerprint":"","email":"' + str(email) + '","username":"' + get_random_string(20) + '","password":"' + get_random_string(
        20) + '","invite":null,"consent":true,"date_of_birth":"","gift_code_sku_id":null,"captcha_key":null}'

    r = await client.post(
        'https://discord.com/api/v8/auth/register',
        headers=headers,
        data=data)
    rData = r.json()
    try:
        if "code" in rData.keys():
            try:
                if rData["errors"]["email"]["_errors"][0]['code'] == "EMAIL_ALREADY_REGISTERED":
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
            except BaseException:
                out.append({"name": name,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        elif rData["captcha_key"][0] == "captcha-required":
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
    except BaseException:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
