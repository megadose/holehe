from holehe.core import *
from holehe.localuseragent import *


async def firefox(email, client, out):
    name = "firefox"
    req = await client.post(
        "https://api.accounts.firefox.com/v1/account/status",
        data={
            "email": email})
    if "false" in req.text:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif "true" in req.text:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
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
