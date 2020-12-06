from holehe.core import *
from holehe.localuseragent import *


async def codeacademy(email, client, out):
    name = "codeacademy"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://www.codecademy.com/register?redirect=%2',
        'Content-Type': 'application/json',
        'Origin': 'https://www.codecademy.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    req = await client.get(
        "https://www.codecademy.com/register?redirect=%2F",
        headers=headers)
    soup = BeautifulSoup(req.content, features="html.parser")
    try:
        headers["X-CSRF-Token"] = soup.find(
            attrs={"name": "csrf-token"}).get("content")
    except BaseException:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    data = '{"user":{"email":"' + email + '"}}'

    response = await client.post(
        'https://www.codecademy.com/register/validate',
        headers=headers,
        data=data)
    if 'is already taken' in response.text:
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
