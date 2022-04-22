"""Clusterize transactions"""
import pickle

import pandas as pd

from .model import *
from . import Analyzer


class Clusterizer(Analyzer):
    def __init__(self):
        self._m = SimpleCluster()

    def fit(self, *args, **kwargs):
        pass

    def predict(self, *args, **kwargs):
        pass

    def fit_predict(self, data, addr, *args, **kwargs):
        return None
        # return self._m.fit_predict(data, addr)

