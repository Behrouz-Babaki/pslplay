from reloop.languages.rlp.logkb import *
import getpass
import maxflow_example
from reloop.languages.rlp.grounding.block import BlockGrounder
from reloop.solvers.lpsolver import *

"""
Dependencies:
    psycopg2 > 2.6
----------------
Maxflow example for usage with a Postgres Database.
You will have to specify the database as well as username, password and file location.
The file location can be specified relative to the location of the files.
For the given example specifying the path as "maxflow_example.max" is sufficient.

For further examples on the formatting on the input files please see the filename extension  .max

   n a s       (source)
   n g t       (target)
   n a
   n b         (nodes)
   a a c 20
   a a b 50    (edges and cap)

WARNING : Executing this file will drop the tables "node", "edge", "cost", "source" and "target" if either of them already exists"

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

# Initialize Database with necessary Tables and Values
db_name = raw_input(
    "Please specify the name of your Database "
    "(WARNING: this deletes the current contents of the database! Please use a dummy database.): ")

db_user = raw_input("Pease specify the Username for the Database: ")

db_password = getpass.getpass("Enter your password (Leave blank if None): ")
try:
    connection = psycopg2.connect("dbname=" + str(db_name) + " user=" + str(db_user) + " password=" + str(db_password))
except NameError:
    raise ImportError(
        "Psycopg2 is currently not installed "
        "on your machine therefore we can not establish a connection to your Postgres Database")
except psycopg2.OperationalError:
    raise psycopg2.OperationalError(
        "Your specified credentials could not be used to connect "
        "to any available database. Are you sure that your database is running or installed?")

cursor = connection.cursor()

# Drop Tables
cursor.execute("DROP TABLE IF EXISTS node")
cursor.execute("DROP TABLE IF EXISTS edge")
cursor.execute("DROP TABLE IF EXISTS cost")
cursor.execute("DROP TABLE IF EXISTS source")
cursor.execute("DROP TABLE IF EXISTS target")
connection.commit()

cursor.execute("CREATE TABLE node (x varchar(255));")

cursor.execute("CREATE TABLE edge (x varchar(255), y varchar(255));")
" +  + "
cursor.execute("CREATE TABLE cost (x varchar(255), y varchar(255), z INTEGER NOT NULL);")
cursor.execute("CREATE TABLE source (x varchar(255));")

cursor.execute("CREATE TABLE target (x varchar(255));")

connection.commit()
path = raw_input("Please specify a path for a maxflow file: ")
file = open(path, "r")

count = 0
for line in file:
    temp = line.split()
    if temp[0] == "n" and len(temp) == 3:
        if temp[2] == 's':
            cursor.execute("INSERT INTO source values('" + temp[1] + "')")
        elif temp[2] == 't':
            cursor.execute("INSERT INTO target values('" + temp[1] + "')")
    elif temp[0] == "n":
        cursor.execute("INSERT INTO node values('" + temp[1] + "')")
    if temp[0] == "a":
        cursor.execute("INSERT INTO edge values('" + temp[1] + "'" + "," + "'" + temp[2] + "')")
        cursor.execute(
            "INSERT INTO cost values('" + temp[1] + "'" + "," + "'" + temp[2] + "' , " + temp[
                3] + ")")
    else:
        continue
    count += 1
    if count % 10000 == 0:
        print "Reading File Please Wait ...\n " + str(count) + " Lines were read so far."
    connection.commit()

cursor.close()
connection.close()
file.close()

solver = CvxoptSolver()
logkb = PostgreSQLKb(db_name, db_user, db_password)
grounder = BlockGrounder(logkb)
model = maxflow_example.maxflow(grounder, solver)
