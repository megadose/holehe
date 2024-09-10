from holehe.localuseragent import ua
import random
import string
import requests  # Adjust if using a different HTTP library

async def facebook(email, client, out):
    name = "Facebook"
    domain = "facebook.com"
    method = "register"
    frequent_rate_limit = True

    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://www.facebook.com',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    try:
        response = await client.get("https://www.facebook.com/accounts/emailsignup/", headers=headers)
        if response.status_code == 404:
            raise Exception("Endpoint not found")

        # Extract CSRF token from the response
        token = response.text.split('{"config":{"csrf_token":"')[1].split('"')[0]
    except Exception as e:
        print(f"Error occurred while fetching CSRF token: {e}")
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    data = {
        'email': email,
        'username': ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(random.randint(6, 30))),
        'first_name': '',
        'opt_into_one_tap': 'false'
    }
    headers["x-csrftoken"] = token

    try:
        check = await client.post(
            "https://www.facebook.com/api/v1/web/accounts/web_create_ajax/attempt/",
            data=data,
            headers=headers)
        check = check.json()

        if check["status"] != "fail":
            if 'email' in check["errors"].keys():
                if check["errors"]["email"][0]["code"] == "email_is_taken":
                    out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
                elif "email_sharing_limit" in str(check["errors"]):
                    out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                                "rateLimit": False,
                                "exists": True,
                                "emailrecovery": None,
                                "phoneNumber": None,
                                "others": None})
            else:
                out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                            "rateLimit": False,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
        else:
            out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                        "rateLimit": True,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
    except Exception as e:
        print(f"Error occurred during POST request: {e}")
        out.append({"name": name, "domain": domain, "method": method, "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
