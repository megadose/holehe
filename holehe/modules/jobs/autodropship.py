from holehe.core import *
from holehe.localuseragent import *


async def autodropship(email, client, out):
	name = "autodropship"
	domain = "autods.com"
	method= "other"
	frequent_rate_limit=False

	headers = {
		"User-Agent": random.choice(ua["browsers"]["chrome"]),
		"Accept": "application/json, text/plain, */*",
		"Content-Type": "application/json",
		"Host": "v2-api.autods.com" 
	}

	data = {
		"email": email
	}

	try:
		response = await client.post("https://v2-api.autods.com/users/check-email/", headers=headers, json=data)
		print(response.json())
		if "UserNotFound" in response.json():
			out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
						"rateLimit": False,
						"exists": False,
						"emailrecovery": None,
						"phoneNumber": None,
						"others": None})
		else:
			others = {
				"Last Login": response.json()["last_login_date"],
				"ID": str(response.json()["id"]),

			}
			out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
						"rateLimit": False,
						"exists": True,
						"emailrecovery": None,
						"phoneNumber": None,
						"others": None})
	except Exception:
		out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
					"rateLimit": True,
					"exists": False,
					"emailrecovery": None,
					"phoneNumber": None,
					"others": None})