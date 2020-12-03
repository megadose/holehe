from holehe.core import *
from holehe.localuseragent import *


async def github(email, client, out):
    name = "github"
    freq = await client.get("https://github.com/join")
    token_regex = re.compile(
        r'<auto-check src="/signup_check/username[\s\S]*?value="([\S]+)"[\s\S]*<auto-check src="/signup_check/email[\s\S]*?value="([\S]+)"')
    token = re.findall(token_regex, freq.text)
    data = {"value": email, "authenticity_token": token[0]}
    req = await client.post("https://github.com/signup_check/email", data=data)
    if "Your browser did something unexpected." in req.text:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": None,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif req.status_code == 422:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif req.status_code == 200:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": None,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
