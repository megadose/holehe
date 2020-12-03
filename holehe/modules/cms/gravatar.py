from holehe.core import *
from holehe.localuseragent import *


async def gravatar(email, client, out):
    name = "gravatar"
    hashed_name = hashlib.md5(email.encode()).hexdigest()
    r = await client.get('https://gravatar.com/{hashed_name}.json')
    if r.status_code != 200:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None
    else:
        try:
            data = r.json()
            name = data['entry'][0]['name'].get('formatted')
            others = {
                'FullName': name,
            }

            out.append({"name": name,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": others})
            return None
        except BaseException:
            out.append({"name": name,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return None
