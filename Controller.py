import pyotp
from Model import login, order_book, stats
from keys import keys
from time import sleep
from logger import err_log
import sys
import pandas as pd
import json


class Controller:
    TOKEN = ""
    symbols = None
    price_df = None

    def __init__(self):
        self.price_df = pd.DataFrame()
        with open("symbols.json", "rt") as json_file:
            self.symbols = json.load(json_file)

    def _get_2fa(self, based32: str):
        totp = pyotp.TOTP(based32)
        return totp.now()

    def request_new_token(self):
        exception = ""
        username = keys.key_dict['username']
        password = keys.key_dict['password']
        otp = str(self._get_2fa(keys.key_dict['2fa-backup']))
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
            otp = str(self._get_2fa(keys.key_dict['2fa-backup']))
            try:
                response = login(username, password, otp)
            except Exception as e:
                response = None
                exception = str(e)

            if response is not None and response.status_code == 200:
                err_log("login fixed", response.text, 200)

        self.TOKEN = response.json()['key']

    def get_order_data(self):
        symbol = "BTCIRT"

        try:
            response = order_book(symbol)
        except Exception as e:
            response = None
            exception = str(e)

        if response.status_code == 200:
            response.json()

        # todo: fill this part

    def get_current_price(self):
        symbols = self.symbols.keys()

        src_string = ""

        for symbol in symbols:
            src_string += symbol + ","

        src_string = src_string[:-1]
        print(src_string)

        try:
            response = stats(str(src_string), "rls")
        except Exception as e:
            response = None
            exception = str(e)

        if response is None:
            pass

        else:
            if response.status_code == 200:
                resp_json = response.json()
                print(resp_json)
                print(sys.getsizeof(resp_json))
