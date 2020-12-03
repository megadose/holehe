from holehe.core import *
from holehe.localuseragent import *

async def replit(email, client, out):

    name="replit"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'content-type': 'application/json',
        'x-requested-with': 'XMLHttpRequest',
        'Origin': 'https://repl.it',
        'Connection': 'keep-alive',
    }

    data = '{"email":"'+str(email)+'"}'

    response = await client.post('https://repl.it/data/user/exists', headers=headers, data=data)
    try:
        if response.json()['exists'] == True:
            return ({"rateLimit": False, "exists": True, "emailrecovery": None, "phoneNumber": None, "others": None})
        else:
            return ({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
    except:
        return ({"rateLimit": True, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
