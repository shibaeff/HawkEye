"""This module provides abstract tester interface"""
from abc import ABCMeta, abstractmethod


class TesterInterface:
    """Abstract tester interface"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def eval(self, expcted, actual):
        """
        Evaluate algorithm quality

        :param expcted: expected data
        :param actual: actual data
        :return: scores
        """
        pass
