from holehe.core import *
from holehe.localuseragent import *


def pinterest(email):
    req = requests.get(
        "https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/",
        params={
            "source_url": "/",
            "data": '{"options": {"email": "' + email + '"}, "context": {}}'})
    if req.json()["resource_response"]["data"]:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
