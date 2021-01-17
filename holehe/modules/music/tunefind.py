from holehe.core import *
from holehe.localuseragent import *


async def tunefind(email, client, out):
    name = "tunefind"
    domain = "tunefind.com"
    method= "register"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Referer': 'https://www.tunefind.com/',
        'x-tf-react': 'true',
        'Origin': 'https://www.tunefind.com',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=---------------------------'
    }
    r = await client.get("https://www.tunefind.com/user/join", headers=headers)
    try:
        crsf_token = r.text.split('"csrf-token" content="')[1].split('"')[0]
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None
    data = '$-----------------------------\r\nContent-Disposition: form-data; name="username"\r\n\r\n\r\n-----------------------------\r\nContent-Disposition: form-data; name="email"\r\n\r\n' + \
        str(email) + '\r\n-----------------------------\r\nContent-Disposition: form-data; name="password"\r\n\r\n\r\n-------------------------------\r\n'
    response = await client.post('https://www.tunefind.com/user/join', headers=headers, data=data)
    if "email" in response.json()["errors"].keys():
        if "Someone is already registered with that email address" in str(
                response.json()["errors"]["email"]):
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
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
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
