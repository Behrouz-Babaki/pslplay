import maxflow_example
from reloop.languages.rlp.grounding.block import *
from reloop.solvers.lpsolver import CvxoptSolver

'''
Depencendies:
    ProbLog>2.1
---------------
Maxflow example, which uses the implemented prolog logical knowledge base contained in ProbLog 2.1
For further use one has to specify their own data by creating a prolog file "*.pl" and add the necessary knowledge to the file.
Then one has to proceed writing their own linear program or use one of our examples with your data.

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
'''

logkb = ProbLogKB("maxflow_prolog.pl")
grounder = BlockGrounder(logkb)
solver = CvxoptSolver()

model = maxflow_example.maxflow(grounder, solver)
