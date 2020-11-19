import requests
import random
import json
import re

from holehe.localuseragent import ua


def github(email):
    s = requests.session()
    freq = s.get("https://github.com/join")
    token_regex = re.compile(
        r'<auto-check src="/signup_check/username[\s\S]*?value="([\S]+)"[\s\S]*<auto-check src="/signup_check/email[\s\S]*?value="([\S]+)"')
    token = re.findall(token_regex, freq.text)
    data = {"value": email, "authenticity_token": token[0]}
    req = s.post("https://github.com/signup_check/email", data=data)
    if "Your browser did something unexpected." in req.text:
        return({"rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
    if req.status_code == 422:
        return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
    if req.status_code == 200:
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    else:
        return({"rateLimit": True, "exists": None, "emailrecovery": None, "phoneNumber": None, "others": None})
