from reloop.languages.rlp import *
import maxflow_example
from reloop.solvers.lpsolver import CvxoptSolver
from reloop.languages.rlp.logkb import PyDatalogLogKb
from pyDatalog import pyDatalog

"""
Dependencies:
    PyDatalog>0.15.2
--------------------
Maxflow example, which uses the implemented PyDatalog knowledge base interface. The pure python way to define one's
predicates is to assert the predicates via pyDatalog as shown below.

pyDatalog.assert_fact(predicate_name, arg_1, arg_2 ...,arg_n)

Additionally one can use one of the already available solvers and grounders by creating the appropriate object.

grounder = Blockgrounder(logkb) | RecursiveGrounder(logkb)
logkb = PyDatalogKB() | PostgreSQLKb(dbname,user,password) | PrologKb(swi_prolog_object) | ProbLogKb(path_to_pl_file)
solver = CvxoptSolver() | PicosSolver()

Additional parameters for the solver can be passed onto the solver / lifted solver by simply creating the solver object
with the prefered arguments. For more information on the available parameters see lpsolvers.py.

We recommend using the Block Grounding as it is more efficient especially grounding problems with huge amounts of data.
For further information on the different logkbs please see the corresponding examples.

After instantiating the objects one only has to create a model to solve the rlp.

model = ...
"""

pyDatalog.assert_fact('node', 'a')
pyDatalog.assert_fact('node', 'b')
pyDatalog.assert_fact('node', 'c')
pyDatalog.assert_fact('node', 'd')
pyDatalog.assert_fact('node', 'e')
pyDatalog.assert_fact('node', 'f')
pyDatalog.assert_fact('node', 'g')

pyDatalog.assert_fact('edge', 'a', 'b')
pyDatalog.assert_fact('edge', 'a', 'c')
pyDatalog.assert_fact('edge', 'b', 'd')
pyDatalog.assert_fact('edge', 'b', 'e')
pyDatalog.assert_fact('edge', 'c', 'd')
pyDatalog.assert_fact('edge', 'c', 'f')
pyDatalog.assert_fact('edge', 'd', 'e')
pyDatalog.assert_fact('edge', 'd', 'f')
pyDatalog.assert_fact('edge', 'e', 'g')
pyDatalog.assert_fact('edge', 'f', 'g')

pyDatalog.assert_fact('source','a')
pyDatalog.assert_fact('target', 'g')

pyDatalog.assert_fact('cost', 'a', 'b', 50 )
pyDatalog.assert_fact('cost', 'a', 'c', 100)
pyDatalog.assert_fact('cost', 'b', 'd', 40 )
pyDatalog.assert_fact('cost', 'b', 'e', 20 )
pyDatalog.assert_fact('cost', 'c', 'd', 60 )
pyDatalog.assert_fact('cost', 'c', 'f', 20 )
pyDatalog.assert_fact('cost', 'd', 'e', 50 )
pyDatalog.assert_fact('cost', 'd', 'f', 60 )
pyDatalog.assert_fact('cost', 'e', 'g', 70 )
pyDatalog.assert_fact('cost', 'f', 'g', 70 )


logkb = PyDatalogLogKb()
grounder = BlockGrounder(logkb)

solver = CvxoptSolver()
model = maxflow_example.maxflow(grounder, solver)
