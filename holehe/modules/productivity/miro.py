from holehe.core import *
from holehe.localuseragent import *
import re


async def miro(email, client, out):
    name = "miro_com"
    domain = "miro.com"
    method = "register"
    frequent_rate_limit = True

    _ua = random.choice(ua["browsers"]["chrome"])
    headers = {
        "User-Agent": _ua,
        "User-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en,en-US;q=0.5",
    }

    try:
        token = None
        r = await client.get("https://miro.com/", headers=headers, timeout=1)
        headers = r.headers
        del headers["Set-Cookie"]
        headers["User-Agent"] = _ua
        if "Your request was blocked" in r.text or r.status_code != 200:
            out.append(
                {
                    "name": name,
                    "domain": domain,
                    "method": method,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None,
                }
            )
            return None

        r = await client.get("https://miro.com/en/signup/", headers=headers, timeout=1)
        if "Your request was blocked" in r.text or r.status_code != 200:
            out.append(
                {
                    "name": name,
                    "domain": domain,
                    "method": method,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None,
                }
            )
            return None
        else:
            token = re.findall(
                r'<input type="hidden" name="signup\[token\]" value="(.*)">', r.text
            )[0]
            if not token:
                out.append(
                    {
                        "name": name,
                        "domain": domain,
                        "method": method,
                        "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None,
                    }
                )
                return None
            else:

                data = {"registration_check": email, "csrfToken": token}

                headers["X-Requested-With"] = "XMLHttpRequest"
                headers["Host"] = "miro.com"
                headers["Origin"] = "https://miro.com"
                headers["Referer"] = "https://miro.com/en/signup/"
                headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
                headers[
                    "Content-Type"
                ] = "application/x-www-form-urlencoded; charset=UTF-8"
                headers["Sec-Fetch-Dest"] = "empty"
                headers["Sec-Fetch-Mode"] = "cors"
                headers["Sec-GPC"] = "1"

                r = await client.post(
                    "https://miro.com/signup/", headers=headers, data=data, timeout=1
                )
                if "Your request was blocked" in r.text or r.status_code != 200:
                    out.append(
                        {
                            "name": name,
                            "domain": domain,
                            "method": method,
                            "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": True,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None,
                        }
                    )
                    return None
                else:
                    if r:
                        if '"isAlreadyRegistered":true' in r.text:
                            out.append(
                                {
                                    "name": name,
                                    "domain": domain,
                                    "method": method,
                                    "frequent_rate_limit": frequent_rate_limit,
                                    "rateLimit": False,
                                    "exists": True,
                                    "emailrecovery": None,
                                    "phoneNumber": None,
                                    "others": None,
                                }
                            )
                            return None
                        elif '"isAlreadyRegistered":false' in r.text:
                            out.append(
                                {
                                    "name": name,
                                    "domain": domain,
                                    "method": method,
                                    "frequent_rate_limit": frequent_rate_limit,
                                    "rateLimit": False,
                                    "exists": False,
                                    "emailrecovery": None,
                                    "phoneNumber": None,
                                    "others": None,
                                }
                            )
                            return None
                        else:
                            out.append(
                                {
                                    "name": name,
                                    "domain": domain,
                                    "method": method,
                                    "frequent_rate_limit": frequent_rate_limit,
                                    "rateLimit": True,
                                    "exists": False,
                                    "emailrecovery": None,
                                    "phoneNumber": None,
                                    "others": None,
                                }
                            )
                            return None

    except Exception as exx:
        out.append(
            {
                "name": name,
                "domain": domain,
                "method": method,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": True,
                "exists": False,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None,
            }
        )
        return None
