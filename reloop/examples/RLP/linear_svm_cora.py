from reloop.languages.rlp.grounding.block import*
import logging, sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
import getpass

"""
This example implements the LP SVM as proposed by Zhou et. al 2001 (Linear Programming Support Vector Machines)

For a thorough explanation please see our examples in the Documentation.

After running linearsvm_load you can use this implementation to execute the lp svm on the given data. If you are using any
other data make sure you change the predicates and model accordingly.


"""
log.setLevel(logging.INFO)

db_name = raw_input(
    "Please specifiy the name of your (populated) database: ")
db_user = raw_input("Pease specify the Username for the Database: ")
db_password = getpass.getpass("Enter your password (Leave blank if None):")

logkb = PostgreSQLKb(db_name,  db_user, db_password)
grounder = BlockGrounder(logkb)

model = RlpProblem("LP-SVM cora", LpMinimize, grounder, CvxoptSolver())

# Constant for the Objective
c = 1.0

# Variable Declarations
X, Z, J, I, P, Q = sub_symbols('X', 'Z', 'J', 'I', 'P', 'Q')

# Predicate Declarations
paper = numeric_predicate("paper", 1)
slack = numeric_predicate("slack", 1)
weight = numeric_predicate("weight", 1)
label = numeric_predicate("label", 1)
kernel = numeric_predicate("rbf_values", 2)

b = numeric_predicate("b", 0)
r = numeric_predicate("r", 0)

b_paper = boolean_predicate("paper", 2)
b_label = boolean_predicate("label", 2)

model.add_reloop_variable(slack, weight, b, r)

# Objective
slacks = RlpSum({I}, b_label(I, Q), slack(I))
model += -r() + c * slacks

# Constraints
model += ForAll({I, Z}, b_paper(I, Z),
                label(I) * (RlpSum({X,J}, b_paper(X, J), weight(X) * label(X) * kernel(Z, J)) + b()) + slack(I) >= r())

model += ForAll({X}, b_paper(X, I), weight(X) <= 1)
model += ForAll({X}, b_paper(X, I), -weight(X) <= 1)
model += r() >= 0
model += ForAll({I}, b_label(I, Z), slack(I) >= 0)

print("The model has been built.")
print model

model.solve()

#print("The model has been solved: " + model.status() + ".")

sol = model.get_solution()
print(sol)



