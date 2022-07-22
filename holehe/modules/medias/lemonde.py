from holehe.core import *
from holehe.localuseragent import *

async def lemonde (email, client, out):
    name = "lemonde"
    domain = "lemonde.fr"
    method = "register"
    frequent_rate_limit=False

    headers = {
        'User-Agent' : random.choice(ua["browsers"]["firefox"]),
        'Accept' : '*/*',
        'Accept-Language' : 'fr,fr-FR;q=0.9, en-US;q=0.5,en;q=0.3',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin' : 'https://secure.lemonde.fr',
        'Connection' : 'keep-alive',
    }

    data = {
        'mail' : str(email),
        'password' : 'requiredpassword',
        'newsletters' : '[]',
        'origin': 'web'
    }

    response = await client.post('https://secure.lemonde.fr/sfuser/register', headers=headers,data=data)
    if "message error" and ("Il existe déjà un compte" or "There is an existing") in response.text:
        out.append({"name" : name, "domain":domain, "method":method, "frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others":None})
    else:
        out.append({"name" : name, "domain":domain, "method":method, "frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others":None})
