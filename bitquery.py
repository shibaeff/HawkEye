import configparser
import json
import logging
import requests

logging.basicConfig(level=logging.DEBUG)

query = """
{
  ethereum(network: ethereum) {
    smartContractCalls(
      options: {asc: "callDepth"}
      txHash: {is: "%s"}
    ) {
      smartContract {
        address {
          address
          annotation
        }
        contractType
        protocolType
        currency {
          symbol
        }
      }
      smartContractMethod {
        name
        signatureHash
      }
      caller {
        address
        annotation
        smartContract {
          contractType
          currency {
            symbol
        }
      }
      }
      success
      amount
      gasValue
      callDepth
    }
  }
}
"""


class BitQuery:
    def __init__(self, config_path="./keys.cfg"):
        """Intialize with a binary tool"""
        config = configparser.ConfigParser()
        config.read(config_path)
        self._key = config["BITQUERY"]["key"]
        logging.debug("read key")

    def form_query(self, addr: str) -> str:
        return query % addr

    def run_query(self, addr: str):
        query = self.form_query(addr)
        headers = {"X-API-KEY": f"{self._key}"}
        request = requests.post('https://graphql.bitquery.io/',
                                json={'query': query}, headers=headers)
        if request.status_code == 200:
            self._resp =  request.json()

    def parse(self):
        self._addrs = list()
        self._raw = self._resp["data"]["ethereum"]['smartContractCalls']
        self._raw_dict = dict()
        self._isToken = list()
        self._Cluster = list()
        self._Address = list()
        self._CodeFor = list()
        for item in self._raw:
            self._raw_dict[item["smartContract"]["address"]["address"]] = item
            self._Address.append(item["smartContract"]["address"]["address"])
            self._isToken.append(item["smartContract"]["contractType"] == "Token")
            # print(item["smartContract"]["contractType"])
        print(self._Address)
        print(self._isToken)
        print(len(set(self._Address)))
    # def prepare_pandas(self):
    #     # self._resp = json.loads(self._resp)
    #     eval(self._resp)
    #     logging.debug(self._resp)
    #     columns = ["Adress", "Cluster", "isToken", "CodeFor"]
