"""Predictions for tokens"""
from analyzer import Analyzer


class TokenAnalyzer(Analyzer):
    def is_simple(self, token: str):
        """
        Determine if token is a simple token
        :param token: token symbol
        :return:
        """
        tokens = ["ETH", "BTC", "DAI", "USDC", "WETH", "WBTC"]
        return token in tokens

    def is_synthetic(self, item: dict):
        """
        Determine if token is synthetic token
        :param item: token symbol
        :return:
        """
        return (item["smartContract"]["contractType"] == "Token" or item["smartContract"]["contractType"] == "DEX") \
               and \
               item["smartContract"]["currency"]["symbol"] != ""

    def fit_predict(self, item: dict, *args, **kwargs) -> (bool, bool):
        if self.is_simple(item["smartContract"]["currency"]["symbol"]):
            return True, False
        elif self.is_synthetic(item):
            return False, True
