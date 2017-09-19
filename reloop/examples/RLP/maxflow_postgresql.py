from reloop.languages.rlp.logkb import *
from reloop.languages.rlp.grounding.block import BlockGrounder
from reloop.solvers.lpsolver import *
import maxflow_example
import getpass

"""
Dependencies:
    psycopg2 > 2.6
----------------
Maxflow example for usage with a Postgres Database.
You will have to specify the database as well as username, password.
This examples creates the tables and its contents directly from python code, by using psycopg2 as an interface.
Creating a cursor allows one to directly manipulate tables and its contents in the database by executing queries
and commands.

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
    "Please specifiy the name of your Database (WARNING: this deletes the current contents of the database! Please use a dummy database.): ")
db_user = raw_input("Pease specify the Username for the Database: ")
db_password = getpass.getpass("Enter your password (Leave blank if None):")
try:
    connection = psycopg2.connect("dbname=" + str(db_name) + " user=" + str(db_user) + " password=" + str(db_password))
except NameError:
    raise ImportError(
        "Psycopg2 is not currently installed on your machine therefore we can not establish a connection to your Postgres Database")
except psycopg2.OperationalError:
    raise psycopg2.OperationalError(
        "Your specified credetials could not be used to connect to any available database.Are you sure that your database is running or installed?")
cursor = connection.cursor()

# Drop Tables
cursor.execute("DROP TABLE IF EXISTS node ")
cursor.execute("DROP TABLE IF EXISTS edge")
cursor.execute("DROP TABLE IF EXISTS cost")
cursor.execute("DROP TABLE IF EXISTS source")
cursor.execute("DROP TABLE IF EXISTS target")
connection.commit()

# Insert data
cursor.execute("CREATE TABLE node (x varchar(5));")
cursor.execute("INSERT INTO node values('a'),('b'),('c'),('d'),('e'),('f'),('g');")

cursor.execute("CREATE TABLE edge (x varchar(5), y varchar(5));")
cursor.execute(
    "INSERT INTO edge values('a','b'),('a','c'),('b','d'),('b','e'),('c','d'),('c','f'),('d','e'),('d','f'),('e','g'),('f','g');")

cursor.execute("CREATE TABLE cost (x varchar(5), y varchar(5), z INTEGER NOT NULL);")
cursor.execute(
    "INSERT INTO cost values('a','b',50),('a','c',100),('b','d',40),('b','e',20),('c','d',60),('c','f',20),('d','e',50),('d','f',60),('e','g',70),('f','g',70);")

cursor.execute("CREATE TABLE source (x varchar(5));")
cursor.execute("INSERT INTO source values('a');")

cursor.execute("CREATE TABLE target (x varchar(5));")
cursor.execute("INSERT INTO target values('g');")

connection.commit()
cursor.close()
connection.close()

logkb = PostgreSQLKb(db_name, db_user, db_password)
grounder = BlockGrounder(logkb)
solver = CvxoptSolver()
maxflow_example.maxflow(grounder, solver)
