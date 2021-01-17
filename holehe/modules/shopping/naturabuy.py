from holehe.core import *
from holehe.localuseragent import *


async def naturabuy(email, client, out):
    name = "naturabuy"
    domain = "naturabuy.fr"
    method = "register"
    frequent_rate_limit=False

    def get_random_string(length):
        letters = string.digits
        result_str = ''.join(random.choice(letters) for i in range(length))
        return(result_str)

    randomChar = str(get_random_string(30))
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'multipart/form-data; boundary=---------------------------',
        'Origin': 'https://www.naturabuy.fr',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    data = '-----------------------------\r\nContent-Disposition: form-data; name="jsref"\r\n\r\nemail\r\n-----------------------------\r\nContent-Disposition: form-data; name="jsvalue"\r\n\r\n' + \
        email + '\r\n-----------------------------\r\nContent-Disposition: form-data; name="registerMode"\r\n\r\nfull\r\n-------------------------------\r\n'

    response = await client.post('https://www.naturabuy.fr/includes/ajax/register.php', headers=headers, data=data)
    try:
        if json.loads(response.text)["free"] == False:
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
    except BaseException:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
