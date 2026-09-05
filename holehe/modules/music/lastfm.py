from holehe.core import *
from holehe.localuseragent import *


async def lastfm(email, client, out):
    name = "lastfm"
    domain = "last.fm"
    method= "register"
    frequent_rate_limit=False

    try:
        req = await client.get("https://www.last.fm/join")
        token = req.cookies["csrftoken"]
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    data = {"csrfmiddlewaretoken": token, "userName": "", "email": email}
    headers = {
        "Accept": "*/*",
        "Referer": "https://www.last.fm/join",
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "csrftoken=" + str(token),
    }
    try:

        check = await client.post("https://www.last.fm/join/partial/validate", headers=headers, data=data)
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    if check.json().get("email", {}).get("error_messages", [None])[0] == "Sorry, that email address is already registered to another account.":
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


# Sample response from valid email on last.fm:
# {
#     "userName": {
#         "valid": false,
#         "success_message": "Ok, that username can be yours!",
#         "error_messages": [
#             "Please enter a username."
#         ]
#     },
#     "email": {
#         "valid": false,
#         "success_message": "Looking good!",
#         "error_messages": [
#             "Sorry, that email address is already registered to another account."
#         ]
#     },
#     "password": {
#         "valid": false,
#         "success_message": "Ok.",
#         "error_messages": [
#             "Please choose a password."
#         ]
#     },
#     "passwordConf": {
#         "valid": false,
#         "success_message": "Ok.",
#         "error_messages": [
#             "Please type your password again."
#         ]
#     },
#     "recaptcha": {
#         "valid": false,
#         "error_messages": [
#             "You didn't complete the captcha properly. Try again?"
#         ]
#     },
#     "backto": {
#         "valid": true
#     },
#     "terms": {
#         "valid": false,
#         "error_messages": [
#             "Not quite so fast! Please agree to these terms first."
#         ]
#     }
# }