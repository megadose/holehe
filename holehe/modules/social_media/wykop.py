from holehe.core import *
from holehe.localuseragent import *


async def wykop(email, client, out):
    name = "wykop"
    domain = "wykop.pl"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
    }

    auth_data = '{"data": {"key": "w53947240748","secret": "d537d9e0a7adc1510842059ae5316419"} }'

    auth_response = await client.post(
        'https://wykop.pl/api/v3/auth',
        headers=headers,
        data=auth_data)

    headers["Authorization"] = f'Bearer {auth_response.json()["data"]["token"]}'

    data = f'{{"data":{{"email":"{email}"}}}}'

    try:
        response = await client.post(
            'https://wykop.pl/api/v3/users',
            headers=headers,
            data=data)
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "error": True,
                    "others": {"errorMessage": "Unexpected error while sending request."}})
        return None

    body = response.json()

    if response.status_code == 409:
        if "email" in body["error"]["data"].keys() and "exist" in body["error"]["data"]["email"]:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    elif response.status_code == 400 and body["error"]["message"] == "application_limit":
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "error": True,
                        "others": {"errorMessage": f"Wrong response code received: {response.status_code}"}})

