from holehe.core import *
from holehe.localuseragent import *


async def discord(email, client, out):
    name = "discord"
    domain = "discord.com"
    method = "register"
    frequent_rate_limit=False

    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return(result_str)

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Content-Type': 'application/json',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = '{"fingerprint":"","email":"' + str(email) + '","username":"' + get_random_string(20) + '","password":"' + get_random_string(
        20) + '","invite":null,"consent":true,"date_of_birth":"","gift_code_sku_id":null,"captcha_key":null}'

    response = await client.post(
        'https://discord.com/api/v8/auth/register',
        headers=headers,
        data=data)
    # CAPTCHA and validation failures do not prove an email is unused.
    # Use the existing blocked-result flag unless Discord confirms registration.
    exists = False
    if response.status_code == 400:
        try:
            responseData = response.json()
            errors = responseData["errors"]["email"]["_errors"]
            exists = any(
                error["code"] == "EMAIL_ALREADY_REGISTERED"
                for error in errors)
        except (ValueError, KeyError, TypeError):
            pass

    out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                "rateLimit": not exists,
                "exists": exists,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None})
