from holehe.core import *
from holehe.localuseragent import *


async def odnoklassniki(email, client, out):
    name = "odnoklassniki"
    domain = "ok.ru"
    method = "password recovery"
    frequent_rate_limit=False

    # credits: https://github.com/shllwrld/ok_checker/
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.5',
        'Referer': 'https://ok.ru/',
        'DNT': '1',
        'Connection': 'keep-alive',
    }

    OK_LOGIN_URL = 'https://www.ok.ru/dk?st.cmd=anonymMain&st.accRecovery=on&st.error=errors.password.wrong'
    OK_RECOVER_URL = 'https://www.ok.ru/dk?st.cmd=anonymRecoveryAfterFailedLogin&st._aid=LeftColumn_Login_ForgotPassword'
    try:
        await client.get(OK_LOGIN_URL + '&st.email=' + email, headers=headers)
        request = await client.get(OK_RECOVER_URL, headers=headers)
        root_soup = BeautifulSoup(request.content, 'html.parser')
        soup = root_soup.find(
            'div', {
                'data-l': 'registrationContainer,offer_contact_rest'})
        if soup:
            account_info = soup.find(
                'div', {'class': 'ext-registration_tx taCenter'})
            masked_email = soup.find('button', {'data-l': 't,email'})
            masked_phone = soup.find('button', {'data-l': 't,phone'})
            if masked_phone:
                masked_phone = masked_phone.find(
                    'div', {'class': 'ext-registration_stub_small_header'}).get_text()
            if masked_email:
                masked_email = masked_email.find(
                    'div', {'class': 'ext-registration_stub_small_header'}).get_text()
            if account_info:
                masked_name = account_info.find(
                    'div', {'class': 'ext-registration_username_header'})
                if masked_name:
                    masked_name = masked_name.get_text()
                account_info = account_info.findAll('div', {'class': 'lstp-t'})
                if account_info:
                    profile_info = account_info[0].get_text()
                    profile_registred = account_info[1].get_text()
                else:
                    profile_info = None
                    profile_registred = None
            else:
                out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                            "rateLimit": False,
                            "exists": False,
                            "emailrecovery": None,
                            "phoneNumber": None,
                            "others": None})
                return None

            others = {
                # TODO: split info separate fields, now only FullName displayed
                'FullName': '; '.join([masked_name, profile_info, profile_registred]),
            }

            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": True,
                        "emailrecovery": masked_email,
                        "phoneNumber": masked_phone,
                        "others": others})
            return None

        if root_soup.find('div', {'data-l': 'registrationContainer,home_rest'}):
            out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                        "rateLimit": False,
                        "exists": False,
                        "emailrecovery": None,
                        "phoneNumber": None,
                        "others": None})
            return None
    except :
        out.append({"name": name,"domain":domain,"method":method,"frequent_rate_limit":frequent_rate_limit,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
