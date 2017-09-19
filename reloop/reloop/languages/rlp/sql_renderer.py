from collections import namedtuple
from rlp import *
from sympy.logic.boolalg import *
from sympy.core import *

ALIAS_PREFIX = "a"

ColDesc = namedtuple('ColumnDescription', 'tbl_alias col_index')

def from_logical_query(query_symbols, logical_query, coeff_expr, cursor):
    sel = tuple(query_symbols)
    if coeff_expr is not None:
        sel += (coeff_expr,)
    renderer = SQLRenderer(sel, cursor)
    renderer.visit(logical_query)
    return renderer.to_sql()


class SQLRenderer(object):
    """
    We assume queries of the form And(pred1, Not(pred2), Not(pred3), ...,) OR And(pred4, Not(pred5), pred6, ...,) OR ...

    (c1 AND c2 AND c3) OR (c1 AND c2 AND c3)
    """

    def __init__(self, selector, cursor):
        self.selector = selector
        self.cursor = cursor
        self.result = ""
        self.current_clause = Clause(self.selector)
        self.clauses = []
        self.predicate_column_names = {}

        self.in_negation = False

    def visit(self, query):
        if hasattr(query, 'func') and query.func is Or:
            self.visit_or(query)
        elif hasattr(query, 'func') and query.func is And:
            self.visit_and(query)
        elif isinstance(query, BooleanPredicate):
            self.visit_boolean_predicate(query)
        elif isinstance(query, Not):
            self.visit_not(query)
        elif isinstance(query, Rel):
            self.visit_relation(query)
        elif isinstance(query, BooleanTrue):
            return
        else:
            raise ValueError('Invalid query type: ' + str(type(query)))

    def visit_or(self, query):
        for clause in query.args:
            self.visit(clause)
            self.clauses.append(self.current_clause)
            self.current_clause = Clause(self.selector)

    def visit_and(self, query):
        for condition in query.args:
            self.visit(condition)

    def visit_not(self, query):
        self.in_negation = True
        self.visit(query.args[0])
        self.in_negation = False

    def visit_boolean_predicate(self, query):
        rel_key = query.name
        if not self.predicate_column_names.has_key(rel_key):
            self.predicate_column_names[rel_key] = get_column_names(rel_key, self.cursor)

        if self.in_negation:
            self.current_clause.add_negative_predicate(query)
        else:
            self.current_clause.add_positive_predicate(query)

    def visit_relation(self, query):
        self.current_clause.add_relation(query)

    def to_sql(self):
        return " UNION ".join([clause.to_sql(self.predicate_column_names) for clause in self.clauses + [self.current_clause]])


class Clause(object):

    def __init__(self, selector):
        self.selector = selector
        self.alias_id = 0
        # {SubSymbol: [(tbl_alias, col)]}
        self.colum_of_symbols = {}
        # [(tbl, tbl_alias)]
        self.from_ = []

        self.rel_cond = []
        self.const_cond = []

        # anti joins
        self.not_exists = []


    def next_alias(self):
        self.alias_id += 1
        return ALIAS_PREFIX + str(self.alias_id)

    def add_positive_predicate(self, predicate):
        alias = self.next_alias()
        self.from_.append((predicate.name, alias))

        for index, arg in enumerate(predicate.args):
            col = ColDesc(alias, index)
            if isinstance(arg, SubSymbol):

                if not self.colum_of_symbols.has_key(arg):
                    self.colum_of_symbols[arg] = []

                self.colum_of_symbols[arg].append(col)
            else:
                self.const_cond.append((col, arg))

    def add_negative_predicate(self, predicate):
        self.not_exists.append(predicate)

    def add_relation(self, rel):
        self.rel_cond.append(rel)

    def to_sql(self, predicate_columns):
        self.predicate_columns = predicate_columns

        sql = "SELECT DISTINCT "
        sql += ", ".join(self.render_selectors())
        sql += " FROM "
        sql += ", ".join([name + " AS " + alias for name, alias in self.from_])

        join_cond = self.render_join_conditions()
        constant_cond = self.render_constant_conditions()
        rel_cond = self.render_relations()
        anti_join_cond = self.render_anti_joins()

        conditions = join_cond + constant_cond + rel_cond + anti_join_cond
        if len(conditions) > 0:
            sql += " WHERE "

        sql += ' AND '.join(conditions)
        return sql

    def render_selectors(self):
        selectors = []
        for sel in self.selector:
            if isinstance(sel, SubSymbol):
                selectors.append(self.render_cond_side(self.colum_of_symbols[sel][0]) + " AS " + str(sel))
            else:
                expr_as_string = str(sel)
                for symbol, coldesc in self.colum_of_symbols.items():
                    if isinstance(symbol, VariableSubSymbol):
                        expr_as_string = expr_as_string.replace(str(symbol), self.render_cond_side(coldesc[0]))

                selectors.append(expr_as_string)

        return selectors

    def render_join_conditions(self):
        join_cond = []
        for subsymbol_conditions in self.colum_of_symbols.itervalues():
            if len(subsymbol_conditions) > 1:
                first = subsymbol_conditions[0]
                for cond in subsymbol_conditions[1:]:
                    join_cond.append((first, cond))

        return [self.render_equality(lhs, rhs) for lhs, rhs in join_cond]

    def render_constant_conditions(self):
        return [self.render_equality(lhs, rhs) for lhs, rhs in self.const_cond]

    def render_anti_joins(self):
        anti_joins = []
        for index, pred in enumerate(self.not_exists):
            sql = "NOT EXISTS (SELECT 1 FROM " + pred.name + " where "
            cond = []
            for index, arg in enumerate(pred.args):
                if isinstance(arg, SubSymbol):
                    cond.append((ColDesc(pred.name, index), self.colum_of_symbols[arg][0]))
                else:
                    cond.append((ColDesc(pred.name, index), arg))

            sql += " AND ".join([self.render_equality(lhs, rhs) for lhs, rhs in cond])
            sql += ")"
            anti_joins.append(sql)
        return anti_joins

    def render_relations(self):
        rel_cond = []
        for rel in self.rel_cond:
            if isinstance(rel.lhs, SubSymbol):
                lhs = self.colum_of_symbols[rel.lhs][0]
            else:
                lhs = rel.lhs
            if isinstance(rel.rhs, SubSymbol):
                rhs = self.colum_of_symbols[rel.rhs][0]
            else:
                rhs = rel.rhs

            rel_cond.append(self.render_relation(lhs, rhs, rel.func))

        return rel_cond

    def render_relation(self, lhs, rhs, rel_class):
        if rel_class is LessThan:
            rel_symbol = "<="
        elif rel_class is StrictLessThan:
            rel_symbol = "<"
        elif rel_class is GreaterThan:
            rel_symbol = ">="
        elif rel_class is StrictGreaterThan:
            rel_symbol = ">"
        elif rel_class is Equality:
            rel_symbol = "="
        else:
            raise NotImplementedError('Rendering for relation ' + str(rel_class) + ' is not implemented')

        lhs = self.render_cond_side(lhs)
        rhs = self.render_cond_side(rhs)

        return lhs + " " + rel_symbol + " " + rhs

    def render_cond_side(self, item):
            if isinstance(item, ColDesc):
                result = item.tbl_alias + "." + self.get_column_name(item.tbl_alias, item.col_index)
            else:
                result = str(item)

            return result

    def render_equality(self, lhs, rhs):
        return self.render_relation(lhs, rhs, Eq)

    def get_column_name(self, name, index):
        for tbl, tbl_alias in self.from_:
            if tbl_alias == name:
                name = tbl
                break

        return self.predicate_columns[name][index]

def get_column_names(relation_name, cursor):
        """
        Gets the name of the columns for a given table.

        :param relation_name: The name of the table
        :type relation_name: str
        :return: A list consisting of the column names.
        """
        if cursor is None:
            return [str(i) for i in range(1,255)]

        query = "SELECT column_name FROM information_schema.columns where table_name=" + "'" + relation_name.lower() \
                + "' ORDER BY ordinal_position ASC"
        cursor.execute(query)
        ans = [item[0] for item in cursor.fetchall()]
        return ans