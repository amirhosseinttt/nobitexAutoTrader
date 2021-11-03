from pathlib import Path
import pyotp
from Model import login, order_book, stats
from keys import keys
from time import sleep
from logger import err_log
import pandas as pd
import json
import datetime
from threading import Thread


class Controller:
    TOKEN = ""
    symbols = None
    price_df = None

    def __init__(self):
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
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
            resp_json = response.json()

            print(resp_json)

        print(response)

    def get_current_price(self):
        symbols = self.symbols.keys()

        src_string = ""

        for symbol in symbols:
            src_string += symbol + ","

        src_string = src_string[:-1]

        try:
            response = stats(str(src_string), "rls")
        except Exception as e:
            response = None
            print(e)

        if response is None:
            pass

        else:
            if response.status_code == 200:
                resp_json = response.json()

                outcome = resp_json["stats"]

                current_time = datetime.datetime.now()
                try:
                    for attribute, value in outcome.items():
                        outcome[attribute]["bestSell"] = int(float(outcome[attribute]["bestSell"]))
                        outcome[attribute]["bestBuy"] = int(float(outcome[attribute]["bestBuy"]))
                        outcome[attribute]["latest"] = int(float(outcome[attribute]["latest"]))
                        outcome[attribute]["dayLow"] = int(float(outcome[attribute]["dayLow"]))
                        outcome[attribute]["dayHigh"] = int(float(outcome[attribute]["dayHigh"]))
                        outcome[attribute]["dayOpen"] = int(float(outcome[attribute]["dayOpen"]))
                        outcome[attribute]["dayClose"] = int(float(outcome[attribute]["dayClose"]))

                except Exception as e:
                    print(e)

                outcome["timestamp"] = int(current_time.timestamp())

                df = pd.json_normalize(outcome)

                if self.price_df is None:
                    self.price_df = df
                else:
                    self.price_df = pd.concat([self.price_df, df], ignore_index=True, axis=0)

            else:
                err_log("get current price didn't return 200", response.text, response.status_code)

    def _collect_price_data(self):
        while True:
            try:
                sleep(1)
                try:
                    self.get_current_price()
                except Exception as e:
                    print(e)

                if self.price_df is not None and len(self.price_df.index) == 5:
                    cur_time = datetime.datetime.now()
                    dir_path = "priceData/" + str(cur_time.year) + "/" + str(cur_time.month) + "/" + str(cur_time.day)
                    Path(dir_path).mkdir(parents=True, exist_ok=True)

                    self.price_df.to_csv(dir_path + "/" + str(int(cur_time.timestamp())) + ".csv")
                    self.price_df = None
            except Exception as e:
                print(e)

    def _get_orderbook_data(self):
        while True:
            try:
                sleep(1)
                try:
                    self.get_order_data()
                except Exception as e:
                    print(e)

            except Exception as e:
                print(e)

    def start(self):
        price_collector_thread = Thread(target=self._collect_price_data, args=(), name="price_collector_thread")
        order_collector_thread = Thread(target=self._get_orderbook_data, args=(), name="order_book_collector_thread")

        threads = [price_collector_thread, order_collector_thread]

        for thread in threads:
            thread.start()

        self._collect_price_data()
