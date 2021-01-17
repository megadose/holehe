from holehe.core import *
from holehe.localuseragent import *


async def evernote(email, client, out):
    name = "evernote"
    domain = "evernote.com"
    method = "login"
    frequent_rate_limit=False

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.evernote.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.evernote.com/Login.action',
        'TE': 'Trailers',
    }
    data = await client.get("https://www.evernote.com/Login.action", headers=headers)
    data2 = {
        'username': email, 'evaluateUsername': '',
        'hpts': data.text.split('document.getElementById("hpts").value = "')
        [1].split('"')[0],
        'hptsh': data.text.split('document.getElementById("hptsh").value = "')
        [1].split('"')[0],
        'analyticsLoginOrigin': 'login_action', 'clipperFlow': 'false',
        'showSwitchService': 'true', 'usernameImmutable': 'false',
        '_sourcePage': data.text.split(
            '<input type="hidden" name="_sourcePage" value="')[1].split('"')
        [0],
        '__fp': data.text.split('<input type="hidden" name="__fp" value="')
        [1].split('"')[0]}
    response = await client.post('https://www.evernote.com/Login.action', data=data2, headers=headers)
    if "usePasswordAuth" in response.text:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif "displayMessage" in response.text:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
