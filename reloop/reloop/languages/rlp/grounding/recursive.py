from grounder import Grounder
from reloop.languages.rlp import *
from sympy.core.relational import Rel, Ge, Le, Eq
from sympy.core import expand, Add, Mul, Pow, Expr, Float
from sympy.logic.boolalg import *
import scipy.sparse
import numpy
from ordered_set import OrderedSet
from reloop.languages.rlp.visitor import *

class RecursiveGrounder(Grounder):
    """

    """

    def __init__(self, logkb):
        self.logkb = logkb

    def ground(self, rlpProblem):
        self.lpmodel = LpProblem(rlpProblem.sense)
        self.add_objective_to_lp(self.ground_expression(rlpProblem.objective))

        for constraint in rlpProblem.constraints:
            if isinstance(constraint, Rel):
                lhs = constraint.lhs - constraint.rhs
                ground_result = constraint.__class__(expand(self.ground_expression(lhs)), 0.0)
                self.add_constraint_to_lp(ground_result)
            else:
                # maybe pre-ground here?
                # result = self.ground_expression(constraint.relation, bound=constraint.query_symbols)
                result = constraint.ground(self.logkb)
                for expr in result:
                    ground = self.ground_expression(expr)
                    ground_result = ground.__class__(expand(self.ground_expression(ground.lhs)), ground.rhs)
                    self.add_constraint_to_lp(ground_result)

        return self.lpmodel.get_scipy_matrices(rlpProblem), self.lpmodel.lp_variables

    def ground_expression(self, expr):

        expression_grounder = ExpressionGrounder(expr, self.logkb)
        return expression_grounder.result

    def add_constraint_to_lp(self, constraint):
        """
        Adds a grounded constraint to the LP

        :param constraint: The grounded constraint.
        """
        # log.debug("Add constraint: " + str(constraint))
        # + "\n" + srepr(constraint)

        if self.is_valid_constraint(constraint):
            lhs = constraint.lhs
            b = constraint.rhs
            if constraint.lhs.func is Add:
                for s in constraint.lhs.args:
                    if s.is_Atom:
                        lhs -= s
                        b -= s

            # TODO handle Lt and Gt
            if constraint.func is Ge:
                sense = 1
            elif constraint.func is Eq:
                sense = 0
            elif constraint.func is Le:
                sense = -1
            self.lpmodel += (lhs, b, sense)

    def add_objective_to_lp(self, objective):
        """
        Adds a grounded objective to the LP

        :param objective: A grounded expression (the objective)
        """
        # log.debug("Add objective: " + str(objective))
        # + "\n" + srepr(objective)
        if self.is_valid_constraint(objective):
            expr = objective
            if objective.func is Add:
                for s in objective.args:
                    if s.is_Atom:
                        expr -= s

            self.lpmodel += expr

    def is_valid_constraint(self, constraint):
        if isinstance(constraint, BooleanTrue):
            return False

        if isinstance(constraint, BooleanFalse):
            raise ValueError("A constraint was grounded to False. You defined a constraint that can't be satisfied")

        return True


class LpProblem():
    def __init__(self, sense, **options):
        self.sense = sense
        self._index = 0
        self._objective = ()
        self._constraints = {}
        self._constraints[-1] = []
        self._constraints[1] = []
        self._constraints[0] = []
        self._result = None
        self._lp_variables = {}

    def __iadd__(self, other):
        """
        Adds a constraint or objective to the lp.

        :param other: Constraint: Tuple of (lhs, b, sense), where lhs is an expression, b an atom (like an integer)
        and sense either -1, 0 or 1; Objective: An object of type :class:`sympy.core.Expr`
        :return: self
        """
        if isinstance(other, tuple):
            self.add_constraint(other)
        elif isinstance(other, Expr):
            self.add_objective(other)
        else:
            raise ValueError("Tuple (Objective) or Expr (Constraint) was expected.")

        return self

    @property
    def lp_variables(self):
        return self._lp_variables

    def add_lp_variable(self, predicate):
        if predicate.__class__ not in self._lp_variables:
            self._lp_variables[predicate.__class__] = OrderedSet()

        return self._lp_variables[predicate.__class__].add(predicate.args)

    @property
    def lp_variable_count(self):
        return sum([len(predicate) for key, predicate in self._lp_variables.items()])

    def get_scipy_matrices(self, rlpProblem):

        poscounts = {}
        i = 0

        for varclass in rlpProblem.reloop_variables:
            if varclass in self._lp_variables:
                # print "asdf"
                # print varclass
                # print i
                poscounts[varclass] = i
                i += len(self._lp_variables[varclass])

        ineq_constraint_count = len(self._constraints[1]) + len(self._constraints[-1])
        eq_constraint_count = len(self._constraints[0])

        a = scipy.sparse.dok_matrix((eq_constraint_count, self.lp_variable_count))
        b = scipy.sparse.dok_matrix((eq_constraint_count, 1))

        g = scipy.sparse.dok_matrix((ineq_constraint_count, self.lp_variable_count))
        h = scipy.sparse.dok_matrix((ineq_constraint_count, 1))

        c = scipy.sparse.dok_matrix((self.lp_variable_count, 1))

        i = 0
        for constraint in self._constraints[0]:
            for varclass, order, factor in constraint[0]:
                a[i, poscounts[varclass] + order] = factor
            b[i] = constraint[1]
            i += 1

        i = 0
        for constraint in self._constraints[-1]:
            for varclass, order, factor in constraint[0]:
                g[i, poscounts[varclass] + order] = factor
            h[i] = constraint[1]
            i += 1

        for constraint in self._constraints[1]:
            for varclass, order, factor in constraint[0]:
                g[i, poscounts[varclass] + order] = -factor
            h[i] = -constraint[1]
            i += 1

        for variable in self._objective:
            c[poscounts[variable[0]] + variable[1]] = variable[2]

        c = self.sense * c

        return c.todense(), g.tocoo(), h.todense(), a.tocoo(), b.todense()

    def lp_variable(self):
        curr_index = self._index
        self._index += 1
        return curr_index

    def add_constraint(self, constraint_tuple):
        lhs, b, sense = constraint_tuple
        variable_factors = self.get_affine(lhs)
        self._constraints[sense].append((variable_factors, b))

    def add_objective(self, expr):
        self._objective = self.get_affine(expr)

    def get_affine(self, expr):
        # TODO: predicates should be called atoms here!
        predicates, factors = get_predicates_factors(expr)
        length = len(predicates)
        factor_vector = numpy.zeros(length)

        contained_lp_variables = []
        used_lp_variables = []
        lp_variable_orders = []

        for j in range(length):
            lp_variable = self.add_lp_variable(predicates[j])

            if predicates[j] in used_lp_variables:
                factor_vector[used_lp_variables.index(predicates[j])] += factors[j]
            else:
                contained_lp_variables.append(predicates[j])
                used_lp_variables.append(predicates[j])
                lp_variable_orders.append(lp_variable)
                factor_vector[used_lp_variables.index(predicates[j])] = factors[used_lp_variables.index(predicates[j])]
        return [(contained_lp_variables[i].__class__, lp_variable_orders[i], factor_vector[i]) for i in
                range(len(contained_lp_variables))]


def get_predicates_factors(expr):
    pred_names = []
    factors = []

    if expr.func is Add:
        for s in expr.args:
            p, f = get_predicates_factors(s)
            pred_names += p
            factors += f

    elif expr.func is Mul:
        if expr.args[0].is_Atom:
            if isinstance(expr.args[1], RlpPredicate):
                value = expr.args[0]
                pred = expr.args[1]
            else:
                raise NotImplementedError()

        elif isinstance(expr.args[0], RlpPredicate):
            if expr.args[1].is_Atom:
                value = expr.args[1]
                pred = expr.args[0]
            elif isinstance(expr.args[1], RlpPredicate):
                raise ValueError("Found non-linear constraint!")
            else:
                raise NotImplementedError()

        else:
            raise NotImplementedError()

        return [pred], [float(value), ]

    elif isinstance(expr, RlpPredicate):
        return [expr], [float(1), ]

    elif expr.func is Pow:
        raise ValueError("Found non-linear constraint!")
    elif isinstance(expr, Number):
        return pred_names, factors
    else:
        raise NotImplementedError("Cannot get predicates for: " + str(expr) + str(expr.func))

    return pred_names, factors


class ExpressionGrounder(ImmutableVisitor):
    """
    Grounds a sympy expression into a set of lp variables and the grounded expression for the recursive grounder
    """

    def __init__(self, expr, logkb):
        self.logkb = logkb
        self.lp_variables = set([])

        expanded_expr = expand(expr)
        self._result = self.visit(expanded_expr)

    def visit(self, expr):
        """
        Recursively visits the syntax tree nodes for the given expression and executes a method based on the current properties of the node in the tree.

        :param expr: The Sympy expression the visitor visits.
        :type expr: Sympy Add|Mul|RlpSum|Pow
        :return: The ground expression
        """
        if expr.func in [Mul, Add, Pow]:
            return expr.func(*map(lambda a: self.visit(a), expr.args))

        if expr.func is RlpSum:
            result = self.visit_rlpsum(expr)
            return self.visit(result)

        if isinstance(expr, NumericPredicate) and not expr.is_reloop_variable:
            return self.visit_numeric_predicate(expr)

        if expr.func is BooleanPredicate:
            # TODO Evaluate to 0 or 1? Did Martin say: that would be cool?
            raise ValueError("RlpBooleanPredicate is invalid here!")

        return expr

    def visit_rlpsum(self, rlpsum):
        """
        Visitor Method, which is called in case the current node of the syntax tree is an instance of a rlpsum

        :param rlpsum: The current node, which is an instance of a rlpsum
        :type rlpsum: RLPSum
        :return:
        """
        answers = self.logkb.ask(rlpsum.query_symbols, rlpsum.query)
        result = Float(0.0)
        for answer in answers:
            expression_eval_subs = rlpsum.expression
            for index, symbol in enumerate(rlpsum.query_symbols):
                subanswer = answer[index]

                expression_eval_subs = expression_eval_subs.subs(symbol, subanswer)
                # expression_eval_subs = expression_eval_subs.subs(symbol, answer[index])
            result += expression_eval_subs

        return result

    def visit_numeric_predicate(self, pred):
        """
        Visitor Method, which is called in case the current node of the syntrax tree for a given expression is a numeric predicate

        :param pred: The numeric predicate to be processed
        :type pred: Numeric Predicate
        :return:
        """
        args = pred.args
        if len(args) > pred.arity:
            raise Exception("Too many arguments.")

        if len(args) < pred.arity:
            raise Exception("Not enough arguments")

        for argument in args:
            if isinstance(argument, SubSymbol):
                raise ValueError("Found free symbols while grounding: " + str(pred))

        answers = self.logkb.ask_predicate(pred)
        if answers is None:
            raise ValueError('Predicate is not defined or no result!')

        if len(answers) != 1:
            raise ValueError("The LogKb gives multiple results. Oh!")

        result = answers.pop()

        return float(result[0])
