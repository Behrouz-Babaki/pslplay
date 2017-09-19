from reloop.languages.rlp import *
import time
import logging
import sys

def maxflow(grounder, solver):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    start = time.time()
    model = RlpProblem("traffic flow LP in the spirit of page 329 in http://ampl.com/BOOK/CHAPTERS/18-network.pdf",
                       LpMaximize, grounder, solver)

    print "\nBuilding a relational variant of the " + model.name

    # declarations
    X, Y, Z = sub_symbols('X', 'Y', 'Z')

    flow = numeric_predicate("flow", 2)
    cost = numeric_predicate("cost", 2)

    model.add_reloop_variable(flow)

    source = boolean_predicate("source", 1)
    target = boolean_predicate("target", 1)
    edge = boolean_predicate("edge", 2)
    node = boolean_predicate("node", 1)

    # objective
    model += RlpSum([X, Y], source(X) & edge(X, Y), flow(X, Y))

    ask = grounder.ask

    #model += ForAll([Z, ], node(Z) & ~source(Z) & ~target(Z), RlpSum([X, ], edge(X, j), flow(X, j)) |eq| RlpSum([Y, ], edge(j, Y), flow(j, Y))
    model += (RlpSum([X, ], edge(X, j), flow(X, j)) |eq| RlpSum([Y, ], edge(j, Y), flow(j, Y))
        for (j,) in ask(node(Z) & ~source(Z) & ~target(Z))
    )

    # model += ForAll([X, Y], edge(X, Y), flow(X, Y) | ge | 0)
    model += (flow(x, y) |ge| 0
        for (x,y) in ask(edge(X,Y))
    )

    # model += ForAll([X, Y], edge(X, Y), flow(X, Y) | le | cost(X, Y))
    for (x, y) in ask(edge(X,Y)):
        model += flow(x, y) |le| cost(x, y)



    print "The model has been built:"
    print(model)

    model.solve()

    end = time.time()

    print "\nThe model has been solved: " + str(model.status()) + "."

    sol = model.get_solution()

    print "The solutions for the flow variables are:\n"

    total = 0
    for key, value in sol.iteritems():
        print(str(key) + " = " + str(value))
        total += value

    try:
        inflow = sol[(flow, (Symbol('a'), Symbol('b')))] + sol[(flow, (Symbol('a'), Symbol('c')))]
    except KeyError:
        inflow = sol['flow(a,b)'] + sol['flow(a,c)']

    print "\nTime needed for the grounding and solving: " + str(end - start) + " s."
    # TODO: Change output to display correct results for an arbitrary number of edges outgoing from the source
    print "\nThus, the maximum flow entering the traffic network at node a is " + str(inflow) + " cars per hour."
    print "\nThe total flow in the traffic network is " + str(total) + " cars per hour."


