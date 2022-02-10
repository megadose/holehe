from holehe.core import *
from holehe.localuseragent import *


async def osu(email, client, out):
    name = "osu"
    domain = "osu.ppy.sh"
    method = "register"
    frequent_rate_limit=False

    try:
        data = {'user[username]': 'wh42fsdjvk',
                'user[user_email]': email,
                "user[password]": "*****",
                "check": '1'
        }

        headers = {"User-Agent": "osu!"}

        req = await client.post("https://osu.ppy.sh/users", headers=headers, data=data)

        if 'Email address already used.' in req.text:
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
    except :
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
