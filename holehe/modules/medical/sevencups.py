from holehe.core import *
from holehe.localuseragent import *


async def sevencups(email, client, out):
    name = "sevencups"
    domain = "7cups.com"
    method= "register"
    frequent_rate_limit=True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]), 'DNT': '1',
        'Connection': 'keep-alive', 'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 'www.7cups.com', 'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.7cups.com',
        'Accept-Encoding': 'gzip, late, br',
        'Referer': 'https://www.7cups.com/listener/CreateAccount.php', 'TE': 'Trailers',
        'Content-Type': 'multipart/form-data; boundary=---------------------------'

    }

    data = '-----------------------------\r\nContent-Disposition: form-data; name="email"\r\n\r\n' + email + '\r\n-----------------------------\r\nContent-Disposition: form-data; name="passwd"\r\n\r\n\r\n-----------------------------\r\nContent-Disposition: form-data; name="dobMonth"\r\n\r\n12\r\n-----------------------------\r\nContent-Disposition: form-data; name="dobDay"\r\n\r\n11\r\n-----------------------------\r\nContent-Disposition: form-data; name="dobYear"\r\n\r\n2010\r\n-----------------------------\r\nContent-Disposition: form-data; name="orgPass"\r\n\r\n\r\n-----------------------------\r\nContent-Disposition: form-data; name="data-request-datatype"\r\n\r\njson\r\n-----------------------------\r\nContent-Disposition: form-data; name="submit-value"\r\n\r\nnull\r\n-------------------------------\r\n'

    response = await client.post(
        'https://www.7cups.com/listener/CreateAccount.php',
        data=data,
        headers=headers)
    if response.status_code == 200:
        if "Account already exists with this email address" in response.text:
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
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
