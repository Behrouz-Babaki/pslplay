import abc


class Grounder(object):
    """
    Interfaces the implementation of available grounding strategies by providing the essential methods for the grounder
    to work properly. This is an abstract class and should be handled as such. Addtionally implemented grounding strategies
    should inherit from this class.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def ground(self, rlpProblem):
        """
        Grounds a relation linear program by applying a defined grounding strategy. The result is then used to formulate
        the lp problem, which is passed to the lpsolver.

        :param rlpProblem: The problem to be grounded
        :return: The linear program
        """
        raise NotImplementedError("")

    def ask(self, query):
        return self.logkb.ask(query.atoms(), query)
