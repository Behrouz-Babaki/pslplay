from reloop.languages.rlp.grounding.block import *
from reloop.solvers.lpsolver import *
import getpass
import maxflow_example


"""
Dependencies:
    psycopg2 > 2.6
----------------
Maxflow example, which uses already present data from a Postgres Database.
For the maxflow example the stored data is supposed to be in the following tables :
    "node"
    "edge"
    "cost"
    "source"
    "target"

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


db_name = raw_input("Please specify the name of your Database: ")
db_user = raw_input("Pease specify the Username for the Database: ")
db_password = getpass.getpass("Enter your password (Leave blank if None): ")

#db_name= "reloop"
#db_user = "reloop2"
#db_password="reloop"
logkb = PostgreSQLKb(db_name, db_user, db_password)
grounder = BlockGrounder(logkb)
solver = CvxoptSolver()
model = maxflow_example.maxflow(grounder, solver)
