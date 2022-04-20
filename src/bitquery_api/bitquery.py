"""Run Biquery Graph QL queries"""
import requests


class BitqueryAPI:
    """
    Run Biquery API calls
    """
    def __init__(self, key):
        """

        :param key: Bitquery API key
        """
        self._key = key

    """Runs Biquery Graph QL queries"""
    def run_query(self, query: str) -> dict:
        """
        Run raw query

        :param query: query json
        :return: query resp
        """
        headers = {"X-API-KEY": f"{self._key}"}
        request = requests.post('https://graphql.bitquery.io/',
                                json={'query': query}, headers=headers)
        if request.status_code == 200:
            self._resp = request.json()
        return self._resp
