from pathlib import Path
import pyotp
from Model import login, order_book, stats, trades
from keys import keys
from time import sleep
from logger import err_log
import pandas as pd
import json
import datetime
from threading import Thread
import pickle
import os.path


class Controller:
    TOKEN = ""
    symbols = None
    order_list = []
    trade_list = []
    stats_list = []
    symbol_to_list_dict = {}
    max_data_length = 5

    def __init__(self):
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        with open(os.path.dirname(__file__) + "/../symbols.json", "rt") as json_file:
            self.symbols = json.load(json_file)

        symbol_keys = self.symbols.keys()

        for index, key in enumerate(symbol_keys):
            self.symbol_to_list_dict[key] = index
            self.order_list.append([])
            self.trade_list.append([])
            self.stats_list.append([])

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

    def get_order_data(self, original_symbol: str):
        symbol = original_symbol.upper() + "IRT"

        try:
            response = order_book(symbol)
        except Exception as e:
            response = None
            exception = str(e)

        if response is not None and response.status_code == 200:
            resp_json = response.json()

            current_time = datetime.datetime.now()

            bids = resp_json['bids']
            for index in range(len(bids)):
                tmp = [int(bids[index][0]), float(bids[index][1])]
                bids[index] = tmp

            asks = resp_json['asks']
            for index in range(len(asks)):
                tmp = [int(asks[index][0]), float(asks[index][1])]
                asks[index] = tmp

            timestamp = int(current_time.timestamp())

            outcome = [bids, asks, timestamp]
            key = self.symbol_to_list_dict[original_symbol]
            self.order_list[key].append(outcome)

            if len(self.order_list[key]) >= self.max_data_length:
                dir_path = os.path.dirname(__file__) + "/../data/orderData/" + original_symbol + "/" + str(
                    current_time.year) + "/" + str(current_time.month) + "/" + str(current_time.day)
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                with open(dir_path + "/" + str(timestamp) + ".pickle", "wb") as file:
                    pickle.dump(self.order_list[key], file, protocol=pickle.HIGHEST_PROTOCOL)
                    self.order_list[key] = []



        else:
            print(response)

    def get_trade_data(self, original_symbol: str):
        symbol = original_symbol.upper() + "IRT"

        try:
            response = trades(symbol)
        except Exception as e:
            response = None
            exception = str(e)

        if response is not None and response.status_code == 200:
            resp_json = response.json()
            current_time = datetime.datetime.now()
            timestamp = int(current_time.timestamp())

            outcome = resp_json['trades']
            key = self.symbol_to_list_dict[original_symbol]
            outcome1 = []
            if len(self.trade_list[key]) > 5:
                for info in outcome:
                    sw = True
                    for item in self.trade_list[key][len(self.trade_list[key]) - 6:]:
                        if info == item:
                            sw = False
                            break
                    if sw:
                        outcome1.append(info)

            else:
                for info in outcome:
                    self.trade_list[key].append(info)
            for item in outcome1:
                self.trade_list[key].append(item)

            if len(self.trade_list[key]) >= self.max_data_length:
                dir_path = os.path.dirname(__file__) + "/../data/tradeData/" + original_symbol + "/" + str(
                    current_time.year) + "/" + str(current_time.month) + "/" + str(current_time.day)
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                try:
                    df = pd.DataFrame(self.trade_list[key])
                    df.to_csv(dir_path + "/" + str(timestamp) + ".csv")
                    self.trade_list[key] = []
                except Exception as e:
                    print(e)



        else:
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
                timestamp = int(current_time.timestamp())
                try:
                    for attribute, value in outcome.items():
                        outcome[attribute]["bestSell"] = int(float(outcome[attribute]["bestSell"]))
                        outcome[attribute]["bestBuy"] = int(float(outcome[attribute]["bestBuy"]))
                        outcome[attribute]["latest"] = int(float(outcome[attribute]["latest"]))
                        outcome[attribute]["dayLow"] = int(float(outcome[attribute]["dayLow"]))
                        outcome[attribute]["dayHigh"] = int(float(outcome[attribute]["dayHigh"]))
                        outcome[attribute]["dayOpen"] = int(float(outcome[attribute]["dayOpen"]))
                        outcome[attribute]["dayClose"] = int(float(outcome[attribute]["dayClose"]))

                    for attribute, value in outcome.items():
                        symbol = attribute[:-4]
                        key = self.symbol_to_list_dict[symbol]
                        value['timeStamp'] = timestamp
                        self.stats_list[key].append(value)

                        if len(self.stats_list[key]) >= self.max_data_length:
                            dir_path = os.path.dirname(__file__) + "/../data/priceData/" + symbol + "/" + str(
                                current_time.year) + "/" + str(current_time.month) + "/" + str(current_time.day)
                            Path(dir_path).mkdir(parents=True, exist_ok=True)
                            try:
                                df = pd.DataFrame(self.stats_list[key])
                                df.to_csv(dir_path + "/" + str(timestamp) + ".csv")
                                self.stats_list[key] = []
                            except Exception as e:
                                print(e)



                except Exception as e:
                    print(e)

            else:
                err_log("get current price didn't return 200", response.text, response.status_code)

    def _collect_price_data(self):
        while True:
            try:
                sleep(1)
                self.get_current_price()
            except Exception as e:
                print(e)

    def _get_orderbook_data(self, symbol):
        while True:
            try:
                sleep(1)
                self.get_order_data(symbol)
            except Exception as e:
                print(e)

    def _get_trade_data(self, symbol):
        while True:
            try:
                sleep(0.5)
                self.get_trade_data(symbol)
            except Exception as e:
                print(e)

    def start(self):
        price_collector_thread = Thread(target=self._collect_price_data, args=(), name="price_collector")

        threads = [price_collector_thread]

        for symbol in self.symbols.keys():
            thread1 = Thread(target=self._get_orderbook_data, args=(symbol,), name=str(symbol) + "order_collector")
            thread2 = Thread(target=self._get_trade_data, args=(symbol,), name=str(symbol) + "trade_collector")
            threads.append(thread1)
            threads.append(thread2)

        for thread in threads:
            thread.start()
