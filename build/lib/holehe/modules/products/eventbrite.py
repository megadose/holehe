from holehe.core import *
from holehe.localuseragent import *


async def eventbrite(email, client, out):
    name = "eventbrite"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.eventbrite.com/',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.eventbrite.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    req = await client.get("https://www.eventbrite.com/signin/?referrer=%2F", headers=headers)
    try:
        csrf_token = req.cookies["csrftoken"]

    except BaseException:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    cookies = {
        'csrftoken': csrf_token,
    }

    headers["X-CSRFToken"] = csrf_token
    data = '{"email":"' + email + '"}'

    response = await client.post(
        'https://www.eventbrite.com/api/v3/users/lookup/',
        headers=headers,
        cookies=cookies,
        data=data)
    if response.status_code == 200:
        try:
            reqd = response.json()
            if reqd["exists"]:
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
    else:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
