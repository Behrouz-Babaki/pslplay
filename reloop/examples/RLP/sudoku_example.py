from reloop.languages.rlp import *
import time
import logging
import sys

def sudoku(grounder,solver):
    model = RlpProblem("play sudoku for fun and profit",
                       LpMaximize, grounder, solver)

    I, J, X, U, V = sub_symbols('I', 'J', 'X', 'U', 'V')
    """
    We have an n x n array of cells. The indices 1 to n are defined with num(1), ..., num(n).
    The predicate fill(I,J,X) indicates the assignment of cell I,J with number X.
    """

    num = boolean_predicate("num", 1)
    boxind = boolean_predicate("boxind", 1)
    box = boolean_predicate("box", 4)
    initial = boolean_predicate("initial", 3)
    fill = numeric_predicate("fill", 3)


    model.add_reloop_variable(fill)

    # each cell receives exactly one number
    model += ForAll([I, J], num(I) & num(J), RlpSum([X, ], num(X), fill(I, J, X)) >= 1)
    model += ForAll([I, J], num(I) & num(J), RlpSum([X, ], num(X), fill(I, J, X)) <= 1)

    # each number is encountered exactly once per row
    model += ForAll([I, X], num(I) & num(X), RlpSum([J, ], num(J), fill(I, J, X)) >= 1)
    model += ForAll([I, X], num(I) & num(X), RlpSum([J, ], num(J), fill(I, J, X)) <= 1)

    # each number is encountered exactly once per column
    model += ForAll([J, X], num(J) & num(X), RlpSum([I, ], num(I), fill(I, J, X)) >= 1)
    model += ForAll([J, X], num(J) & num(X), RlpSum([I, ], num(I), fill(I, J, X)) <= 1)

    # each number is encountered exactly once per box
    model += ForAll([X, U, V], num(X) & boxind(U) & boxind(V), RlpSum([I, J], box(I, J, U, V), fill(I, J, X)) >= 1)
    model += ForAll([X, U, V], num(X) & boxind(U) & boxind(V), RlpSum([I, J], box(I, J, U, V), fill(I, J, X)) <= 1)

    # nonnegativity
    model += ForAll([I, J, X], num(X) & num(I) & num(J), fill(I, J, X) >= 0)

    # initial assignment
    model += ForAll([I, J, X], initial(I, J, X), fill(I, J, X) <= 1)
    model += ForAll([I, J, X], initial(I, J, X), fill(I, J, X) >= 1)

    # objective
    model += RlpSum([X, ], num(X), fill(1, 1, X))

    model.solve()

    sol = model.get_solution()
    print "The solutions for the fill variables are:\n"
    for key, value in sol.iteritems():
        if round(value, 2) >= 0.99:
            print key, "=", round(value, 2)
