from holehe.core import *
from holehe.localuseragent import *

def issuu(email):

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://issuu.com/signup?returnUrl=https%3A%2F%2Fissuu.com%2F&issuu_product=header&issuu_subproduct=anon_home&issuu_context=signin&issuu_cta=log_up',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    response = requests.get(
        'https://issuu.com/call/signup/check-email/' +
        email,
        headers=headers)
    try:
        if response.json()["status"] == "unavailable":
            return({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except BaseException:
        return({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
