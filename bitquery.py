import configparser
import json
import logging
import random
import pandas as pd
import requests

from queries import *

logging.basicConfig(level=logging.DEBUG)

class BitQuery:
    def __init__(self, config_path="./keys.cfg"):
        """Intialize with a binary tool"""
        config = configparser.ConfigParser()
        config.read(config_path)
        self._key = config["BITQUERY"]["key"]
        logging.debug("read key")

    def isSimple(self, token):
        tokens = ["ETH", "BTC", "DAI", "USDC", "WETH", "WBTC"]
        for tok in tokens:
            if tok == token:
                return True
        return False

    def run_query(self, query):
        headers = {"X-API-KEY": f"{self._key}"}
        request = requests.post('https://graphql.bitquery.io/',
                                json={'query': query}, headers=headers)
        if request.status_code == 200:
            self._resp = request.json()
        return self._resp

    # def get_calls(self, addr):
    #     # print(callsQuery % addr)
    #     raw = self.run_query(callsQuery % addr)
    #     s = set()
    #     for item in raw["data"]["ethereum"]["smartContractCalls"]:
    #         # print(item["smartContract"]["address"]["address"])
    #         s.add(item["smartContract"]["address"]["address"])
    #     return s

    # this cluster number stands for simple token
    SIMPLE_TOKEN = -1

    def parse(self, addr):
        self._resp = self.run_query(txQuery % addr)
        raw = self._resp["data"]["ethereum"]['smartContractCalls']
        self._Res = dict()
        # print(len(raw))
        prev = None
        for item in raw:
            addr = item["smartContract"]["address"]["address"]
            self._Res[addr] = dict()
            self._Res[addr]["Address"] = addr
            self._Res[addr]["isToken"] = False
            self._Res[addr]["Cluster"] = 0
            self._Res[addr]["CodeFor"] = ""
            # self._Res[addr]["isToken"] = item["smartContract"]["contractType"] == "Token"
            # tokens part
            name = item["smartContract"]["currency"]["symbol"]
            if self.isSimple(name):
                self._Res[addr]["Cluster"] = BitQuery.SIMPLE_TOKEN
                self._Res[addr]["isToken"] = True
            elif (item["smartContract"]["contractType"] == "Token" or item["smartContract"]["contractType"] == "DEX")\
                    and\
                    item["smartContract"]["currency"]["symbol"] != "":
                self._Res[addr]["isToken"] = True
             # codeFor part
            if prev is not None and prev == item["caller"]["address"]:
                self._Res[addr]["CodeFor"] = prev
            prev = addr

    def to_pandas(self):
        columns = list(list(self._Res.items())[0][1].keys())
        self._df = pd.DataFrame(columns=columns)
        for key, item in self._Res.items():
            self._df = self._df.append(item, ignore_index=True)
        return self._df
    # def prepare_pandas(self):
    #     # self._resp = json.loads(self._resp)
    #     eval(self._resp)
    #     logging.debug(self._resp)
    #     columns = ["Adress", "Cluster", "isToken", "CodeFor"]
