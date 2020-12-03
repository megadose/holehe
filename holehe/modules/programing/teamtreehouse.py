from holehe.core import *
from holehe.localuseragent import *


async def teamtreehouse(email, client, out):
    name = "teamtreehouse"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://teamtreehouse.com/subscribe/new?trial=yes',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://teamtreehouse.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    req = await client.get(
        "https://teamtreehouse.com/subscribe/new?trial=yes",
        headers=headers)
    soup = BeautifulSoup(req.content, features="html.parser")
    token = soup.find(attrs={"name": "csrf-token"}).get("content")
    headers['X-CSRF-Token'] = token

    data = {
        'email': email
    }

    response = await client.post(
        'https://teamtreehouse.com/account/email_address',
        headers=headers,
        data=data)
    if 'that email address is taken.' in response.text:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif response.text == '{"success":true}':
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
