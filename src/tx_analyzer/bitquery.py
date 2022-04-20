import configparser
import logging
import pandas as pd
import requests

from queries import *
from src.bitquery_api import BitqueryAPI
from src.contract_analyzer import ContractAnalyzer

# logging.basicConfig(level=logging.DEBUG)


class BitQuery:
    def __init__(self, config_path="./keys.cfg"):
        """
        :param config_path: path to config with keys
        """
        config = configparser.ConfigParser()
        config.read(config_path)
        self._key = config["BITQUERY"]["key"]
        logging.debug("read key")
        self.API = BitqueryAPI(self._key)

    def getSender(self, tx_hash):
        """
        Get transaction sender
        :param tx_hash: transaction hash
        :return: transaction sender address
        """
        return self.API.run_query(senderQuery % tx_hash)["data"]["ethereum"]["transactions"][0]["sender"]["address"]

    def parse(self, tx_hash):
        """
        Analyze transaction contracts
        :param tx_hash: transaction hash
        :return:
        """
        self._resp = self.API.run_query(txQuery % tx_hash)
        raw = self._resp["data"]["ethereum"]['smartContractCalls']
        self._Res = dict()
        prev = None
        for item in raw:
            addr = item["smartContract"]["address"]["address"]
            row = ContractAnalyzer().fit_predict(addr, item, prev)
            self._Res[addr] = row
            prev = addr
        sender = self.getSender(tx_hash)
        self._Res[sender] = dict()
        self._Res[sender]["Address"] = sender
        self._Res[sender]["Cluster"] = "Sender"
        self._Res[sender]["isToken"] = False
        self._Res[sender]["CodeFor"] = ""
        return self._Res

    def to_pandas(self):
        """
        Return pandas with solution
        :return: pandas df with solution
        """
        columns = list(list(self._Res.items())[0][1].keys())
        self._df = pd.DataFrame(columns=columns)
        for key, item in self._Res.items():
            self._df = self._df.append(item, ignore_index=True)
        return self._df
