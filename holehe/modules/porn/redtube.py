from holehe.core import *
from holehe.localuseragent import *


async def redtube(email, client, out):
    name = "redtube"
    domain = "redtube.com"
    method= "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://redtube.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    r = await client.get("https://redtube.com/register", headers=headers)
    soup = BeautifulSoup(r.text, features="html.parser")
    try:
        token = soup.find(attrs={"id": "token"}).get("value")
        if token is None:
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return None
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    headers['X-Requested-With'] = 'XMLHttpRequest'

    params = {
        'token': token,
    }

    data = {
        'token': token,
        'redirect': '',
        'check_what': 'email',
        'email': email
    }

    response = await client.post('https://www.redtube.com/user/create_account_check', headers=headers, params=params, data=data)

    if "Email has been taken." in response.text:
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
