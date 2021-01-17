from holehe.core import *
from holehe.localuseragent import *


async def blablacar(email, client, out):
    name = "blablacar"
    domain = "blablacar.com"
    method = "register"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'fr_FR',
        'Referer': 'https://www.blablacar.fr/',
        'Content-Type': 'application/json',
        'x-locale': 'fr_FR',
        'x-currency': 'EUR',
        'x-client': 'SPA|1.0.0',
        'x-forwarded-proto': 'https',
        'Origin': 'https://www.blablacar.fr',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    try:
        appToken = await client.get(
            "https://www.blablacar.fr/register",
            headers=headers)
        appToken = appToken.text.split(',"appToken":"')[1].split('"')[0]

    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    cookies = {
        'datadome': '',
    }
    try:
        headers["Authorization"] = 'Bearer ' + appToken
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    response = await client.get(
        'https://edge.blablacar.fr/auth/validation/email/' +
        email,
        headers=headers,
        cookies=cookies)
    data = response.json()
    if "url" in data.keys():
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif "exists" in data.keys():
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": data["exists"],
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
