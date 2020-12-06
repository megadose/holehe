from holehe.core import *
from holehe.localuseragent import *


async def vivino(email, client, out):
    name = "vivino"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Referer': 'https://www.vivino.com/',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    r = await client.get("https://www.tunefind.com/user/join", headers=headers)
    try:
        crsf_token = r.text.split('"csrf-token" content="')[1].split('"')[0]
    except BaseException:
        out.append({"rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    headers['X-CRSF-Token'] = crsf_token
    data = '{"email":"' + str(email) + '","password":"e"}'

    response = await client.post('https://www.vivino.com/api/login', headers=headers, data=data)
    if response.status_code == 429:
        out.append({"rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        if response.json()['error'] == "The supplied email does not exist":
            out.append({"name": name,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
