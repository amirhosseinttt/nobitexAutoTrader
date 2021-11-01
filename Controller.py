import pyotp
from Model import login
from keys import keys
from time import sleep
from logger import err_log

TOKEN = ""


def get_2fa(based32: str):
    totp = pyotp.TOTP(based32)
    return totp.now()


def request_new_token():
    exception = ""
    response = None
    username = keys.key_dict['username']
    password = keys.key_dict['password']
    otp = str(get_2fa(keys.key_dict['2fa-backup']))
    try:
        response = login(username, password, otp)
    except Exception as e:
        response = None
        exception = str(e)

    while response is None or response.status_code != 200:
        if response is None:
            err_log("login requests failed to send!", exception, 1)
        else:
            err_log("login error", response.text, 1)
        sleep(5)
        username = keys.key_dict['username']
        password = keys.key_dict['password']
        otp = str(get_2fa(keys.key_dict['2fa-backup']))
        try:
            response = login(username, password, otp)
        except Exception as e:
            response = None
            exception = str(e)

        if response != None and response.status_code == 200:
            err_log("login fixed", response.text, 200)

    TOKEN = response.json()['key']



