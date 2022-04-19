import configparser
import json
import logging
import random
import pandas as pd
import requests

from queries import *
from src.token_analyzer import TokenAnalyzer

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

    def getSender(self, addr):
        return self.run_query(senderQuery % addr)["data"]["ethereum"]["transactions"][0]["sender"]["address"]

    # this cluster number stands for simple token
    SIMPLE_TOKEN = "Simple Token"

    def parse(self, tx_addr):
        self._resp = self.run_query(txQuery % tx_addr)
        raw = self._resp["data"]["ethereum"]['smartContractCalls']
        self._Res = dict()
        # print(len(raw))
        prev = None
        for item in raw:
            addr = item["smartContract"]["address"]["address"]
            self._Res[addr] = dict()
            self._Res[addr]["Address"] = addr
            self._Res[addr]["isToken"] = False
            self._Res[addr]["Cluster"] = "0"
            self._Res[addr]["CodeFor"] = ""
            # self._Res[addr]["isToken"] = item["smartContract"]["contractType"] == "Token"
            # tokens part
            token_analyzer = TokenAnalyzer()
            is_simple, is_synthetic = token_analyzer.fit_predict(item)
            name = item["smartContract"]["currency"]["symbol"]
            if is_simple:
                self._Res[addr]["Cluster"] = BitQuery.SIMPLE_TOKEN
                self._Res[addr]["isToken"] = True
            elif is_synthetic:
                self._Res[addr]["isToken"] = True
            # codeFor part
            if prev is not None and prev == item["caller"]["address"]:
                self._Res[addr]["CodeFor"] = prev
            prev = addr
        sender = self.getSender(tx_addr)
        self._Res[sender] = dict()
        self._Res[sender]["Address"] = sender
        self._Res[sender]["Cluster"] = "Sender"
        self._Res[sender]["isToken"] = False
        self._Res[sender]["CodeFor"] = ""

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
