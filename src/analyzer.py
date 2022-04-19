"""This module provides infterfaces for analyzers"""

from abc import abstractproperty, abstractmethod, ABCMeta


class Analyzer():
    __metaclass__ = ABCMeta

    @abstractmethod
    def fit(self, *args, **kwargs):
        """
        This method should be implemeted if costly computations
        are involved
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def predict(self, *args, **kwargs):
        """
        This medthod should be implemeted if costly
        computations were involved
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def fit_predict(self, *args, **kwargs):
        """
        This method is for lightweight predictions
        :param args:
        :param kwargs:
        :return:
        """
        pass
