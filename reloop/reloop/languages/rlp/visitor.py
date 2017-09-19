from abc import ABCMeta

from reloop.languages.rlp import *
import abc


class ImmutableVisitor(object):
    """
    Class interfacing a generic visitor used by the Normalizer
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def visit(self, expr):
        raise NotImplementedError("")

    @property
    def result(self):
        return self._result

