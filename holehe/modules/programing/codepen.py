from holehe.core import *
from holehe.localuseragent import *


async def codepen(email, client, out):
    name = "codepen"
    domain = "codepen.io"
    method = "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://codepen.io/accounts/signup/user/free',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://codepen.io',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }
    try:
        req = await client.get(
            "https://codepen.io/accounts/signup/user/free",
            headers=headers)
        soup = BeautifulSoup(req.content, features="html.parser")
        token = soup.find(attrs={"name": "csrf-token"}).get("content")
        headers["X-CSRF-Token"] = token
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    data = {
        'attribute': 'email',
        'value': email,
        'context': 'user'
    }

    response = await client.post(
        'https://codepen.io/accounts/duplicate_check',
        headers=headers,
        data=data)
    if "That Email is already taken." in response.text:
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
