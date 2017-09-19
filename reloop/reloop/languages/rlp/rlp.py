from sympy import srepr, simplify
from sympy.core import *
from sympy.sets import FiniteSet
from sympy.logic.boolalg import *
from infix import or_infix
import logging
from ordered_set import OrderedSet

log = logging.getLogger(__name__)


class RlpProblem():
    """
    The model of a Relational Linear Program.
    """

    def __init__(self, name, sense, grounder, lpsolver):
        """
        Instantiates the model

        :param name: The name of the problem, describing it
        :param sense: LpMaximize or LpMinimize
        :param logkb: An instance of :class:`.logkb.LogKB`
        :param lp: A type of :class:`lp.LpProblem`
        """

        self.sense = sense
        self.grounder = grounder
        self.lpsolver = lpsolver
        self.name = name
        self._reloop_variables = OrderedSet([])
        self._constraints = []
        self.objective = None

    def add_reloop_variable(self, *predicates):
        """
        Introduces predicates as lp variables. These predicate wont be grounded.

        :param predicates: A tuple of predicates to be added to the model
        """
        for predicate in predicates:
            self._reloop_variables |= {predicate}
            predicate.is_reloop_variable = True

    @property
    def reloop_variables(self):
        return self._reloop_variables

    @property
    def constraints(self):
        return self._constraints

    def __iadd__(self, rhs):
        """
        Adds the objective or a constraint to the model.

        :param rhs: Either an instance of :class :`Expr` (objective) or an instance of Rel or ForAllConstraint (constraint)
        :return: The class instance itself
        """
        import types

        if is_valid_relation(rhs) | isinstance(rhs, ForAll):
            self._constraints += [rhs]
        elif isinstance(rhs, Expr):
            self.objective = rhs
        elif(isinstance(rhs, types.GeneratorType)):
            for item in rhs:
                self += item
        else:
            raise ValueError("'rhs' must be either an instance of sympy.Rel, sympy.Expr or an instance of "
                             "ForallConstraint!")

        return self

    def solve(self, **kwargs):
        """
        Grounds and solves the logical programm.
        """
        lp, varmap = self.grounder.ground(self)
        self.varmap = varmap
        self.solution = self.lpsolver.solve(*lp, **kwargs)

    def status(self):
        """
        Passes the call to self.lpmodel

        :return: The solution status of the LP.

        """
        pass
        # return self.lpmodel.status()

    def get_solution(self):
        """
        :return: The solution of the LP
        """

        # (flow.__class__, ('a', 'b')) => sol
        if self.solution is None:
            return None

        solution = {}
        solution_iter = iter(self.solution)

        for reloop_variable in self._reloop_variables:
            solution.update({reloop_variable(*args): solution_iter.next() for args in self.varmap[reloop_variable]})

        return solution

    def __str__(self):
        asstr = "Objective: "
        asstr += srepr(self.objective)
        asstr += "\n\n"
        asstr += "Subject to:\n"
        for c in self._constraints:
            asstr += srepr(c)
            asstr += "\n"
        return asstr


class Query:
    """
    Internal representation of a logical query.
    """

    def __init__(self, query_symbols, query):
        """

        :param query_symbols: List of type :class:`SubSymbol`
        :param query: A logical query
        """
        if not isinstance(query_symbols, FiniteSet):
            query_symbols = FiniteSet(*query_symbols)

        self._query_symbols = query_symbols
        self._query = simplify(query)

    @property
    def query_symbols(self):
        return self._query_symbols

    @property
    def query(self):
        return self._query


class ForAll(Query):
    """
    Wraps a :class:`.Query` and a :class:`.Rel` to represent a set of constraints.
    """

    def __init__(self, query_symbols, query, relation):
        Query.__init__(self, query_symbols, query)
        if not is_valid_relation(relation):
            raise ValueError("Third argument has to be a valid relation.")
        self.relation = relation
        self.result = []
        self.grounded = False

    def ground(self, logkb):
        """
        Grounds the query and relation

        :param logkb: An implementation of a Logical Knowledge Base
        :type logkb: :class:`.LogKB`
        :return: A set of grounded constraints
        """
        answers = logkb.ask(self.query_symbols, self.query)
        result = set([])
        if answers is not None:
            lhs = self.relation.lhs - self.relation.rhs
            for answer in answers:
                expression_eval_subs = lhs
                for index, symbol in enumerate(self.query_symbols):
                    # this ensures that pydatalog strings do not get parsed by sympy
                    subanswer = answer[index] if not isinstance(answer[index], basestring) \
                        else Symbol(answer[index])
                    expression_eval_subs = expression_eval_subs.subs(symbol, subanswer)
                result |= {self.relation.__class__(expression_eval_subs, 0.0)}

        self.result = result
        self.grounded = True
        return self.result

    def __str__(self):
        return "FORALL " + str(self.query_symbols) + " in " + str(self.query) + ": " + srepr(self.relation)


class SubSymbol(Symbol):
    """
    Just a sympy.Symbol, but inherited to be able to define symbols explicitly
    """
    pass


class VariableSubSymbol(SubSymbol):
    pass


def sub_symbols(*symbols):
    """
    Convenience function for instantiating multiple :class:`.SubSymbol` at once.

    :param symbols: Tuple of strings
    :return: Tuple of SubSymbols
    """
    sub_sym = map(lambda s: SubSymbol(s), symbols)
    if len(sub_sym) == 1:
        return sub_sym[0]
    return tuple(sub_sym)


def boolean_predicate(name, arity):
    """
    Convenience function for generating a :class:`BooleanPredicate` type

    :param name: Name of the predicate
    :param arity: Arity (must match count of relation elements)
    :return: A type with the given name, inherited from :class:`BooleanPredicate`
    """
    return rlp_predicate(name, arity, boolean=true)


def numeric_predicate(name, arity):
    """
    Convenience function for generating a :class:`NumericPredicate` type

    :param name: Name of the predicate
    :param arity: Arity (count of relation elements decremented by one)
    :return: A type with the given name, inherited from :class:`NumericPredicate`
    """
    return rlp_predicate(name, arity, boolean=false)


def rlp_predicate(name, arity, boolean):
    """
    Serves as a predicate type factory: For the given parameters it will create a new type that inherits from Numeric\
    /Boolean/Rlp predicate. Usually this funciton is called by :func:`~numeric_predicate` or
    :func:`~boolean_predicate`

    :param name: Name of the predicate
    :param arity: Arity (count of relation elements decremented by one)
    :param boolean: Flag, indicates wether thd new type is a boolean predicate
    :return: A type with the given name, inherited from a predicate class with properties "arity", "name",\
     "is_reloop_variable" and "__str__"
    """
    if arity < 0:
        raise ValueError("Arity must not be less than 0. Dude!")
    if arity == 0 and boolean:
        raise ValueError("Arity must not be less than 1, if boolean is true. Dude!")

    if arity == 0:
        predicate_type = RlpPredicate
    elif boolean:
        predicate_type = BooleanPredicate
    else:
        predicate_type = NumericPredicate

    predicate_class = type(name, (predicate_type,), {"arity": arity,
                                                     "nargs": arity,
                                                     "name": name,
                                                     "is_reloop_variable": False,
                                                     "__str__": predicate_type.__class__.__str__})
    return predicate_class


class RlpPredicate(Expr):

    def __new__(cls, *args):
        if len(args) != 0:
            raise TypeError('%s takes exactly 0 arguments (%s given)' % (cls.name, len(args)))
        else:
            return Expr.__new__(cls, *args)



class NumericPredicate(RlpPredicate, Function):
    """
    Representing a predicate that is understood as a function. That is, though the relation :math:`R` inside the LogKB
    has :math:`k` elements, we define :math:`R(e_1, ..., e_{k-1}) := e_{k}`.
    """
    def __new__(cls, *args):
        return Function.__new__(cls, *args)


    @classmethod
    def eval(cls, *args):
        return None


class BooleanPredicate(BooleanAtom, Function):
    """
    A Predicate to use in boolean expressions; can be used like a function inside boolean terms.
    """
    pass


class RlpSum(Expr, Query):
    """
    A sum over an answer set, obtained by querying the LogKB.
    """

    def __new__(cls, query_symbols, query, expression):
        if not isinstance(query_symbols, FiniteSet):
            query_symbols = FiniteSet(*query_symbols)

        rlp_sum = Expr.__new__(cls)
        rlp_sum._args = tuple([query_symbols, query, expression])

        return rlp_sum

    def __init__(self, query_symbols, query, expression):
        Query.__init__(self, query_symbols, query)
        if not isinstance(expression, Expr):
            raise ValueError("The third argument was not an sympy.core.Expr!")
        if isinstance(expression, Rel):
            raise ValueError("You cannot use a sympy.core.Rel instance here!")
        self.expression = expression

    @property
    def is_number(self):
        return False

    def _hashable_content(self):
        """We need to overwrite this: The first parameter is a list and because of that the base
        implementation does not work."""
        return tuple(self.query_symbols) + self._args[1:]

    def _sympyrepr(self, printer, *args):
        return "RlpSum(" + str(self.query_symbols) + " in " + str(self.query) + ", " + srepr(self.expression) + ")"


@or_infix
def eq(a, b):
    return Eq(a, b)


@or_infix
def ge(a, b):
    return Ge(a, b)


@or_infix
def le(a, b):
    return Le(a, b)


def is_valid_relation(relation):
    if isinstance(relation, Gt) | isinstance(relation, Lt):
        raise NotImplementedError("StrictGreaterThan and StrictLessThan is not implemented!")
    if isinstance(relation, Rel):
        return True
    return False
