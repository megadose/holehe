<<<<<<< HEAD
from holehe.core import *
from holehe.localuseragent import *
=======
import requests
import random
from bs4 import BeautifulSoup

from holehe.localuseragent import ua
>>>>>>> d81c58f236f6aa0a3078a1d0d810a62f91060beb


def odnoklassniki(email):
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

    session = requests.Session()
    session.headers.update(headers)
    session.get(OK_LOGIN_URL+'&st.email='+email)
    request = session.get(OK_RECOVER_URL)
    root_soup = BeautifulSoup(request.content, 'html.parser')
    soup = root_soup.find('div', {'data-l': 'registrationContainer,offer_contact_rest'})
    if soup:
        account_info = soup.find('div', {'class': 'ext-registration_tx taCenter'})
        masked_email = soup.find('button', {'data-l': 't,email'})
        masked_phone = soup.find('button', {'data-l': 't,phone'})
        if masked_phone:
            masked_phone = masked_phone.find('div', {'class': 'ext-registration_stub_small_header'}).get_text()
        if masked_email:
            masked_email = masked_email.find('div', {'class': 'ext-registration_stub_small_header'}).get_text()
        if account_info:
            masked_name = account_info.find('div', {'class': 'ext-registration_username_header'})
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
            return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})

        others = {
            # TODO: split info separate fields, now only FullName displayed
            'FullName': '; '.join([masked_name, profile_info, profile_registred]),
        }

        return({"rateLimit": False, "exists": True, "emailrecovery": masked_email, "phoneNumber": masked_phone, "others": others})

    if root_soup.find('div', {'data-l': 'registrationContainer,home_rest'}):
        return({"rateLimit": False, "exists": False, "emailrecovery": None, "phoneNumber": None, "others": None})
