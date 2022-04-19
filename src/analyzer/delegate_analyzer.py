"""Analyzer to determine delegate calls"""
from src.analyzer import Analyzer


class DelegateAnalyzer(Analyzer):
    """Determine source of delegate call if it happened"""
    def fit_predict(self, prev: str, item: dict, *args, **kwargs) -> str:
        """
        Returns the addr of smart contract if delegate call happened
        :param prev: previous contract address
        :param item: current contract
        :param args:
        :param kwargs:
        :return: address of the contract that performs delegate call, return empty string if no
        """
        if prev is not None and prev == item["caller"]["address"]:
            return prev
        return ""
