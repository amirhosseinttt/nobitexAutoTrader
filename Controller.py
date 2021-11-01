import pyotp
from Model import login
from keys import keys


def get_2fa(based32: str):
    totp = pyotp.TOTP(based32)
    return totp.now()


def request_token():
    username = keys.key_dict['username']
    password = keys.key_dict['password']
    otp = str(get_2fa(keys.key_dict['2fa-backup']))
    response = login(username, password, otp)
    print(response.text)



if __name__ == "__main__":
    print(request_token())
