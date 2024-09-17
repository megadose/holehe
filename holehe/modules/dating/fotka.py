from holehe.core import *
from holehe.localuseragent import *


async def fotka(email, client, out):
    name = "fotka"
    domain = "fotka.com"
    method = "login"
    frequent_rate_limit=True

    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return(result_str)

    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = f'login={email}&pass={get_random_string(20)}&back_url='

    try:
        response = await client.post(
            'https://api.fotka.com/v2/zaloguj/?form_login=1',
            headers=headers,
            data=data)
    except Exception:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
            "rateLimit": False,
            "exists": False,
            "emailrecovery": None,
            "phoneNumber": None,
            "error": True,
            "others": {"errorMessage": "Unexpected error while sending request."}})
        return None


    location = response.headers['location']

    if 'error=-2' in location:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit, 
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None}) # multiple accounts found
    elif 'error=-9' in location or 'error=-7' in location:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif 'error=-5' in location or 'error=-6' in location:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    elif 'error=-1' in location or 'error=-4' in location or 'error=-8' in location:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "error": True,
                    "others": {"errorMessage": "Invalid response code."}})
