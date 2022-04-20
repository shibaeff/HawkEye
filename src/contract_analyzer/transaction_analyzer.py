"""Analyze transaction cluster"""
from . import TokenAnalyzer, DelegateAnalyzer, Analyzer


class ContractAnalyzer(Analyzer):
    """Analyzes smaert contract"""
    SIMPLE_TOKEN = "Simple Token"

    def fit_predict(self, addr, item, prev, *args, **kwargs):
        """
        Make a prediction

        :param addr: current contract address
        :param item: current contrct data
        :param prev: prev contrct address
        :param args:
        :param kwargs:
        :return: contract cluster, contract delegate call, is contract is a token
        """
        row = dict()
        row["Address"] = addr
        row["isToken"] = False
        row["Cluster"] = "0"
        row["CodeFor"] = ""
        # row["isToken"] = item["smartContract"]["contractType"] == "Token"
        # tokens part
        token_analyzer = TokenAnalyzer()
        is_simple, is_synthetic = token_analyzer.fit_predict(item)
        name = item["smartContract"]["currency"]["symbol"]
        if is_simple:
            row["Cluster"] = ContractAnalyzer.SIMPLE_TOKEN
            row["isToken"] = True
        elif is_synthetic:
            row["isToken"] = True
        # codeFor part
        delegate_analyzer = DelegateAnalyzer()
        caller = delegate_analyzer.fit_predict(prev, item)
        if caller != "":
            row["CodeFor"] = caller
        return row
