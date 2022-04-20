"""A collection of testers"""
from . import TesterInterface
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np


def rates(true, pre, positives, negatives):
    tn, fp, fn, tp = confusion_matrix(true, pre).ravel()
    return np.array([accuracy_score(true, pre), tp / positives, tn / negatives])


class TokenTester(TesterInterface):
    """Test accuracy of token classification"""

    def eval(self, expected, actual):
        """Evalute score

        :param expected: expcted data
        :param actual: actual data
        :return: accuracy score, tpr, tnr
        """
        return rates(expected, actual, sum(expected), len(expected) - sum(expected))
