from holehe.core import *
from holehe.localuseragent import *


async def twitter(email, client, out):
    name = "twitter"
    req = await client.get(
        "https://api.twitter.com/i/users/email_available.json",
        params={
            "email": email})
    if req.json()["taken"]:
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
