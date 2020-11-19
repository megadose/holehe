from holehe.core import *
from holehe.localuseragent import *



def bitmoji(email):
    req = requests.get("https://accounts.snapchat.com")
    xsrf = req.text.split('data-xsrf="')[1].split('"')[0]
    webClientId = req.text.split('ata-web-client-id="')[1].split('"')[0]
    url = "https://accounts.snapchat.com/accounts/merlin/login"
    headers = {
        "Host": "accounts.snapchat.com",
        "User-Agent": random.choice(ua["browsers"]["firefox"]),
        "Accept": "*/*",
        "X-XSRF-TOKEN": xsrf,
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "Content-Length": "51",
        "Connection": "close",
        "Cookie": "xsrf_token=" + xsrf + "; web_client_id=" + webClientId
    }
    data = '{"email":' + email + ',"app":"BITMOJI_APP"}'

    response = requests.post(url, data=data, headers=headers)
    if response.status_code != 204:
        data = response.json()
        return({"rateLimit": False, "exists": data["hasBitmoji"], "emailrecovery": None, "phoneNumber": None, "others": None})
    return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
