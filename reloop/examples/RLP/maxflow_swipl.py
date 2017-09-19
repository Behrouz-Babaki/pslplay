from pyswip import Prolog
import maxflow_example
from reloop.languages.rlp.logkb import PrologKB
from reloop.languages.rlp.grounding.block import *
from reloop.solvers.lpsolver import CvxoptSolver
from reloop.languages.rlp.grounding.recursive import RecursiveGrounder

"""
Dependencies :
    PySwip 0.23 (pip installs 0.22)
    Ctypes Version > 1.0
    libpl.so in /usr/lib shared library of swi prolog (to install compile prolog from source and set the shared libary flag

Maxflow example for Reloop using the python SWI-Prolog interface. One can either define their predicates directly in
python as shown below or create a seperate "*.pl" file with the necessary data. By creating a prolob object and asserting
the facts or consulting a file (prolog.consult(path_to_fike)) one can easily define their own maxflow problem and solve
it with Reloop.

Additionally one can use one of the already available solvers and grounders by creating the appropriate object.

grounder = RecursiveGrounder(logkb)
logkb = PyDatalogKB() | PostgreSQLKb(dbname,user,password) | PrologKb(swi_prolog_object) | ProbLogKb(path_to_pl_file)
solver = CvxoptSolver() | PicosSolver()

Additional parameters for the solver can be passed onto the solver / lifted solver by simply creating the solver object
with the prefered arguments. For more information on the available parameters see lpsolvers.py.

We recommend using the Block Grounding as it is more efficient especially grounding problems with huge amounts of data.
For further information on the different logkbs please see the corresponding examples.

After instantiating the objects one only has to create a model to solve the rlp.

model = ...

"""

prolog = Prolog()


###############################################################################################################
# Directly inserts the predicates into the PrologKB via the prolog object.

nodes = ["a", "b", "c", "d", "e", "f", "g"]
edges = ["a,b", "a,c", "b,d", "b,e", "c,d", "c,f", "d,e", "d,f", "e,g", "f,g"]
costs = ["a,b,'50'", "a,c,'100'", "b,d,'40'", "b,e,'20'", "c,d,'60'", "c,f,'20'", "d,e,'50'", "d,f,'60'", "e,g,'70'",
         "f,g,'70'"]
source = ["a"]
target = ["g"]
prolog.assertz("source(" + source[0] + ")")
prolog.assertz("target(" + target[0] + ")")
# print list(prolog.query("test(A,B,C,D,E,F,G)"))
for node in nodes:
    prolog.assertz("node(" + node + ")")
for edge in edges:
    insert = "edge(" + edge + ")"
    #    print insert
    prolog.assertz(insert)
for cost in costs:
    insert = "cost(" + cost + ")"
    #    print insert
    prolog.assertz(insert)


#prolog.consult("maxflow_swipl.pl")
logkb = PrologKB(prolog)
# BlockGrounding not supported yet
grounder = RecursiveGrounder(logkb)
solver = CvxoptSolver()
model = maxflow_example.maxflow(grounder, solver)
