"""Predictions for tokens"""
from . import Analyzer


class TokenAnalyzer(Analyzer):
    """Analyze tokens"""

    def is_simple(self, token: str) -> bool:
        """
        Determine if token is a simple token

        :param token: token symbol
        :return: if token is simple
        """
        tokens = ["ETH", "BTC", "DAI", "USDC", "WETH", "WBTC"]
        return token in tokens

    def is_synthetic(self, item: dict) -> bool:
        """
        Determine if token is synthetic token

        :param item: smart contract data
        :return: if token is synthetic
        """
        return (item["smartContract"]["contractType"] == "Token" or item["smartContract"]["contractType"] == "DEX") \
               and \
               item["smartContract"]["currency"]["symbol"] != ""

    def fit_predict(self, item: dict, *args, **kwargs) -> (bool, bool):
        """
        Make a prediction

        :param item: smart contract data
        :param args:
        :param kwargs:
        :return: if token is simple, if token is synthetic
        """
        if self.is_simple(item["smartContract"]["currency"]["symbol"]):
            return True, False
        elif self.is_synthetic(item):
            return False, True
        return False, False
