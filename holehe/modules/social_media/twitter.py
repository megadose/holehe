from holehe.core import *
from holehe.localuseragent import *


async def twitter(email, client, out):
    name = "twitter"
    domain = "twitter.com"
    method = "register"
    frequent_rate_limit=False

    try:
        req = await client.get(
            "https://api.twitter.com/i/users/email_available.json",
            params={
                "email": email})
        if req.json()["taken"]:
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
