from holehe.core import *
from holehe.localuseragent import *


async def freelancer(email, client, out):
    name = "freelancer"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/json',
        'Origin': 'https://www.freelancer.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"user":{"email":"' + email + '"}}'
    response = await client.post('https://www.freelancer.com/api/users/0.1/users/check?compact=true&new_errors=true', data=data, headers=headers)
    resData = response.json()
    if response.status_code == 409 and "EMAIL_ALREADY_IN_USE" in response.text:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})

    elif response.status_code == 200:
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
