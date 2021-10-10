from holehe.core import *
from holehe.localuseragent import *

async def apple(email, client, out):
    name = "apple"
    domain = "apple.com"
    method= "password recovery"
    frequent_rate_limit=False

    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': random.choice(ua["browsers"]["safari"]),
        'Accept-Language': 'fr-fr',
        'Accept-Encoding': 'gzip',
        'Connection': 'keep-alive'}

    try:
        response = await client.post('https://iforgot.apple.com/password/verify/appleid', headers=headers, data = {'id': email})
        NumHTML = BeautifulSoup(response.text, 'html.parser').find('script', type="application/json", id="boot_args")
        phones = []
        n = 0
        while True:
            try:
                phoneList = json.loads(NumHTML.contents[0])["data"]["trustedPhones"]
                phones.append(phoneList[n]["number"])
                n += 1
            except (IndexError, KeyError) as ex:
                break

        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": None,
                        "phoneNumber": ', '.join(phones) if phones != [] else None,
                        "others": None})

    except httpx.TooManyRedirects:
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
